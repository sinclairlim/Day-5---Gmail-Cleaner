# Quick Start Guide - Test in 10 Minutes

Follow these steps to test the Gmail Cleaner app quickly.

## Before You Start

You'll need:
1. **Google Cloud OAuth credentials** ([Get them here](https://console.cloud.google.com))
2. **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))

## Step 1: Check Prerequisites (1 min)

Run the setup validator:

```bash
./test-setup.sh
```

This will check if you have Python, Node.js, and all requirements.

## Step 2: Configure Credentials (3 min)

### 2.1 Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Add redirect URI: `http://localhost:8000/api/auth/callback`
6. Copy your Client ID and Client Secret

**Detailed instructions**: See [TESTING_GUIDE.md](TESTING_GUIDE.md#step-1-set-up-google-oauth-one-time-setup)

### 2.2 Get OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new key
3. Copy it immediately

### 2.3 Configure Backend

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and replace:
- `GOOGLE_CLIENT_ID=...` with your Client ID
- `GOOGLE_CLIENT_SECRET=...` with your Client Secret
- `OPENAI_API_KEY=...` with your OpenAI key

## Step 3: Install Backend (2 min)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Install Frontend (2 min)

Open a NEW terminal:

```bash
cd frontend

# Install dependencies
npm install
```

## Step 5: Run the App (2 min)

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # if not already activated
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

You should see:
```
➜  Local:   http://localhost:3000/
```

## Step 6: Test It! (2 min)

1. **Open**: http://localhost:3000
2. **Click**: "Sign in with Google"
3. **Authorize**: The app (you may see a warning - this is normal for development)
4. **Scan**: Choose "Spam Emails" and click "Scan"
5. **Review**: Check the AI analysis and results
6. **Select**: Click some emails
7. **Delete** (optional): Test deletion with spam emails

## Troubleshooting

### Backend won't start
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Check .env file exists
ls backend/.env

# Verify credentials are set
cat backend/.env
```

### Frontend won't start
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
```

### OAuth errors
- Verify redirect URI is exactly: `http://localhost:8000/api/auth/callback`
- Add your email as a test user in Google Cloud Console
- Use `localhost` not `127.0.0.1`

### "Not authenticated" errors
- Complete the Google OAuth flow
- Check browser console (F12) for errors
- Restart both servers

## What to Test

✅ **Login** - OAuth flow works
✅ **Scan** - Different scan types (spam, large, old, all)
✅ **AI Analysis** - LangChain insights appear
✅ **Selection** - Can select/deselect emails
✅ **Deletion** - Can delete emails (they go to trash)
✅ **Stats** - Dashboard shows statistics

## Cost Check

After 10-20 scans, check your OpenAI usage:
- Go to: https://platform.openai.com/usage
- Should be < $0.01 with gpt-4o-mini

## Next Steps

- ✅ App works? **Customize it!** Edit UI, add features
- ✅ Ready for production? See **deployment** section in [README.md](README.md)
- ❌ Issues? Check **[TESTING_GUIDE.md](TESTING_GUIDE.md)** for detailed help

## Quick Commands Reference

```bash
# Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Start frontend
cd frontend && npm run dev

# Stop servers
Ctrl+C in each terminal

# Check setup
./test-setup.sh
```

## Support

- **Detailed testing**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Setup help**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Costs**: [COST_ANALYSIS.md](COST_ANALYSIS.md)
- **API docs**: http://localhost:8000/docs (when backend is running)

Happy testing! 🚀
