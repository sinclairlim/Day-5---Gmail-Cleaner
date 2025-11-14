from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from app.core.config import settings
import json

router = APIRouter()

# Store credentials temporarily (in production, use a proper session store or database)
credentials_store = {}


def create_flow():
    """Create OAuth flow"""
    return Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.REDIRECT_URI],
            }
        },
        scopes=settings.GMAIL_SCOPES,
        redirect_uri=settings.REDIRECT_URI
    )


@router.get("/login")
async def login():
    """Initiate OAuth flow"""
    flow = create_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    return JSONResponse({
        "auth_url": authorization_url,
        "state": state
    })


@router.get("/callback")
async def callback(request: Request):
    """Handle OAuth callback"""
    try:
        flow = create_flow()
        flow.fetch_token(code=request.query_params.get('code'))

        credentials = flow.credentials

        # Store credentials (use user ID in production)
        user_id = "current_user"  # Replace with actual user management
        credentials_store[user_id] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        # Redirect to frontend with success
        frontend_url = settings.cors_origins_list[0]
        return RedirectResponse(url=f"{frontend_url}/auth/success")

    except Exception as e:
        print(f"OAuth callback error: {e}")
        frontend_url = settings.cors_origins_list[0]
        return RedirectResponse(url=f"{frontend_url}/auth/error")


@router.get("/status")
async def auth_status():
    """Check if user is authenticated"""
    user_id = "current_user"
    is_authenticated = user_id in credentials_store

    return JSONResponse({
        "authenticated": is_authenticated
    })


@router.post("/logout")
async def logout():
    """Clear user credentials"""
    user_id = "current_user"
    if user_id in credentials_store:
        del credentials_store[user_id]

    return JSONResponse({
        "message": "Logged out successfully"
    })


def get_credentials() -> Credentials:
    """Get current user credentials"""
    user_id = "current_user"

    if user_id not in credentials_store:
        raise HTTPException(status_code=401, detail="Not authenticated")

    creds_data = credentials_store[user_id]
    credentials = Credentials(
        token=creds_data['token'],
        refresh_token=creds_data['refresh_token'],
        token_uri=creds_data['token_uri'],
        client_id=creds_data['client_id'],
        client_secret=creds_data['client_secret'],
        scopes=creds_data['scopes']
    )

    # Refresh token if expired
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(GoogleRequest())
        # Update stored credentials
        credentials_store[user_id]['token'] = credentials.token

    return credentials
