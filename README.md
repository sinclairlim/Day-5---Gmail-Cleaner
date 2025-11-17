# Gmail Cleaner

FastAPI + React app for cleaning Gmail: authenticate with Google, scan a chunk of your inbox, see the biggest senders, and bulk-delete straight to the trash.

## What it does now
- Google OAuth login with Gmail read/modify scopes
- Scans up to `max_results` recent messages (default 5000) and shows subject, size, labels, snippet, and sender
- Aggregates **Top Senders** so you can select/delete everything from a sender in one click
- Bulk delete moves messages to the Gmail trash (not permanent delete)
- Progress endpoint is available and polled during scans; the stats endpoint intentionally returns zeroed data to avoid background Gmail calls
- LangChain/OpenAI client is wired up for future AI analysis, but current scans only return metadata and sender totals (no AI token usage)

## Repo layout
- `backend/` — FastAPI, Gmail API client, OAuth flow
- `frontend/` — React + TypeScript (Vite), API service, login/dashboard UI
- `test-setup.sh` — optional sanity check for local tooling

## Requirements
- Python 3.8+
- Node.js 18+
- Google Cloud project with Gmail API enabled and an OAuth client
- OpenAI API key (required by backend settings even though AI analysis is not invoked by default)

## Configure environment
Create `backend/.env` from the template below (no committed example file):

```env
# OAuth / Gmail
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:8000/api/auth/callback
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/userinfo.profile,openid

# OpenAI (required by app settings; current flows don't call the model)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# App
SECRET_KEY=change_me
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

If your frontend is hosted somewhere else, include it in `CORS_ORIGINS` (comma-separated).

Frontend optionally honors `VITE_API_BASE` (e.g., `VITE_API_BASE=https://your-api.example.com/api`); otherwise it defaults to `http://localhost:8000/api`.

## Run locally

**Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and complete the Google sign-in. Use `backend/run.sh` and `frontend/run.sh` if you want a one-command start in each folder.

## Google OAuth setup
1. In [Google Cloud Console](https://console.cloud.google.com/), create/select a project.
2. Enable the **Gmail API**.
3. Create OAuth credentials: **Web application** type.
4. Add redirect URI: `http://localhost:8000/api/auth/callback`.
5. Copy the client ID/secret into `backend/.env` and add yourself as a test user if the consent screen is in testing mode.

## API snapshot
- `GET /api/auth/login` → returns the Google auth URL
- `GET /api/auth/callback` → handles OAuth redirect and stores credentials in-memory
- `GET /api/auth/status` / `POST /api/auth/logout`
- `GET /api/gmail/user-info` → current user's email profile
- `POST /api/gmail/scan` → body `{ scan_type, max_results, days_old?, min_size_mb? }` (currently just pulls the latest messages and aggregates senders)
- `GET /api/gmail/scan-progress` → current scan progress (per in-memory user)
- `POST /api/gmail/delete` → `{ email_ids: [] }` moves messages to trash
- `GET /api/gmail/stats` → returns zeroed stats by design to avoid extra Gmail calls

## Notes and limitations
- Credentials and scan progress are kept in-memory for the current user only; restart the backend to clear them. Use session storage/DB for multi-user or production scenarios.
- Deletions use the Gmail trash endpoint (recoverable from Gmail Trash).
- Large scans can take time because Gmail API calls are serialized; exponential backoff handles rate limits.
- The OpenAI client is initialized but unused in current flows; set a key to satisfy settings validation, but no tokens are consumed until you hook analysis back up.
