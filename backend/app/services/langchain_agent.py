from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from typing import List, Dict, Any
from app.core.config import settings


class EmailAnalysisAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,  # Configurable via .env (default: gpt-4o-mini)
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )

        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent email analysis assistant.
            Analyze the provided emails and give insights about:
            1. Common patterns (senders, subjects, types)
            2. Why these emails might be considered spam/large/old
            3. Recommendations for deletion
            4. Potential important emails that should be kept

            Be concise and actionable."""),
            ("user", "Analyze these emails:\n\n{emails_summary}")
        ])

        self.chain = self.analysis_prompt | self.llm | StrOutputParser()

    def analyze_emails(self, emails: List[Dict[str, Any]], scan_type: str) -> str:
        """Analyze a list of emails and provide insights"""
        if not emails:
            return f"No {scan_type} emails found. Your inbox looks clean!"

        # Create a summary of emails for the LLM
        emails_summary = self._create_email_summary(emails, scan_type)

        try:
            analysis = self.chain.invoke({
                "emails_summary": emails_summary
            })
            return analysis
        except Exception as e:
            return f"Analysis failed: {str(e)}"

    def _create_email_summary(self, emails: List[Dict[str, Any]], scan_type: str) -> str:
        """Create a concise summary of emails for analysis"""
        summary_parts = [
            f"Scan Type: {scan_type}",
            f"Total Emails: {len(emails)}",
            f"Total Size: {sum(e['size'] for e in emails) / (1024*1024):.2f} MB",
            "\nSample Emails:"
        ]

        # Include up to 10 sample emails
        for i, email in enumerate(emails[:10], 1):
            size_mb = email['size'] / (1024 * 1024)
            summary_parts.append(
                f"\n{i}. Subject: {email['subject'][:50]}"
                f"\n   From: {email['sender'][:50]}"
                f"\n   Date: {email['date']}"
                f"\n   Size: {size_mb:.2f} MB"
                f"\n   Labels: {', '.join(email['labels'][:3])}"
            )

        if len(emails) > 10:
            summary_parts.append(f"\n... and {len(emails) - 10} more emails")

        return "\n".join(summary_parts)

    def should_delete_email(self, email: Dict[str, Any]) -> tuple[bool, str]:
        """Use AI to determine if an email should be deleted"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an email filtering assistant.
            Determine if this email should be deleted based on:
            - Whether it's spam
            - Whether it's promotional
            - Whether it's outdated
            - Whether it has any value

            Respond with 'DELETE' or 'KEEP' followed by a brief reason."""),
            ("user", """Email Details:
            Subject: {subject}
            From: {sender}
            Date: {date}
            Snippet: {snippet}
            Labels: {labels}""")
        ])

        chain = prompt | self.llm | StrOutputParser()

        try:
            result = chain.invoke({
                "subject": email['subject'],
                "sender": email['sender'],
                "date": email['date'],
                "snippet": email['snippet'],
                "labels": ', '.join(email['labels'])
            })

            should_delete = result.upper().startswith('DELETE')
            reason = result.split('\n')[0]

            return should_delete, reason
        except Exception as e:
            return False, f"Analysis failed: {str(e)}"
