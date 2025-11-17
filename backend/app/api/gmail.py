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
    """Scan the latest 500 emails and show top senders"""
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

        # SIMPLIFIED: Just fetch the latest emails (no filtering)
        # Use max_results from request, default to 500
        max_emails = scan_request.max_results or 500
        print(f"\n>>> Scanning latest {max_emails} emails <<<\n")

        emails = gmail_service.search_emails("", max_emails)

        # Analyze senders (this is just processing, no additional API calls)
        sender_analysis = gmail_service.analyze_senders(emails)

        # Calculate total size
        total_size_mb = sum(e['size'] for e in emails) / (1024 * 1024)

        # Create analysis message
        if emails:
            analysis = f"Scanned {len(emails)} latest emails totaling {total_size_mb:.2f} MB. Top senders shown below."
        else:
            analysis = "No emails found."

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
async def get_stats():
    """Get Gmail statistics - DISABLED to avoid automatic API calls"""
    # Return dummy data without making any Gmail API calls
    return StatsResponse(
        total_emails=0,
        total_size_mb=0.0,
        spam_count=0,
        large_emails_count=0,
        old_emails_count=0
    )
