# Gmail Cleaner - Testing Guide

This guide will help you test the Gmail Cleaner application locally.

## Prerequisites Checklist

Before testing, make sure you have:

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Google Cloud OAuth credentials (Client ID & Secret)
- [ ] OpenAI API key

## Quick Test (5 Minutes)

If you just want to see if everything works:

```bash
# Terminal 1 - Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file (see below)
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser.

## Step-by-Step Testing Guide

### Step 1: Set Up Google OAuth (One-Time Setup)

#### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown → "New Project"
3. Name: "Gmail Cleaner Test"
4. Click "Create"

#### 1.2 Enable Gmail API

1. In your new project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click it and press "Enable"

#### 1.3 Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" → Click "Create"
3. Fill in:
   - App name: `Gmail Cleaner Test`
   - User support email: Your email
   - Developer contact: Your email
4. Click "Save and Continue"
5. On "Scopes" screen, click "Add or Remove Scopes":
   - Add `gmail.readonly`
   - Add `gmail.modify`
   - Click "Update" → "Save and Continue"
6. On "Test users" screen, click "Add Users":
   - Add YOUR Gmail address (the one you'll test with)
   - Click "Save and Continue"
7. Click "Back to Dashboard"

#### 1.4 Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Web application"
4. Name: "Gmail Cleaner Local"
5. Authorized redirect URIs:
   - Click "Add URI"
   - Enter: `http://localhost:8000/api/auth/callback`
   - Click "Create"
6. **SAVE** the Client ID and Client Secret that appear

### Step 2: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create account
3. Click "Create new secret key"
4. Name it "Gmail Cleaner Test"
5. **COPY** the key immediately (you can't see it again)

### Step 3: Configure Backend

#### 3.1 Navigate to Backend

```bash
cd backend
```

#### 3.2 Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3.4 Create .env File

```bash
cp .env.example .env
```

#### 3.5 Edit .env File

Open `backend/.env` in your editor and fill in:

```env
# Google OAuth Credentials (from Step 1.4)
GOOGLE_CLIENT_ID=your_actual_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_actual_client_secret_here
REDIRECT_URI=http://localhost:8000/api/auth/callback

# OpenAI API Key (from Step 2)
OPENAI_API_KEY=sk-your_actual_openai_key_here

# OpenAI Model (leave as default)
OPENAI_MODEL=gpt-4o-mini

# Backend Settings
SECRET_KEY=test_secret_key_12345_replace_in_production
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Environment
ENVIRONMENT=development
```

**Important**: Replace the placeholder values with your actual credentials!

#### 3.6 Test Backend

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### 3.7 Verify Backend

Open a browser to: `http://localhost:8000/docs`

You should see the FastAPI Swagger documentation with all endpoints.

**Keep this terminal running!**

### Step 4: Configure Frontend

Open a **NEW terminal** (keep backend running).

#### 4.1 Navigate to Frontend

```bash
cd frontend
```

#### 4.2 Install Dependencies

```bash
npm install
```

This will take 1-2 minutes.

#### 4.3 Run Frontend

```bash
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
```

### Step 5: Test the Application

#### 5.1 Open Application

Open your browser to: `http://localhost:3000`

You should see the Gmail Cleaner login page.

#### 5.2 Sign In

1. Click "Sign in with Google"
2. You'll be redirected to Google
3. Select your Google account (must be a test user you added)
4. You may see a warning: "Google hasn't verified this app"
   - This is **NORMAL** for development
   - Click "Advanced" → "Go to Gmail Cleaner Test (unsafe)"
5. Review permissions and click "Continue"
6. You'll be redirected back to the dashboard

#### 5.3 Test Scanning

1. Select a scan type (try "Spam Emails" first)
2. Leave max results at 100
3. Click "Scan"
4. Wait 5-10 seconds

You should see:
- AI Analysis panel with insights
- List of emails found
- Total count and size

#### 5.4 Test Selection

1. Click on some emails to select them
2. Try "Select All" button
3. Try "Deselect All" button

#### 5.5 Test Deletion (Optional)

**Warning**: This will move emails to trash (recoverable for 30 days)

1. Select a few test emails (ideally spam)
2. Click "Delete Selected"
3. Confirm the deletion
4. Emails should disappear from the list
5. Check your Gmail trash to verify

#### 5.6 Test Different Scan Types

Try each scan type:
- **Spam Emails**: Finds spam and old unread emails
- **Large Emails**: Finds emails with attachments > 5MB
- **Old Emails**: Finds emails older than 1 year
- **All Categories**: Combines all three

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Problem**: `Error loading .env file` or `ValidationError`
```bash
# Check that .env file exists
ls backend/.env

# Verify all required fields are filled in
cat backend/.env
```

**Problem**: `401 Unauthorized` errors
- Check that `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are correct
- Make sure there are no extra spaces in .env file
- Verify redirect URI matches exactly: `http://localhost:8000/api/auth/callback`

**Problem**: OpenAI errors
- Verify `OPENAI_API_KEY` starts with `sk-`
- Check you have credits: https://platform.openai.com/usage
- Try switching to `gpt-3.5-turbo` if `gpt-4o-mini` fails

### Frontend Issues

**Problem**: Page is blank
- Check browser console (F12) for errors
- Verify backend is running on port 8000
- Make sure `CORS_ORIGINS` includes `http://localhost:3000`

**Problem**: OAuth redirect fails
- Check redirect URI in Google Cloud Console
- Must be exactly: `http://localhost:8000/api/auth/callback`
- Use `localhost` not `127.0.0.1`

**Problem**: "Not authenticated" errors
- Complete the OAuth flow again
- Clear browser cookies
- Restart both servers

### Google OAuth Issues

**Problem**: "Access blocked: Gmail Cleaner has not completed the Google verification process"
- Go to OAuth consent screen
- Add your email as a test user
- Make sure app is in "Testing" mode (not "Published")

**Problem**: "redirect_uri_mismatch"
- Check Google Cloud Console → Credentials
- Verify redirect URI is: `http://localhost:8000/api/auth/callback`
- No trailing slash!

## Testing Checklist

After setup, verify:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can access API docs at http://localhost:8000/docs
- [ ] Can see login page
- [ ] Can complete Google OAuth flow
- [ ] Can see dashboard after login
- [ ] Can scan for spam emails
- [ ] AI analysis appears
- [ ] Can select emails
- [ ] Can delete emails (optional)
- [ ] Can try different scan types
- [ ] Can logout

## Testing Different Scenarios

### Test 1: Empty Results
If your inbox is already clean:
- Try different scan types
- You should see: "No {type} emails found. Your inbox looks clean!"

### Test 2: Large Scans
- Increase max results to 500
- Test performance with large datasets

### Test 3: Model Switching
Edit `backend/.env`:
```env
OPENAI_MODEL=gpt-3.5-turbo  # Try different model
```
Restart backend and compare analysis quality.

### Test 4: Error Handling
- Try scanning without internet
- Try with invalid OpenAI key
- Verify error messages are user-friendly

## Performance Testing

### Check API Response Times

Open browser DevTools → Network tab:
- Scan request should complete in 3-10 seconds
- Most time is AI analysis
- Delete requests should be < 2 seconds per email

### Monitor Costs

After testing, check OpenAI usage:
1. Go to https://platform.openai.com/usage
2. View today's usage
3. Should see minimal cost (< $0.01 for 10-20 scans)

## Sample Test Data

If you want to create test emails:
1. Send yourself some large emails with attachments
2. Mark some emails as spam
3. Have some old emails (or change date filters)

## Next Steps After Testing

Once everything works:

1. **Customize** - Modify UI, add features
2. **Deploy** - Follow deployment guide in README
3. **Production** - Use production OAuth credentials
4. **Monitor** - Set up logging and analytics

## Getting Help

If you encounter issues:

1. Check the error message carefully
2. Review this guide's troubleshooting section
3. Check backend logs (terminal running uvicorn)
4. Check frontend console (F12 in browser)
5. Verify all environment variables are set correctly
6. Try restarting both servers

## Clean Up After Testing

To stop the application:

```bash
# In backend terminal: Ctrl+C
# In frontend terminal: Ctrl+C

# Deactivate virtual environment
deactivate
```

Your emails are safe - deleted items go to trash and can be recovered for 30 days!
