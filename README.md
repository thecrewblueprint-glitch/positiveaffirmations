# Positive Affirmations

A preserved 365-day positive-affirmations application with Google Calendar integration.

**Status:** dormant / reference-only  
**Accepted branch:** `main`  
**Deployment:** not currently authorized

## Retained implementation

The repository keeps the implemented application rather than its full development history:

- FastAPI backend with SQLAlchemy persistence;
- React + Vite frontend;
- Google OAuth and Google Calendar synchronization;
- JWT application sessions and per-user authorization;
- encrypted Google OAuth tokens at rest;
- scheduler/batching support for calendar synchronization.

The current source remains authoritative for implementation details. Historical architecture, deployment decisions, completed work, and rejected approaches are routed through [`MEMORY.md`](MEMORY.md).

## Local development reference

Backend:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
npm install
npm run dev
```

Use `.env.example` as the backend configuration reference. Secrets, OAuth credentials, tokens, and runtime databases must not be committed.

## Reactivation boundary

Do not treat old provider configuration or URLs in source history as current infrastructure authority. Before any future deployment or external-service activation, revalidate:

- current dependency compatibility;
- frontend/backend configuration;
- database persistence;
- Google OAuth scopes and redirect URIs;
- CORS and secret handling;
- scheduler behavior;
- hosting/provider requirements and cost.

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for the current deployment boundary. Reactivation requires explicit owner direction.
