from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any
from datetime import datetime, timedelta
import base64
import email


class GmailService:
    def __init__(self, credentials: Credentials):
        self.service = build('gmail', 'v1', credentials=credentials)
        self.user_id = 'me'

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
        """Search emails based on Gmail query syntax"""
        try:
            results = self.service.users().messages().list(
                userId=self.user_id,
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            detailed_messages = []

            for message in messages:
                msg_detail = self.get_message_details(message['id'])
                if msg_detail:
                    detailed_messages.append(msg_detail)

            return detailed_messages
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise

    def get_message_details(self, message_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific email"""
        try:
            message = self.service.users().messages().get(
                userId=self.user_id,
                id=message_id,
                format='full'
            ).execute()

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
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def scan_spam_emails(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """Find potential spam emails"""
        query = "label:spam OR (is:unread older_than:30d)"
        return self.search_emails(query, max_results)

    def scan_large_emails(self, min_size_mb: float = 5.0, max_results: int = 100) -> List[Dict[str, Any]]:
        """Find large emails"""
        # Gmail doesn't support size queries directly, so we search and filter
        query = "has:attachment"
        emails = self.search_emails(query, max_results * 2)

        min_size_bytes = min_size_mb * 1024 * 1024
        return [e for e in emails if e['size'] >= min_size_bytes][:max_results]

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
