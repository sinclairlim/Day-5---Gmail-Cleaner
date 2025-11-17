from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
import base64
import email
import time
import random


class GmailService:
    def __init__(self, credentials: Credentials):
        self.service = build('gmail', 'v1', credentials=credentials)
        self.user_id = 'me'
        self.progress_callback: Optional[Callable] = None

        # Rate limiting configuration
        self.max_retries = 5
        self.base_delay = 1.0  # seconds
        self.max_delay = 32.0  # seconds

    def _execute_with_backoff(self, request, operation_name: str = "API call"):
        """Execute a request with exponential backoff retry logic"""
        for attempt in range(self.max_retries):
            try:
                return request.execute()
            except HttpError as error:
                # Check if it's a rate limit error (429)
                if error.resp.status == 429:
                    if attempt < self.max_retries - 1:
                        # Calculate exponential backoff with jitter
                        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                        jitter = random.uniform(0, 0.3 * delay)
                        sleep_time = delay + jitter

                        print(f"Rate limit hit on {operation_name}. Retrying in {sleep_time:.2f}s (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(sleep_time)
                    else:
                        print(f"Max retries reached for {operation_name}")
                        raise
                else:
                    # Non-rate-limit error, raise immediately
                    raise
            except Exception as error:
                print(f"Unexpected error in {operation_name}: {error}")
                raise

    def get_user_info(self) -> Dict[str, Any]:
        """Get user profile information"""
        try:
            profile = self._execute_with_backoff(
                self.service.users().getProfile(userId=self.user_id),
                "get_user_info"
            )
            return {
                'email': profile.get('emailAddress'),
                'total_messages': profile.get('messagesTotal', 0),
                'threads_total': profile.get('threadsTotal', 0)
            }
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise

    def search_emails(self, query: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """Search emails based on Gmail query syntax - SIMPLIFIED VERSION"""
        try:
            print(f"\n=== Starting email search: query='{query}', max_results={max_results} ===")

            all_messages = []
            page_token = None

            # Step 1: Get list of message IDs
            while len(all_messages) < max_results:
                page_size = min(500, max_results - len(all_messages))

                print(f"Fetching message IDs (page_size={page_size})...")
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
                print(f"Got {len(messages)} message IDs (total: {len(all_messages)})")

                page_token = results.get('nextPageToken')
                if not page_token:
                    break

            if not all_messages:
                print("No messages found")
                return []

            print(f"\n=== Fetching details for {len(all_messages)} messages ===")

            # Step 2: Fetch details one by one (simple, no batching)
            detailed_messages = []

            for idx, msg in enumerate(all_messages, 1):
                try:
                    # Update progress
                    if self.progress_callback:
                        progress = int((idx / len(all_messages)) * 100)
                        self.progress_callback({
                            'progress': progress,
                            'current': idx,
                            'total': len(all_messages),
                            'status': f'Fetching email {idx} of {len(all_messages)}'
                        })

                    # Fetch metadata (faster than 'full')
                    message = self.service.users().messages().get(
                        userId=self.user_id,
                        id=msg['id'],
                        format='metadata',
                        metadataHeaders=['From', 'Subject', 'Date']
                    ).execute()

                    msg_detail = self._parse_message_response(message)
                    if msg_detail:
                        detailed_messages.append(msg_detail)

                    if idx % 10 == 0:
                        print(f"Progress: {idx}/{len(all_messages)} emails fetched")

                    # Small delay every 10 requests to avoid rate limits
                    if idx % 10 == 0:
                        time.sleep(0.2)

                except HttpError as error:
                    if error.resp.status == 429:
                        print(f"Rate limit hit at email {idx}, waiting 2 seconds...")
                        time.sleep(2)
                        # Retry once
                        try:
                            message = self.service.users().messages().get(
                                userId=self.user_id,
                                id=msg['id'],
                                format='metadata',
                                metadataHeaders=['From', 'Subject', 'Date']
                            ).execute()
                            msg_detail = self._parse_message_response(message)
                            if msg_detail:
                                detailed_messages.append(msg_detail)
                        except:
                            print(f"Failed to fetch email {idx} after retry")
                    else:
                        print(f"Error fetching email {idx}: {error}")

            # Final progress update
            if self.progress_callback:
                self.progress_callback({
                    'progress': 100,
                    'current': len(detailed_messages),
                    'total': len(all_messages),
                    'status': 'Complete'
                })

            print(f"=== Scan complete: {len(detailed_messages)} emails fetched ===\n")
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

        # Fetch a reasonable multiplier to account for filtering
        # Use 1.5x instead of 3x to reduce API calls
        fetch_count = min(int(max_results * 1.5), max_results + 50)
        emails = self.search_emails(query, fetch_count)

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
        """Get Gmail statistics - only large emails"""
        try:
            # Only scan for large emails
            large_emails = self.scan_large_emails(max_results=50)

            total_size = sum(e['size'] for e in large_emails)

            return {
                'total_emails': len(large_emails),
                'total_size_mb': total_size / (1024 * 1024),
                'spam_count': 0,  # No longer scanning
                'large_emails_count': len(large_emails),
                'old_emails_count': 0  # No longer scanning
            }
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise
