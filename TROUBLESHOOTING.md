# Troubleshooting Guide

Quick solutions to common issues when testing Gmail Cleaner.

## Setup Issues

### ✗ Python not found
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# Windows
# Download from https://python.org
```

### ✗ Node.js not found
```bash
# macOS
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Windows
# Download from https://nodejs.org
```

### ✗ backend/.env not found
```bash
cd backend
cp .env.example .env
# Then edit .env with your credentials
```

## Backend Issues

### ModuleNotFoundError
```bash
# Activate virtual environment first!
cd backend
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Then install
pip install -r requirements.txt
```

### ValidationError for config
```bash
# Check your .env file has all required values
cat backend/.env

# Required fields:
# GOOGLE_CLIENT_ID
# GOOGLE_CLIENT_SECRET
# OPENAI_API_KEY
# SECRET_KEY
```

### Port 8000 already in use
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
# Then update CORS_ORIGINS and frontend API calls
```

### OpenAI API errors

**"Invalid API key"**
- Check your key starts with `sk-`
- No spaces before/after in .env
- Get a new key: https://platform.openai.com/api-keys

**"Insufficient quota"**
- Check usage: https://platform.openai.com/usage
- Add payment method or get free credits
- Try switching to `gpt-3.5-turbo` temporarily

**"Model not found"**
```bash
# In backend/.env, use a supported model:
OPENAI_MODEL=gpt-4o-mini
# or
OPENAI_MODEL=gpt-3.5-turbo
```

## Frontend Issues

### npm install fails
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Port 3000 already in use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or Vite will automatically use 3001
```

### Blank page
1. Check browser console (F12)
2. Verify backend is running: http://localhost:8000/docs
3. Check CORS settings in backend/.env
4. Clear browser cache (Cmd+Shift+R or Ctrl+Shift+R)

### API calls failing
```bash
# Check backend is running
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

## Google OAuth Issues

### "redirect_uri_mismatch"
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to "Credentials"
3. Edit your OAuth client
4. Make sure redirect URI is EXACTLY:
   ```
   http://localhost:8000/api/auth/callback
   ```
   (No trailing slash, use `localhost` not `127.0.0.1`)

### "Access blocked: This app's request is invalid"
**The app is in testing mode and you're not a test user:**
1. Go to OAuth consent screen
2. Add your email under "Test users"
3. Try logging in again

### "This app hasn't been verified"
**This is NORMAL for development apps!**
1. Click "Advanced"
2. Click "Go to Gmail Cleaner (unsafe)"
3. Review permissions and continue

This warning only appears during development. Published apps don't show this.

### OAuth loop (keeps redirecting)
```bash
# Clear browser cookies for localhost
# Chrome: F12 → Application → Cookies → Delete all

# Restart both servers
# Backend: Ctrl+C then restart
# Frontend: Ctrl+C then restart
```

### "Not authenticated" errors
1. Complete OAuth flow: http://localhost:3000
2. Check browser cookies are enabled
3. Clear application data and re-login
4. Restart backend server

## Email Scanning Issues

### No emails found (when you expect some)
**For spam scan:**
- Gmail might not have any spam
- Try "Old Emails" instead

**For large emails:**
- Default is 5MB+
- You may not have large attachments
- Try lowering the threshold in the code

**For old emails:**
- Default is 365+ days
- Adjust `days_old` parameter

### Scan takes too long
- Large scans (500+ emails) can take 20-30 seconds
- Gmail API has rate limits
- AI analysis adds 3-5 seconds
- Consider reducing `max_results`

### "Quota exceeded" errors
**Gmail API quota:**
- Free tier: 1 billion quota units/day
- Each scan uses ~100-500 units
- You have plenty of quota!
- If you hit it, wait 24 hours

**OpenAI quota:**
- Check: https://platform.openai.com/usage
- Add payment method if needed
- Free tier gives $5 credit

## Deletion Issues

### Emails not deleting
- App moves to trash (not permanent delete)
- Check Gmail trash to verify
- May take a few seconds to reflect

### Some emails failed to delete
- Check the error message
- Some emails may be protected
- System labels can't be modified

### Deleted wrong emails
**Don't panic! They're in trash:**
1. Go to Gmail
2. Click "Trash"
3. Select emails
4. Click "Move to inbox"
5. Emails are recovered!

Trash keeps emails for 30 days.

## Development Issues

### Changes not reflecting

**Backend changes:**
```bash
# Make sure --reload flag is used
uvicorn app.main:app --reload
```

**Frontend changes:**
```bash
# Vite should auto-reload
# If not, restart dev server
npm run dev
```

### Import errors
```bash
# Backend - activate venv!
source venv/bin/activate

# Frontend - reinstall
npm install
```

## Browser Issues

### CORS errors in console
```bash
# Check backend/.env
CORS_ORIGINS=http://localhost:3000

# Restart backend after changing
```

### Cookies not working
- Use `localhost` not `127.0.0.1`
- Check browser settings allow cookies
- Try incognito/private mode
- Clear all localhost cookies

### Console errors
Common safe errors to ignore:
- "Download the React DevTools..." (just a suggestion)
- Favicon 404 (doesn't affect functionality)

## Network Issues

### Can't reach backend
```bash
# Check backend is running
curl http://localhost:8000

# Should return: {"message":"Gmail Cleaner API",...}

# Check firewall isn't blocking
```

### SSL/Certificate errors
- Use `http://` not `https://` for local development
- Check redirect URIs use `http://localhost`

## Performance Issues

### Slow scans
- Normal: 5-10 seconds for 100 emails
- AI analysis adds time
- Large email lists take longer
- Gmail API rate limits apply

### High memory usage
- Normal for AI processing
- Close other apps if needed
- Reduce `max_results` if very slow

## Getting More Help

### Check logs

**Backend logs:**
```bash
# Terminal running uvicorn shows all API requests/errors
```

**Frontend logs:**
```bash
# Browser console (F12) shows errors
# Network tab shows API calls
```

### Verify setup
```bash
./test-setup.sh
```

### Still stuck?

1. Read error message carefully
2. Check relevant section above
3. See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed setup
4. See [SETUP_GUIDE.md](SETUP_GUIDE.md) for configuration
5. Check API docs: http://localhost:8000/docs

### Common error patterns

**"Cannot find module"** → Install dependencies
**"Permission denied"** → Check file permissions or use `chmod`
**"Address already in use"** → Port is busy, kill process
**"Invalid credentials"** → Check .env file
**"CORS error"** → Backend CORS_ORIGINS setting
**"Not authenticated"** → Complete OAuth flow

## Prevention Tips

✅ Always activate virtual environment before running backend
✅ Use `localhost` not `127.0.0.1`
✅ Keep terminals running while testing
✅ Check .env file has no extra spaces
✅ Restart servers after config changes
✅ Test with small scans first (10-20 emails)
✅ Clear browser cache if UI looks broken

## Quick Commands

```bash
# Check setup
./test-setup.sh

# Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Start frontend
cd frontend && npm run dev

# Check backend health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs

# Kill port 8000
lsof -ti:8000 | xargs kill -9

# Kill port 3000
lsof -ti:3000 | xargs kill -9

# Reset everything
rm -rf backend/venv frontend/node_modules
cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd ../frontend && npm install
```
