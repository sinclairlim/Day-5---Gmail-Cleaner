from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserInfo(BaseModel):
    email: EmailStr
    name: str
    picture: Optional[str] = None


class EmailMessage(BaseModel):
    id: str
    thread_id: str
    subject: str
    sender: str
    date: datetime
    size: int
    labels: List[str]
    snippet: str


class ScanRequest(BaseModel):
    scan_type: str  # "spam", "large", "old", "all"
    max_results: int = 100
    days_old: Optional[int] = None  # For "old" type
    min_size_mb: Optional[float] = None  # For "large" type


class ScanResult(BaseModel):
    emails: List[EmailMessage]
    total_count: int
    total_size_mb: float
    analysis: str  # LangChain agent analysis


class DeleteRequest(BaseModel):
    email_ids: List[str]


class DeleteResponse(BaseModel):
    deleted_count: int
    failed_ids: List[str]
    message: str


class StatsResponse(BaseModel):
    total_emails: int
    total_size_mb: float
    spam_count: int
    large_emails_count: int
    old_emails_count: int
