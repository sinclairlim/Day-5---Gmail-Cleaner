# Gmail Cleaner - Complete Setup Guide

This guide will walk you through setting up the Gmail Cleaner application from scratch.

## Prerequisites

Before you begin, make sure you have:

- [x] Python 3.8 or higher installed
- [x] Node.js 18 or higher installed
- [x] A Google account
- [x] An OpenAI account with API access

## Step 1: Clone or Download the Project

```bash
cd Day-5---Gmail-Cleaner
```

## Step 2: Google Cloud Platform Setup

### 2.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Name it "Gmail Cleaner" and click "Create"

### 2.2 Enable Gmail API

1. In the left sidebar, go to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on it and press "Enable"

### 2.3 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in app name: "Gmail Cleaner"
   - Add your email as developer contact
   - Skip optional fields
   - Add scopes: `gmail.readonly` and `gmail.modify`
   - Add test users (your email)
4. Back to creating credentials:
   - Application type: "Web application"
   - Name: "Gmail Cleaner Web Client"
   - Authorized redirect URIs: `http://localhost:8000/api/auth/callback`
   - Click "Create"
5. Copy the Client ID and Client Secret (you'll need these)

## Step 3: OpenAI API Setup

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in or create an account
3. Go to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (you won't be able to see it again)

## Step 4: Backend Setup

### 4.1 Navigate to Backend Directory

```bash
cd backend
```

### 4.2 Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 4.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4.4 Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file with your actual credentials:

```env
GOOGLE_CLIENT_ID=your_client_id_from_google_cloud.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret_from_google_cloud
REDIRECT_URI=http://localhost:8000/api/auth/callback

OPENAI_API_KEY=sk-your_openai_api_key_here

SECRET_KEY=generate_a_random_string_here_use_any_random_string
CORS_ORIGINS=http://localhost:3000

ENVIRONMENT=development
```

To generate a secret key, you can use Python:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4.5 Test the Backend

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Visit `http://localhost:8000/docs` to see the API documentation.

Keep this terminal running!

## Step 5: Frontend Setup

Open a NEW terminal window/tab.

### 5.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 5.2 Install Dependencies

```bash
npm install
```

This may take a few minutes.

### 5.3 Run the Development Server

```bash
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
```

## Step 6: Test the Application

1. Open your browser to `http://localhost:3000`
2. You should see the Gmail Cleaner login page
3. Click "Sign in with Google"
4. You'll be redirected to Google's login page
5. Sign in with your Google account
6. Authorize the application (you may see a warning because the app is in development mode - this is normal)
7. You'll be redirected back to the dashboard

## Step 7: Use the Application

### Scan Emails

1. Select a scan type:
   - **Spam Emails** - Finds emails marked as spam or old unread emails
   - **Large Emails** - Finds emails with attachments over 5MB
   - **Old Emails** - Finds emails older than 1 year
   - **All Categories** - Combines all three scans

2. Click "Scan"
3. Wait for the AI analysis
4. Review the results

### Delete Emails

1. Select emails you want to delete by clicking on them
2. Or use "Select All" to select everything
3. Click "Delete Selected"
4. Confirm the deletion

Note: Emails are moved to trash, not permanently deleted. You can recover them from Gmail's trash for 30 days.

## Troubleshooting

### Backend Issues

**Error: "Not authenticated"**
- Make sure you've completed the OAuth flow
- Check that your Google OAuth credentials are correct
- Try logging out and logging in again

**Error: "Module not found"**
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

**Error: "Invalid credentials"**
- Check your `.env` file
- Make sure there are no extra spaces or quotes around values

### Frontend Issues

**Blank page or errors**
- Check the browser console (F12)
- Make sure the backend is running on port 8000
- Clear browser cache and reload

**OAuth redirect fails**
- Check that your redirect URI in Google Cloud Console matches exactly: `http://localhost:8000/api/auth/callback`
- Make sure you're using `http://localhost:3000` not `http://127.0.0.1:3000`

### General Issues

**CORS errors**
- Make sure `CORS_ORIGINS` in `.env` includes `http://localhost:3000`
- Restart the backend server after changing `.env`

**API rate limits**
- Gmail API has rate limits - if you hit them, wait a few minutes
- OpenAI API has usage limits based on your plan

## Production Deployment

For production deployment:

1. Update environment variables for production
2. Build the frontend: `npm run build`
3. Deploy backend to a server (Railway, Render, DigitalOcean)
4. Deploy frontend to static hosting (Vercel, Netlify)
5. Update Google OAuth redirect URIs with production URLs
6. Update CORS settings in backend

## Security Notes

- Never commit your `.env` file
- Use environment-specific credentials for production
- Consider implementing user sessions with a database
- Add rate limiting for production
- Set up proper logging and monitoring

## Need Help?

- Check the main README.md for more information
- Review the API documentation at `http://localhost:8000/docs`
- Open an issue on GitHub

## Next Steps

- Customize the UI to match your brand
- Add more scan filters
- Implement email preview
- Add export functionality
- Set up analytics
