# Google OAuth Setup - Step by Step

Follow these steps to get your Google OAuth credentials (5 minutes).

## Step 1: Go to Google Cloud Console

1. Open: https://console.cloud.google.com
2. Sign in with your Google account

## Step 2: Create a New Project

1. Click the **project dropdown** at the top (next to "Google Cloud")
2. Click **"New Project"** in the top right
3. Project name: `Gmail Cleaner` (or any name you like)
4. Click **"Create"**
5. Wait 10-20 seconds for project creation
6. Click **"Select Project"** when it appears

## Step 3: Enable Gmail API

1. In the left sidebar, go to **"APIs & Services"** → **"Library"**
   - Or use the search bar at top and search "APIs Library"
2. Search for: `Gmail API`
3. Click on **"Gmail API"**
4. Click **"Enable"**
5. Wait for it to enable (~5 seconds)

## Step 4: Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"** (left sidebar)
2. Choose **"External"** user type
3. Click **"Create"**

### Fill in App Information:
- **App name:** `Gmail Cleaner`
- **User support email:** (your email - select from dropdown)
- **Developer contact information:** (your email)
- Leave everything else blank/default
- Click **"Save and Continue"**

### Scopes Screen:
- Click **"Add or Remove Scopes"**
- In the filter box, search: `gmail`
- Check these boxes:
  - ✅ `.../auth/gmail.readonly` - "View your email messages and settings"
  - ✅ `.../auth/gmail.modify` - "Manage your email"
- Scroll down and search: `userinfo`
- Check:
  - ✅ `userinfo.email` - "See your primary Google Account email address"
  - ✅ `userinfo.profile` - "See your personal info"
- Click **"Update"**
- Click **"Save and Continue"**

### Test Users Screen:
- Click **"Add Users"**
- Enter YOUR email address (the one you'll test with)
- Click **"Add"**
- Click **"Save and Continue"**

### Summary Screen:
- Review and click **"Back to Dashboard"**

## Step 5: Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"** (left sidebar)
2. Click **"Create Credentials"** (top of page)
3. Select **"OAuth client ID"**

### Configure OAuth Client:
- **Application type:** Select **"Web application"**
- **Name:** `Gmail Cleaner Local` (or any name)

### Authorized JavaScript origins:
- Click **"Add URI"**
- Enter: `http://localhost:3000`
- Click **"Add URI"** again
- Enter: `http://localhost:8000`

### Authorized redirect URIs:
- Click **"Add URI"**
- Enter EXACTLY: `http://localhost:8000/api/auth/callback`
- ⚠️ **Important:** No trailing slash, use `localhost` not `127.0.0.1`

4. Click **"Create"**

## Step 6: Copy Your Credentials

A popup will appear with:
- **Your Client ID** (looks like: `123456789-abc123.apps.googleusercontent.com`)
- **Your Client Secret** (looks like: `GOCSPX-abc123xyz`)

### Save These!
1. Click the **copy icon** next to Client ID → paste somewhere safe
2. Click the **copy icon** next to Client Secret → paste somewhere safe
3. Click **"OK"**

**Don't worry if you close the popup - you can always view them again in the Credentials page!**

## Step 7: Add to Your .env File

1. Open: `backend/.env` in your code editor
2. Add these lines (replace with your actual values):

```env
GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_client_secret_here
```

3. Save the file

## Step 8: Restart Your Backend

In your terminal running the backend:
1. Press **Ctrl+C** to stop it
2. Run again: `source venv/bin/activate && python -m uvicorn app.main:app --reload`

## Done! ✅

Your app is now ready to use Google OAuth!

---

## Troubleshooting

**Can't find "APIs & Services"?**
- Click the hamburger menu (☰) in top left
- Look for "APIs & Services"

**"Gmail API" not found?**
- Make sure you selected your project at the top
- Try refreshing the page

**Lost your credentials?**
- Go to "APIs & Services" → "Credentials"
- Your OAuth client will be listed
- Click on it to view Client ID and Secret

**Error: "redirect_uri_mismatch"?**
- Check you entered EXACTLY: `http://localhost:8000/api/auth/callback`
- No trailing slash
- Use `localhost` not `127.0.0.1`

---

## Quick Reference

- **Google Cloud Console:** https://console.cloud.google.com
- **Your project:** Check top of page (project dropdown)
- **Credentials location:** APIs & Services → Credentials
- **Redirect URI:** `http://localhost:8000/api/auth/callback`
