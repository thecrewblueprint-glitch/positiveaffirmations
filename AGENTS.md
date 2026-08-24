# AGENTS.md — Dormant Daily Affirmations application

## Status

This repository contains a standalone affirmations application, but it is currently **dormant**. Do not treat the existing FastAPI/React/OAuth/database implementation as authorization to run, deploy, reconnect, modernize, or expand the product.

## Canonical state

- Accepted branch: `main`.
- Existing accepted source documents the last known application architecture.
- `50yearroadmap` tracks this repository as a dormant adjacent project.

## Reactivation gate

Substantive work requires explicit owner reactivation/authorization first. After reactivation, substantive agent-authored changes use the matrix PR-first lifecycle:

`main → work branch → change → validate → PR → review/audit → authorized merge → verify`

Opening a PR is not merge authority.

## Security/data boundaries

The application architecture includes authentication, Google OAuth, calendar access, configuration secrets, and a database. Therefore:

- never commit OAuth client secrets, app secret keys, tokens, refresh tokens, user credentials, database credentials, or production `.env` values;
- do not connect/reconnect Google accounts or invoke external calendar actions merely to inspect the repository;
- do not assume old configuration, dependency versions, auth flows, or deployment instructions remain safe/current if reactivated;
- inspect and validate security-sensitive architecture before any future deployment/revival;
- do not import personal/private data from other repositories.

## Cost/external-service boundary

Dormant status means no recurring jobs, hosting, paid services, schedulers, or external integrations should be activated merely for governance or testing. Any such activation requires separate owner authorization.

## Interruption/recovery

No persistent continuation checkpoint is required while dormant. If reactivated, preserve meaningful work in a PR and add/use a lightweight `NEXT_SESSION.md` or equivalent when needed.

## Agent entry

This file is the local machine-readable entry contract. Follow current canonical matrix governance in `50yearroadmap` for authority/change-control details. Dormancy is itself an accepted state and must be preserved until the owner changes it.
