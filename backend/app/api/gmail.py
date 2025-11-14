from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import (
    ScanRequest, ScanResult, DeleteRequest, DeleteResponse,
    StatsResponse, EmailMessage, UserInfo
)
from app.services.gmail_service import GmailService
from app.services.langchain_agent import EmailAnalysisAgent
from app.api.auth import get_credentials
from google.oauth2.credentials import Credentials
from typing import List

router = APIRouter()


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
    gmail_service: GmailService = Depends(get_gmail_service)
):
    """Scan emails based on criteria"""
    try:
        emails = []

        if scan_request.scan_type == "spam":
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

        # Analyze with LangChain
        agent = EmailAnalysisAgent()
        analysis = agent.analyze_emails(emails, scan_request.scan_type)

        # Calculate total size
        total_size_mb = sum(e['size'] for e in emails) / (1024 * 1024)

        # Convert to EmailMessage objects
        email_messages = [EmailMessage(**e) for e in emails]

        return ScanResult(
            emails=email_messages,
            total_count=len(emails),
            total_size_mb=total_size_mb,
            analysis=analysis
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


@router.get("/stats", response_model=StatsResponse)
async def get_stats(gmail_service: GmailService = Depends(get_gmail_service)):
    """Get Gmail statistics"""
    try:
        stats = gmail_service.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
