# Deployment Guide

> **Status: dormant / reference-only.** This repository is not currently authorized for deployment under the ecosystem governance registry. Reactivation and any production deployment require owner direction. The accepted repository branch is `main`.
>
> Provider plans, pricing, quotas, product names, and setup screens change over time. Before any future deployment, verify current Netlify, Render, Google Cloud, and other provider requirements rather than treating historical values in this document as authoritative.

This guide preserves the project's last intended deployment shape: a frontend hosted on Netlify and a FastAPI backend with PostgreSQL hosted on Render. It is operational reference material, not an instruction to deploy the dormant project now.

---

## 1. Prepare the repository

Use the accepted `main` branch unless repository governance is explicitly changed:

```bash
git add -A
git commit -m "Ready for deployment"
git push origin main
```

Private-repository access depends on the hosting provider's current GitHub integration and account permissions.

---

## 2. Backend reference: Render

If the owner reactivates the project, the historical backend deployment shape was:

- PostgreSQL database
- FastAPI web service
- repository branch: `main`
- build command: `pip install -r requirements.txt`
- start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Expected environment variables:

```text
APP_ENV=production
DATABASE_URL=<PostgreSQL URL>
GOOGLE_CLIENT_ID=<Google client ID>
GOOGLE_CLIENT_SECRET=<Google client secret>
GOOGLE_REDIRECT_URI=https://<backend-host>/auth/google/callback
SECRET_KEY=<strong random secret>
SYNC_HOUR_UTC=2
SYNC_MINUTE_UTC=0
GOOGLE_API_DELAY_MS=100
BATCH_SIZE=50
```

After a backend hostname is assigned, the exact OAuth redirect URI must also be authorized in Google Cloud Console.

Do not rely on historical assumptions about free PostgreSQL availability, service sleep behavior, pricing, or plan limits. Verify the provider's current terms before choosing a plan.

---

## 3. Frontend reference: Netlify

The historical frontend deployment shape was:

- repository branch: `main`
- build command: `npm install && npm run build`
- publish directory: `dist`

The frontend must point to the actual deployed backend URL. Prefer a deployment environment variable rather than hard-coding a production endpoint:

```text
VITE_API_URL=https://<backend-host>
```

Application code should continue to provide an appropriate local-development fallback where required.

Do not rely on historical claims about build quotas, request quotas, pricing, or other plan limits. Verify current provider documentation before deployment.

---

## 4. CORS and OAuth

Before any production launch:

- restrict backend CORS to the actual approved frontend origin(s);
- authorize the exact production OAuth redirect URI in Google Cloud;
- keep client secrets and `SECRET_KEY` out of committed source;
- verify development origins are not unintentionally accepted in production;
- verify account access, secret rotation, and recovery procedures.

---

## 5. Validation before a future launch

If the project is reactivated, validate at minimum:

1. the repository's current governance and accepted branch;
2. provider plans and deployment requirements;
3. backend startup and database connectivity;
4. frontend-to-backend connectivity and CORS;
5. Google OAuth redirect behavior;
6. secret handling and production environment variables;
7. the complete sign-in, affirmation, and calendar-sync flow.

Deployment is not currently part of the repository's accepted dormant state. This document should be refreshed again as part of any future reactivation before production actions are taken.
