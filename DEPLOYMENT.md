# 🚀 Deployment Guide

Deploy both frontend and backend for free using **Netlify** and **Render**.

---

## **Step 1: Prepare Your Repository**

1. Push all code to GitHub:
```bash
git add -A
git commit -m "Ready for deployment"
git push origin claude/affirmations-refactor-qvu71z
```

2. Make sure your repo is public (or connected to Netlify/Render)

---

## **Step 2: Deploy Backend on Render**

### Create PostgreSQL Database (Free)

1. Go to https://render.com
2. Click **"New"** → **"PostgreSQL"**
3. Fill in:
   - **Name:** `affirmations-db`
   - **Database:** `affirmations`
   - **Region:** Choose closest to you
4. Click **"Create Database"**
5. Copy the **Internal Database URL** (starts with `postgres://`)

### Deploy FastAPI Service

1. Go to https://render.com (logged in)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repo
4. Select the branch: `claude/affirmations-refactor-qvu71z`
5. Fill in:
   - **Name:** `affirmations-api`
   - **Root Directory:** (leave empty)
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
6. Under **Environment Variables**, add:
   ```
   APP_ENV=production
   DATABASE_URL=<paste your PostgreSQL URL from step 1>
   GOOGLE_CLIENT_ID=<your Google Client ID>
   GOOGLE_CLIENT_SECRET=<your Google Client Secret>
   GOOGLE_REDIRECT_URI=https://your-affirmations-api.onrender.com/auth/google/callback
   SECRET_KEY=<generate a random string>
   SYNC_HOUR_UTC=2
   SYNC_MINUTE_UTC=0
   GOOGLE_API_DELAY_MS=100
   BATCH_SIZE=50
   ```
7. Click **"Create Web Service"**

Wait 5-10 minutes for deployment. You'll get a URL like `https://affirmations-api.onrender.com`

### Update Google OAuth Credentials

1. Go to Google Cloud Console
2. Edit your OAuth client
3. Update **Authorized redirect URIs** to include:
   ```
   https://affirmations-api.onrender.com/auth/google/callback
   ```

---

## **Step 3: Deploy Frontend on Netlify**

### Connect GitHub to Netlify

1. Go to https://netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **GitHub**
4. Select your `positiveaffirmations` repo
5. Choose branch: `claude/affirmations-refactor-qvu71z`
6. Fill in:
   - **Build command:** `npm install && npm run build`
   - **Publish directory:** `dist`
7. Click **"Deploy site"**

### Update API URL in Frontend

After you have the Render API URL, update your frontend to point to it:

**Edit `src/App.jsx`, `src/pages/LoginPage.jsx`, and `src/pages/DashboardPage.jsx`:**

Replace all instances of:
```javascript
'http://localhost:8000'
```

With:
```javascript
'https://affirmations-api.onrender.com'
```

Or create an environment variable:

**Add to `.env` (frontend):**
```
VITE_API_URL=https://affirmations-api.onrender.com
```

**Update API calls in components:**
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const response = await fetch(`${API_URL}/affirmations/`)
```

---

## **Step 4: Update CORS in Backend**

Edit `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://your-site.netlify.app",  # Your Netlify domain
    ] if settings.APP_ENV == "development" else ["https://your-site.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## **Step 5: Deploy Everything**

1. **Commit and push all changes:**
   ```bash
   git add -A
   git commit -m "Add deployment configuration and API URL updates"
   git push
   ```

2. **Both Netlify and Render will auto-deploy** when you push to your branch

3. **Wait for deployments to complete:**
   - Render: Check status at https://dashboard.render.com
   - Netlify: Check status at https://app.netlify.com

---

## **Testing Deployed App**

Once both are deployed:

1. Go to your Netlify URL (e.g., `https://your-site.netlify.app`)
2. Click "Sign in with Google"
3. Authorize the app
4. Test affirmations and calendar sync

---

## **Environment Variables Reference**

### Backend (Render)
```
APP_ENV=production
DATABASE_URL=postgresql://user:pass@host/db
GOOGLE_CLIENT_ID=your-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret
GOOGLE_REDIRECT_URI=https://affirmations-api.onrender.com/auth/google/callback
SECRET_KEY=your-secret-key
SYNC_HOUR_UTC=2
SYNC_MINUTE_UTC=0
GOOGLE_API_DELAY_MS=100
BATCH_SIZE=50
```

### Frontend (Netlify)
```
VITE_API_URL=https://affirmations-api.onrender.com
```

---

## **Free Tier Limitations**

### Render
- Free tier spins down after 15 mins of inactivity
- May take 30+ seconds to wake up
- Database included (free PostgreSQL)

### Netlify
- Unlimited builds and deploys
- 125,000 request/month
- No cold starts (always running)

---

## **Troubleshooting**

### Backend not starting on Render
- Check logs at https://dashboard.render.com
- Verify all environment variables are set
- Make sure `requirements.txt` is in root directory

### Frontend can't connect to backend
- Check CORS settings in `app/main.py`
- Verify API URL in frontend code
- Check browser console for errors

### OAuth redirect fails
- Make sure `GOOGLE_REDIRECT_URI` is in Google Cloud Console
- Match the exact URL (including domain and path)

---

## **Next Steps**

1. Deploy backend first (Render)
2. Get the Render API URL
3. Update frontend code with API URL
4. Deploy frontend (Netlify)
5. Test the full flow

Questions? Check the README.md or GitHub Issues.
