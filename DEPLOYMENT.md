# Deployment Boundary

**Status:** dormant / reference-only.  
**Accepted branch:** `main`.  
**Current deployment authority:** none.

This repository preserves application source; it does not preserve an active hosting plan. Historical Netlify/Render/PostgreSQL deployment details were moved into long-term repository memory and remain recoverable through Git history.

Do not deploy, connect OAuth, start scheduled jobs, provision paid services, or reactivate external infrastructure without explicit owner direction.

## Before any future reactivation

Re-establish deployment from current evidence rather than old provider assumptions:

1. verify current repository governance and accepted source;
2. audit dependencies and application startup;
3. choose and verify current frontend/backend/database providers;
4. remove or replace historical hard-coded service URLs where appropriate;
5. configure secrets only through approved runtime secret storage;
6. verify Google OAuth scopes and exact redirect URIs;
7. restrict CORS to approved origins;
8. test database persistence, token encryption, authentication, calendar sync, retry behavior, and scheduler behavior;
9. verify provider pricing/limits before authorizing recurring cost;
10. perform an end-to-end production validation before calling the application live.

See [`MEMORY.md`](MEMORY.md) for the historical deployment shape and the important architectural/security decisions retained outside the working tree.
