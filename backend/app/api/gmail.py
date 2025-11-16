from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import (
    ScanRequest, ScanResult, DeleteRequest, DeleteResponse,
    StatsResponse, EmailMessage, UserInfo
)
from app.services.gmail_service import GmailService
from app.services.langchain_agent import EmailAnalysisAgent
from app.api.auth import get_credentials
from google.oauth2.credentials import Credentials
from typing import List, Dict, Any

router = APIRouter()

# In-memory progress storage (key: user email, value: progress data)
scan_progress: Dict[str, Dict[str, Any]] = {}


def get_gmail_service(credentials: Credentials = Depends(get_credentials)) -> GmailService:
    """Dependency to get Gmail service"""
    return GmailService(credentials)


@router.get("/user-info", response_model=UserInfo)
async def get_user_info(gmail_service: GmailService = Depends(get_gmail_service)):
    """Get user profile information"""
    try:
        user_info = gmail_service.get_user_info()
        # For a complete user info, you'd also call the People API
        return UserInfo(
            email=user_info['email'],
            name=user_info['email'].split('@')[0],  # Simplified
            picture=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scan", response_model=ScanResult)
async def scan_emails(
    scan_request: ScanRequest,
    gmail_service: GmailService = Depends(get_gmail_service),
    credentials: Credentials = Depends(get_credentials)
):
    """Scan emails based on criteria"""
    try:
        # Get user email for progress tracking
        user_info = gmail_service.get_user_info()
        user_email = user_info['email']

        # Initialize progress
        scan_progress[user_email] = {
            'progress': 0,
            'current': 0,
            'total': 0,
            'status': 'Starting scan...'
        }

        # Set up progress callback
        def update_progress(progress_data):
            scan_progress[user_email] = progress_data

        gmail_service.progress_callback = update_progress

        emails = []

        if scan_request.scan_type == "inbox":
            # Scan entire inbox (all emails)
            emails = gmail_service.search_emails("", scan_request.max_results)
        elif scan_request.scan_type == "spam":
            emails = gmail_service.scan_spam_emails(scan_request.max_results)
        elif scan_request.scan_type == "large":
            min_size = scan_request.min_size_mb or 5.0
            emails = gmail_service.scan_large_emails(min_size, scan_request.max_results)
        elif scan_request.scan_type == "old":
            days_old = scan_request.days_old or 365
            emails = gmail_service.scan_old_emails(days_old, scan_request.max_results)
        elif scan_request.scan_type == "all":
            spam = gmail_service.scan_spam_emails(scan_request.max_results // 3)
            large = gmail_service.scan_large_emails(5.0, scan_request.max_results // 3)
            old = gmail_service.scan_old_emails(365, scan_request.max_results // 3)
            emails = spam + large + old
        else:
            raise HTTPException(status_code=400, detail="Invalid scan type")

        # Sort emails by size in descending order
        emails.sort(key=lambda x: x['size'], reverse=True)

        # Analyze senders
        sender_analysis = gmail_service.analyze_senders(emails)

        # # Analyze with LangChain (DISABLED - focus on sender analysis)
        # agent = EmailAnalysisAgent()
        # analysis = agent.analyze_emails(emails, scan_request.scan_type)

        # Calculate total size
        total_size_mb = sum(e['size'] for e in emails) / (1024 * 1024)

        # Create analysis message with size breakdown
        if emails:
            largest_email_mb = emails[0]['size'] / (1024 * 1024)
            analysis = f"Found {len(emails)} emails totaling {total_size_mb:.2f} MB. Largest email: {largest_email_mb:.2f} MB. Sorted by size (largest first)."
        else:
            analysis = "No emails found matching the criteria."

        # Convert to EmailMessage objects
        email_messages = [EmailMessage(**e) for e in emails]

        return ScanResult(
            emails=email_messages,
            total_count=len(emails),
            total_size_mb=total_size_mb,
            analysis=analysis,
            sender_stats=sender_analysis[:50]  # Top 50 senders
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delete", response_model=DeleteResponse)
async def delete_emails(
    delete_request: DeleteRequest,
    gmail_service: GmailService = Depends(get_gmail_service)
):
    """Delete specified emails"""
    try:
        result = gmail_service.delete_emails(delete_request.email_ids)
        return DeleteResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scan-progress")
async def get_scan_progress(gmail_service: GmailService = Depends(get_gmail_service)):
    """Get current scan progress"""
    try:
        user_info = gmail_service.get_user_info()
        user_email = user_info['email']

        progress_data = scan_progress.get(user_email, {
            'progress': 0,
            'current': 0,
            'total': 0,
            'status': 'No scan in progress'
        })

        return progress_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_stats(gmail_service: GmailService = Depends(get_gmail_service)):
    """Get Gmail statistics"""
    try:
        stats = gmail_service.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
