# Gmail Cleaner Backend

FastAPI backend with Google OAuth, Gmail API integration, and LangChain AI analysis.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run server
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key Components

### Services
- **gmail_service.py** - Gmail API operations
- **langchain_agent.py** - AI email analysis

### API Routes
- **auth.py** - OAuth authentication
- **gmail.py** - Email operations

### Models
- **schemas.py** - Pydantic models for request/response

## Configuration

Edit `.env` file with your credentials:
- Google OAuth credentials from Google Cloud Console
- OpenAI API key for LangChain
- Secret key for session management

## Development

Run in development mode with auto-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production

For production deployment:
1. Set `ENVIRONMENT=production` in `.env`
2. Use a production WSGI server (gunicorn)
3. Set up proper credential storage (database)
4. Configure HTTPS
5. Set up monitoring and logging
