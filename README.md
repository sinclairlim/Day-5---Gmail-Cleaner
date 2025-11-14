# Gmail Cleaner - AI-Powered Email Management

A professional-grade application that uses AI to help you clean and organize your Gmail inbox. Built with FastAPI, React, and LangChain.

## Features

- **Google OAuth Authentication** - Secure login with your Google account
- **Smart Email Scanning** - Find spam, large files, and old emails
- **AI Analysis** - LangChain-powered insights about your emails
- **Bulk Actions** - Select and delete multiple emails at once
- **Real-time Stats** - View your inbox statistics and storage usage
- **Beautiful UI** - Modern, responsive React interface

## Architecture

```
frontend/ (React + TypeScript + Vite)
    |
    | REST API calls
    |
backend/ (FastAPI + Python)
    |
    | Google OAuth + Gmail API
    |
Google Gmail API
    |
LangChain (OpenAI GPT-4)
```

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Google Gmail API** - Email access and management
- **Google OAuth 2.0** - Secure authentication
- **LangChain** - AI agent for email analysis
- **OpenAI GPT-4** - Natural language processing

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide React** - Icons

## Prerequisites

- Python 3.8+
- Node.js 18+
- Google Cloud Project with Gmail API enabled
- OpenAI API key

## Quick Start (10 Minutes)

**Want to test it quickly?** Follow the [QUICK_START.md](QUICK_START.md) guide!

```bash
# 1. Validate your setup
./test-setup.sh

# 2. Configure credentials (see QUICK_START.md)
cd backend && cp .env.example .env
# Edit .env with your Google OAuth and OpenAI credentials

# 3. Run backend (Terminal 1)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Run frontend (Terminal 2)
cd frontend
npm install
npm run dev

# 5. Open http://localhost:3000
```

**Detailed testing**: See [TESTING_GUIDE.md](TESTING_GUIDE.md)

## Setup Instructions

### 1. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Web application"
   - Add authorized redirect URI: `http://localhost:8000/api/auth/callback`
   - Download the credentials JSON

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your credentials:
# - GOOGLE_CLIENT_ID
# - GOOGLE_CLIENT_SECRET
# - OPENAI_API_KEY
# - SECRET_KEY (generate a random string)

# Run the server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Login**: Click "Sign in with Google" and authorize the application
2. **Scan**: Choose a scan type (spam/large/old/all) and click "Scan"
3. **Review**: Check the AI analysis and review the found emails
4. **Select**: Choose emails you want to delete
5. **Delete**: Click "Delete Selected" to move emails to trash

## Cost Analysis

### OpenAI API Costs (with GPT-4o-mini)

The app is optimized for cost-efficiency using **GPT-4o-mini** by default:

| Usage Pattern | Scans per Month | Estimated Monthly Cost |
|---------------|-----------------|------------------------|
| Light User | 10 scans | $0.01 - $0.03 |
| Regular User | 50 scans | $0.05 - $0.15 |
| Heavy User | 200 scans | $0.20 - $0.60 |

**Per scan cost**: ~$0.001 - $0.003 (less than a penny!)

### Model Options

You can configure different models in `.env`:

```env
OPENAI_MODEL=gpt-4o-mini  # Default (recommended)
# or
OPENAI_MODEL=gpt-3.5-turbo  # ~$0.002-0.005 per scan
# or
OPENAI_MODEL=gpt-4  # ~$0.03-0.08 per scan (premium quality)
```

**Why GPT-4o-mini?**
- 97% cheaper than GPT-4
- Excellent quality for email analysis
- Fast response times
- Perfect for production use

## API Endpoints

### Authentication
- `GET /api/auth/login` - Initiate OAuth flow
- `GET /api/auth/callback` - OAuth callback handler
- `GET /api/auth/status` - Check authentication status
- `POST /api/auth/logout` - Logout user

### Gmail Operations
- `GET /api/gmail/user-info` - Get user profile
- `POST /api/gmail/scan` - Scan emails
- `POST /api/gmail/delete` - Delete emails
- `GET /api/gmail/stats` - Get inbox statistics

## Security Features

- OAuth 2.0 authentication
- Secure credential storage
- Token refresh handling
- CORS protection
- Environment variable configuration

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Core configuration
│   ├── models/        # Pydantic models
│   └── services/      # Business logic
├── requirements.txt
└── .env.example

frontend/
├── src/
│   ├── components/    # React components
│   ├── pages/         # Page components
│   ├── services/      # API services
│   └── App.tsx
├── package.json
└── vite.config.ts
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### Backend (Railway/Render/DigitalOcean)

1. Update `.env` with production values
2. Set `ENVIRONMENT=production`
3. Update `CORS_ORIGINS` to your frontend URL
4. Deploy using your preferred platform

### Frontend (Vercel/Netlify)

1. Build the frontend: `npm run build`
2. Deploy the `dist` folder
3. Update backend CORS settings

## Environment Variables

### Backend (.env)
```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:8000/api/auth/callback
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

## Limitations

- Emails are moved to trash (not permanently deleted)
- OAuth session stored in memory (use database for production)
- Rate limits apply based on Gmail API quotas
- OpenAI API costs apply for analysis

## Future Enhancements

- [ ] Permanent deletion option
- [ ] Email scheduling
- [ ] Custom filters
- [ ] Export reports
- [ ] Email preview
- [ ] Undo deletion
- [ ] Database integration
- [ ] User sessions
- [ ] Advanced analytics

## License

MIT

## Contributing

Pull requests are welcome! Please read the contributing guidelines first.

## Support

For issues and questions, please open an issue on GitHub.

## Disclaimer

This application requires access to your Gmail account. We recommend:
- Reviewing the code before use
- Using a test Gmail account initially
- Understanding that deleted emails go to trash (recoverable for 30 days)
- Being aware of OpenAI API costs for analysis features
