# 💝 Daily Affirmations

**Live Development:** `http://localhost:3000`

365 unique daily affirmations synced to your Google Calendar. A complete full-stack application with FastAPI backend and React frontend using Crew Blueprint branding.

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ (frontend)
- Python 3.10+ (backend)
- Google OAuth credentials

### Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m app.db.init_db

# Start API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start scheduler
python -m app.workers.scheduler
```

**API:** `http://localhost:8000`  
**Docs:** `http://localhost:8000/docs`

### Frontend Setup

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

**Frontend:** `http://localhost:3000`

---

## 📋 Features

### Core Functionality
- ✨ **365 Unique Affirmations** — One per day with monthly themes
- 📅 **Google Calendar Sync** — Auto-sync affirmations to your calendar
- 🔐 **Google OAuth Login** — Secure authentication
- ✏️ **Edit Affirmations** — Customize daily affirmations
- 📱 **Responsive Design** — Works on mobile, tablet, and desktop
- 💝 **GitHub Sponsors** — Integrated donation button

### Dashboard
- Interactive calendar picker for browsing dates
- Large display of current day's affirmation
- Edit affirmation text inline
- Sync status notifications
- List of all affirmations with previews

---

## 🏗️ Architecture

### Backend (FastAPI)
- **Database:** SQLAlchemy 2.0 ORM with SQLite (dev) / PostgreSQL (prod)
- **Auth:** Google OAuth 2.0 with automatic token refresh
- **Scheduler:** APScheduler for nightly sync jobs
- **API:** RESTful endpoints for affirmations, calendar, donations

### Frontend (React + Vite)
- **Build Tool:** Vite for fast development and optimized builds
- **Styling:** CSS with Crew Blueprint color system
- **State:** React hooks (useState, useEffect)
- **API Client:** Fetch API

### Color Scheme (Crew Blueprint)
- **Primary Background:** Blueprint Black (#050708)
- **Secondary Background:** Charcoal Steel (#0E1216)
- **Primary Accent:** Safety Gold (#F5B400)
- **Text:** Worklight White (#F4F6F8)
- **Success:** Completion Green (#4CC66A)

---

## 📁 Project Structure

```
positiveaffirmations/
├── app/                          # FastAPI backend
│   ├── main.py                   # App entry point
│   ├── core/config.py            # Settings & environment
│   ├── models/                   # SQLAlchemy ORM models
│   ├── db/                       # Database setup
│   ├── services/                 # Business logic
│   ├── api/routes/               # API endpoints
│   └── workers/scheduler.py      # Background jobs
│
├── src/                          # React frontend
│   ├── main.jsx                  # React entry point
│   ├── App.jsx                   # Main component
│   ├── index.css                 # Global styles
│   ├── components/               # Reusable components
│   ├── pages/                    # Page components
│   └── DonationWidget.jsx        # GitHub Sponsors
│
├── index.html                    # HTML entry
├── package.json                  # Frontend deps
├── vite.config.js                # Vite config
├── requirements.txt              # Backend deps
└── README.md                     # This file
```

---

## 🔌 API Endpoints

### Authentication
- `GET /auth/google/start` — Get OAuth auth URL
- `POST /auth/google/callback` — Complete OAuth login
- `DELETE /auth/google/disconnect/{user_id}` — Sign out

### Affirmations
- `GET /affirmations/` — Get all user affirmations
- `GET /affirmations/{date}` — Get affirmation for specific date
- `PATCH /affirmations/{id}` — Update affirmation text

### Calendar
- `POST /calendar/sync` — Sync affirmations to Google Calendar
- `GET /calendar/status/{user_id}` — Get sync progress

### Donations
- `POST /donations/log` — Log a donation event
- `GET /donations/stats` — Get public donation statistics

---

## ⚙️ Configuration

Create a `.env` file from `.env.example`:

```env
DATABASE_URL=sqlite:///./app.db
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
APP_ENV=development
SECRET_KEY=your-secret-key
SYNC_HOUR_UTC=2
SYNC_MINUTE_UTC=0
GOOGLE_API_DELAY_MS=100
BATCH_SIZE=50
```

---

## 📦 Build for Production

### Frontend
```bash
npm run build
# Creates optimized build in dist/
```

---

## 💬 Support

Built with 💝 by The Crew Blueprint

**Made for daily affirmations & positive growth**
