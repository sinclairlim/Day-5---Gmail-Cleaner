# Gmail Cleaner Frontend

Modern React frontend with TypeScript, built with Vite.

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Features

- **Authentication** - Google OAuth login flow
- **Dashboard** - Main interface for email management
- **Email List** - Interactive list with selection
- **Stats Cards** - Visual statistics display
- **AI Analysis** - LangChain insights panel

## Project Structure

```
src/
├── components/        # Reusable UI components
│   ├── EmailList.tsx
│   ├── StatsCard.tsx
│   └── AnalysisPanel.tsx
├── pages/            # Page components
│   ├── LoginPage.tsx
│   ├── DashboardPage.tsx
│   └── AuthCallback.tsx
├── services/         # API integration
│   └── api.ts
├── App.tsx           # Main app component
└── main.tsx          # Entry point
```

## Development

The app runs on `http://localhost:3000` and proxies API requests to the backend at `http://localhost:8000`.

## Building

```bash
npm run build
```

Outputs to `dist/` folder, ready for deployment.

## Deployment

Deploy the `dist` folder to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- Any static hosting service

Remember to update the backend `CORS_ORIGINS` with your production URL.
