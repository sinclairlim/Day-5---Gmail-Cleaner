#!/bin/bash

echo "========================================="
echo "Gmail Cleaner - Test Setup Validator"
echo "========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ALL_GOOD=true

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found. Please install Python 3.8+"
    ALL_GOOD=false
fi
echo ""

# Check Node.js
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js found: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found. Please install Node.js 18+"
    ALL_GOOD=false
fi
echo ""

# Check npm
echo "Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} npm found: $NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm not found. Please install Node.js"
    ALL_GOOD=false
fi
echo ""

# Check backend .env
echo "Checking backend configuration..."
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} backend/.env file exists"

    # Check for required variables
    if grep -q "GOOGLE_CLIENT_ID=your_google_client_id_here" backend/.env; then
        echo -e "${YELLOW}⚠${NC}  GOOGLE_CLIENT_ID not configured (still using placeholder)"
        ALL_GOOD=false
    else
        echo -e "${GREEN}✓${NC} GOOGLE_CLIENT_ID is set"
    fi

    if grep -q "GOOGLE_CLIENT_SECRET=your_google_client_secret_here" backend/.env; then
        echo -e "${YELLOW}⚠${NC}  GOOGLE_CLIENT_SECRET not configured (still using placeholder)"
        ALL_GOOD=false
    else
        echo -e "${GREEN}✓${NC} GOOGLE_CLIENT_SECRET is set"
    fi

    if grep -q "OPENAI_API_KEY=your_openai_api_key_here" backend/.env; then
        echo -e "${YELLOW}⚠${NC}  OPENAI_API_KEY not configured (still using placeholder)"
        ALL_GOOD=false
    elif grep -q "OPENAI_API_KEY=sk-" backend/.env; then
        echo -e "${GREEN}✓${NC} OPENAI_API_KEY is set"
    else
        echo -e "${YELLOW}⚠${NC}  OPENAI_API_KEY format looks incorrect (should start with sk-)"
        ALL_GOOD=false
    fi
else
    echo -e "${RED}✗${NC} backend/.env file not found"
    echo "   Run: cp backend/.env.example backend/.env"
    echo "   Then edit it with your credentials"
    ALL_GOOD=false
fi
echo ""

# Check if backend dependencies are installed
echo "Checking backend dependencies..."
if [ -d "backend/venv" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment exists"
else
    echo -e "${YELLOW}⚠${NC}  Virtual environment not found"
    echo "   Run: cd backend && python3 -m venv venv"
fi
echo ""

# Check if frontend dependencies are installed
echo "Checking frontend dependencies..."
if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✓${NC} Frontend dependencies installed"
else
    echo -e "${YELLOW}⚠${NC}  Frontend dependencies not installed"
    echo "   Run: cd frontend && npm install"
fi
echo ""

# Summary
echo "========================================="
if [ "$ALL_GOOD" = true ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    echo ""
    echo "Ready to start testing:"
    echo ""
    echo "Terminal 1 - Backend:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn app.main:app --reload"
    echo ""
    echo "Terminal 2 - Frontend:"
    echo "  cd frontend"
    echo "  npm run dev"
    echo ""
    echo "Then open: http://localhost:3000"
else
    echo -e "${YELLOW}Some issues found.${NC}"
    echo ""
    echo "Please fix the issues above and run this script again."
    echo ""
    echo "For detailed setup instructions, see:"
    echo "  - TESTING_GUIDE.md"
    echo "  - SETUP_GUIDE.md"
fi
echo "========================================="
