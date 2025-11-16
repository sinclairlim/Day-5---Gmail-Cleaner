from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import base64
import email
import time


class GmailService:
    def __init__(self, credentials: Credentials):
        self.service = build('gmail', 'v1', credentials=credentials)
        self.user_id = 'me'
        self.progress_callback: Optional[Callable] = None

    def get_user_info(self) -> Dict[str, Any]:
        """Get user profile information"""
        try:
            profile = self.service.users().getProfile(userId=self.user_id).execute()
            return {
                'email': profile.get('emailAddress'),
                'total_messages': profile.get('messagesTotal', 0),
                'threads_total': profile.get('threadsTotal', 0)
            }
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise

    def search_emails(self, query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Search emails based on Gmail query syntax with pagination support"""
        try:
            all_messages = []
            page_token = None

            # Gmail API returns max 500 results per page, so we need to paginate
            while len(all_messages) < max_results:
                # Request up to 500 messages per page (Gmail API limit)
                page_size = min(500, max_results - len(all_messages))

                results = self.service.users().messages().list(
                    userId=self.user_id,
                    q=query,
                    maxResults=page_size,
                    pageToken=page_token
                ).execute()

                messages = results.get('messages', [])
                if not messages:
                    break

                all_messages.extend(messages)

                # Check if there are more pages
                page_token = results.get('nextPageToken')
                if not page_token:
                    break

            # Now fetch details for all messages in batches
            detailed_messages = []
            batch_size = 50  # Reduced from 100 to avoid rate limits
            total_batches = (len(all_messages) + batch_size - 1) // batch_size

            for batch_idx, i in enumerate(range(0, len(all_messages), batch_size)):
                batch = all_messages[i:i + batch_size]

                # Update progress
                if self.progress_callback:
                    progress = int((batch_idx / total_batches) * 100)
                    self.progress_callback({
                        'progress': progress,
                        'current': len(detailed_messages),
                        'total': len(all_messages),
                        'status': f'Processing batch {batch_idx + 1} of {total_batches}'
                    })

                # Create batch request
                batch_request = self.service.new_batch_http_request()

                def callback(request_id, response, exception):
                    if exception:
                        print(f"Error fetching message: {exception}")
                    elif response:
                        msg_detail = self._parse_message_response(response)
                        if msg_detail:
                            detailed_messages.append(msg_detail)

                # Add all requests to batch
                for message in batch:
                    batch_request.add(
                        self.service.users().messages().get(
                            userId=self.user_id,
                            id=message['id'],
                            format='full'
                        ),
                        callback=callback
                    )

                # Execute batch
                batch_request.execute()

                # Add delay between batches to avoid rate limits
                # Gmail allows ~250 quota units per second, each message.get costs 5 units
                # So 50 messages = 250 units, we need to wait 1 second
                if i + batch_size < len(all_messages):
                    time.sleep(1)

            # Final progress update
            if self.progress_callback:
                self.progress_callback({
                    'progress': 100,
                    'current': len(detailed_messages),
                    'total': len(all_messages),
                    'status': 'Complete'
                })

            return detailed_messages
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise

    def _parse_message_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a Gmail message response into our format"""
        try:
            headers = message.get('payload', {}).get('headers', [])
            header_dict = {h['name']: h['value'] for h in headers}

            # Get email size
            size_estimate = message.get('sizeEstimate', 0)

            # Parse date
            date_str = header_dict.get('Date', '')
            try:
                date = email.utils.parsedate_to_datetime(date_str)
            except:
                date = datetime.now()

            return {
                'id': message['id'],
                'thread_id': message['threadId'],
                'subject': header_dict.get('Subject', 'No Subject'),
                'sender': header_dict.get('From', 'Unknown'),
                'date': date.isoformat(),
                'size': size_estimate,
                'labels': message.get('labelIds', []),
                'snippet': message.get('snippet', '')
            }
        except Exception as error:
            print(f"Error parsing message: {error}")
            return None

    def get_message_details(self, message_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific email"""
        try:
            message = self.service.users().messages().get(
                userId=self.user_id,
                id=message_id,
                format='full'
            ).execute()

            return self._parse_message_response(message)
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def scan_spam_emails(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """Find potential spam emails"""
        query = "label:spam OR (is:unread older_than:30d)"
        return self.search_emails(query, max_results)

    def scan_large_emails(self, min_size_mb: float = 5.0, max_results: int = 100) -> List[Dict[str, Any]]:
        """Find large emails (sorted by size descending)"""
        # Gmail doesn't support size queries directly, so we search and filter
        # We'll search for emails with attachments as they tend to be larger
        query = "has:attachment"

        # Fetch more emails to ensure we get enough large ones
        emails = self.search_emails(query, max_results * 3)

        # Filter by minimum size
        min_size_bytes = min_size_mb * 1024 * 1024
        large_emails = [e for e in emails if e['size'] >= min_size_bytes]

        # Sort by size descending and limit results
        large_emails.sort(key=lambda x: x['size'], reverse=True)
        return large_emails[:max_results]

    def scan_old_emails(self, days_old: int = 365, max_results: int = 100) -> List[Dict[str, Any]]:
        """Find old emails"""
        query = f"older_than:{days_old}d"
        return self.search_emails(query, max_results)

    def delete_emails(self, email_ids: List[str]) -> Dict[str, Any]:
        """Delete multiple emails (move to trash)"""
        failed_ids = []
        deleted_count = 0

        for email_id in email_ids:
            try:
                self.service.users().messages().trash(
                    userId=self.user_id,
                    id=email_id
                ).execute()
                deleted_count += 1
            except HttpError as error:
                print(f"Failed to delete {email_id}: {error}")
                failed_ids.append(email_id)

        return {
            'deleted_count': deleted_count,
            'failed_ids': failed_ids,
            'message': f'Successfully deleted {deleted_count} emails'
        }

    def analyze_senders(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze emails by sender - group and count"""
        from collections import defaultdict

        sender_stats = defaultdict(lambda: {'count': 0, 'total_size': 0, 'emails': []})

        for email in emails:
            sender = email['sender']
            # Extract email address from "Name <email@domain.com>" format
            if '<' in sender and '>' in sender:
                sender_email = sender.split('<')[1].split('>')[0].strip()
            else:
                sender_email = sender.strip()

            sender_stats[sender_email]['count'] += 1
            sender_stats[sender_email]['total_size'] += email['size']
            sender_stats[sender_email]['emails'].append(email['id'])

        # Convert to list and sort by count (descending)
        result = []
        for sender, stats in sender_stats.items():
            result.append({
                'sender': sender,
                'count': stats['count'],
                'total_size_mb': stats['total_size'] / (1024 * 1024),
                'email_ids': stats['emails']
            })

        # Sort by count descending
        result.sort(key=lambda x: x['count'], reverse=True)
        return result

    def get_stats(self) -> Dict[str, Any]:
        """Get overall Gmail statistics"""
        try:
            spam_emails = self.scan_spam_emails(max_results=500)
            large_emails = self.scan_large_emails(max_results=500)
            old_emails = self.scan_old_emails(max_results=500)

            total_size = sum(e['size'] for e in spam_emails + large_emails + old_emails)

            return {
                'total_emails': len(spam_emails) + len(large_emails) + len(old_emails),
                'total_size_mb': total_size / (1024 * 1024),
                'spam_count': len(spam_emails),
                'large_emails_count': len(large_emails),
                'old_emails_count': len(old_emails)
            }
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise
