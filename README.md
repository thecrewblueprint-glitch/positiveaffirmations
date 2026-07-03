# Positive Affirmations

A lightweight app concept for generating 365 unique positive affirmations and delivering one affirmation per day through a calendar-style experience.

## Current Direction

The project is being shaped around two possible release paths:

1. **Fast static MVP** — generate 365 affirmations, display the affirmation for the current date, and optionally export an `.ics` calendar file.
2. **Full Google Calendar app** — use OAuth 2.0, generate 365 unique affirmations, and create one Google Calendar event per day.

The static MVP is the quickest version to ship. The Google Calendar version is the stronger long-term product.

## Core Features

- 365 unique affirmations.
- One affirmation assigned to each day of the year.
- Non-repeating affirmation generation.
- Daily display mode.
- Calendar/event export path.
- Future Google Calendar OAuth integration.
- Future dashboard for previewing, editing, regenerating, and syncing affirmations.

## Recommended MVP

Start with a static or simple web app that:

1. Generates or stores 365 affirmations.
2. Shows today’s affirmation.
3. Lets the user browse upcoming affirmations.
4. Exports a 365-day `.ics` calendar file.

This avoids Google OAuth complexity during the first build while still producing a useful calendar-ready tool.

## Long-Term Version

The full app should include:

- Google OAuth 2.0.
- Minimal Google Calendar scopes.
- Secure token storage.
- 365 generated affirmations saved to a database.
- One Google Calendar event per date.
- Event ID tracking for updates and deletion.
- Background workers for retry logic and rate-limit handling.

## Documentation

- [Google Calendar Affirmations App Architecture](docs/google-calendar-affirmations-architecture.md)
