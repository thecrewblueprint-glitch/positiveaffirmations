# Google Calendar Affirmations App Architecture

## Purpose

Build an app that connects to Google Calendar, generates 365 unique positive affirmations, assigns one affirmation to each day of the year, and schedules or displays them automatically.

The first practical version should focus on a clean, reliable MVP:

1. User connects a Google account.
2. App requests permission to create calendar events.
3. App generates 365 unique affirmations locally.
4. App schedules one daily calendar event per date.
5. App stores Google event IDs and sync status for later editing, deletion, or resync.

## Google Calendar Integration

The safest Google Calendar integration uses OAuth 2.0 with minimal scopes.

Recommended scopes:

- `https://www.googleapis.com/auth/calendar.events` — required when the app creates, updates, or deletes events.
- `https://www.googleapis.com/auth/calendar.readonly` — only needed for read-only calendar access.

For this app, `calendar.events` is the key permission because the app needs to create affirmation events.

Event creation should use the Calendar API `events.insert()` endpoint.

## Core App Responsibilities

The app should do three jobs:

1. **Authenticate the user with Google**
   - Use OAuth 2.0.
   - Store access and refresh tokens securely.
   - Refresh tokens before expiry.

2. **Generate a full year of non-repeating affirmations**
   - Generate locally before touching Google Calendar.
   - Run duplicate checks before saving.
   - Save each affirmation by user and date.

3. **Create or manage daily calendar entries**
   - Insert one event per day.
   - Store the returned Google event ID.
   - Track status for successful, failed, pending, or deleted events.

## Recommended Architecture

### Frontend

Responsibilities:

- Login screen.
- Google Calendar connection flow.
- Onboarding/settings.
- Calendar preview.
- Affirmation preview.
- Regenerate/edit controls.
- Sync status display.

Possible implementations:

- Laravel Blade for fastest MVP.
- Vue or React if the interface becomes more interactive.

### Backend

Responsibilities:

- Google OAuth flow.
- Token storage and refresh.
- Calendar sync logic.
- Affirmation generation.
- Event creation and deletion.
- Retry logic.
- API endpoints for the frontend.

Recommended backend: **Laravel**.

Laravel is a good fit because it handles scheduled commands, queues, database migrations, background jobs, and API integrations well.

### Database

Responsibilities:

- Store users.
- Store connected Google accounts.
- Store generated affirmations.
- Store Google Calendar event IDs.
- Store app settings.
- Track sync failures.

### Scheduler / Worker

Responsibilities:

- Create calendar events in batches.
- Retry failed inserts.
- Refresh Google tokens.
- Process regeneration requests.
- Prevent duplicate event creation.

Use Laravel queues or a worker service.

## Data Model

### `users`

Suggested fields:

- `id`
- `name`
- `email`
- `timezone`
- `created_at`
- `updated_at`

### `google_accounts`

Suggested fields:

- `id`
- `user_id`
- `google_user_id`
- `google_email`
- `access_token`
- `refresh_token`
- `token_expires_at`
- `token_refreshed_at`
- `google_calendar_id`
- `created_at`
- `updated_at`

Notes:

- Store tokens securely.
- Refresh tokens before expiry.
- Track `token_refreshed_at` for debugging and maintenance.

### `affirmations`

Suggested fields:

- `id`
- `user_id`
- `date`
- `text`
- `theme`
- `text_hash`
- `created_at`
- `updated_at`

Recommended constraints:

- Unique key on `user_id + date`.
- Optional unique key on `user_id + text_hash` to prevent duplicate affirmation text for the same user.

### `calendar_events`

Suggested fields:

- `id`
- `user_id`
- `affirmation_id`
- `google_event_id`
- `google_calendar_id`
- `status`
- `last_error`
- `synced_at`
- `created_at`
- `updated_at`

Suggested statuses:

- `pending`
- `synced`
- `failed`
- `deleted`

### `app_settings`

Suggested fields:

- `id`
- `user_id`
- `preferred_time`
- `tone`
- `categories`
- `notification_style`
- `event_title_style`
- `created_at`
- `updated_at`

## Affirmation Engine

The affirmation engine should generate variety without relying on purely random output.

Use a combination of:

- Themes.
- Sentence templates.
- Verbs.
- Nouns.
- Emotional tone.
- Monthly focus areas.
- Duplicate detection.

Suggested themes:

- Confidence.
- Productivity.
- Peace.
- Resilience.
- Leadership.
- Health.
- Gratitude.
- Discipline.
- Self-worth.
- Momentum.
- Patience.
- Courage.

Suggested monthly structure:

| Month | Theme |
|---|---|
| January | Momentum |
| February | Self-worth |
| March | Discipline |
| April | Renewal |
| May | Confidence |
| June | Focus |
| July | Resilience |
| August | Health |
| September | Leadership |
| October | Gratitude |
| November | Peace |
| December | Reflection |

### Deterministic Seeded Generation

A deterministic seeded approach is better than pure random generation because it allows the same user/date pair to regenerate consistently.

Pseudocode:

```php
$seed = $user->id . '-' . $date->format('Y-m-d');
$theme = $themes[crc32($seed) % count($themes)];
$template = $templates[crc32($seed . '-template') % count($templates)];
$verb = $verbs[crc32($seed . '-verb') % count($verbs)];
$noun = $nouns[crc32($seed . '-noun') % count($nouns)];
```

Example template:

```text
I am growing in {noun} every day.
```

Before saving, hash the final text and verify it has not already been used for that user.

## Calendar Event Strategy

There are two main calendar display options.

### Option 1: Affirmation as the event title

Example:

```text
I am steady, capable, and prepared for today.
```

Pros:

- The affirmation is visible immediately.

Cons:

- Long titles clutter month and week views.
- Calendar grid becomes harder to scan.

### Option 2: Fixed event title with affirmation in the description

Example title:

```text
Daily Affirmation
```

Example description:

```text
I am steady, capable, and prepared for today.
```

Pros:

- Cleaner calendar view.
- Better for 365 events.
- Easier to search and manage.

Cons:

- User must open the event to read the full text.

Recommended MVP choice: **Option 2**.

## Event Type

For the MVP, use one all-day event per date.

Later options:

- Timed event at the user’s preferred time.
- Reminder notification.
- Morning notification.
- Weekly theme summary.
- Monthly batch view.

## Timezone Handling

Timezone handling must be explicit.

Rules:

- Store dates in a neutral format.
- Store the user’s preferred timezone.
- Convert date/time only when inserting into Google Calendar.
- Avoid assuming server timezone.
- Do not generate date ranges based only on UTC if the user expects local dates.

For all-day events, use Google Calendar date fields instead of datetime fields when possible.

## Rate Limiting and Retry Logic

Google Calendar API quotas can vary by project status, verification, and usage.

Implementation rules:

- Do not fire 365 event insertions in one blocking request.
- Use queue jobs.
- Batch event creation.
- Add exponential backoff.
- Store failed attempts.
- Let the user retry failed syncs.

A safe MVP pattern:

1. Generate all 365 affirmations.
2. Queue daily event insert jobs.
3. Process jobs in small batches.
4. Mark each event as synced or failed.
5. Show sync progress in the dashboard.

## Token Lifecycle

The Google account connection must handle token refresh correctly.

Rules:

- Store `access_token`, `refresh_token`, and `token_expires_at`.
- Store `token_refreshed_at`.
- Refresh before the token expires.
- Handle revoked permissions cleanly.
- Prompt the user to reconnect if refresh fails.

## MVP Build Phases

### Phase 1 — Static/Local Affirmation App

Goal: prove the affirmation engine and UI without Google integration.

Build:

- 365 affirmations.
- Daily display.
- Local preview.
- Basic settings.

### Phase 2 — Laravel Foundation

Goal: create the backend structure.

Build:

- Laravel app.
- Users table.
- Affirmations table.
- App settings table.
- Basic dashboard.

### Phase 3 — Google OAuth

Goal: connect a Google account safely.

Build:

- Google OAuth login/connect flow.
- Token storage.
- Token refresh.
- Reconnect handling.

### Phase 4 — Calendar Event Sync

Goal: create events in Google Calendar.

Build:

- `events.insert()` logic.
- Queue jobs.
- Sync status tracking.
- Error logging.

### Phase 5 — Editing and Resync

Goal: make the system maintainable.

Build:

- Edit a single affirmation.
- Regenerate one date.
- Delete synced events.
- Resync failed events.
- Delete a month or full year.

### Phase 6 — Polished Dashboard

Goal: make the app usable for real users.

Build:

- Upcoming affirmation preview.
- Year calendar overview.
- Monthly theme display.
- Sync progress.
- Reconnect warning.

## Fastest MVP Path

The fastest useful version is:

1. Build a static page with 365 generated affirmations.
2. Add date-based display.
3. Add ICS export for all 365 affirmations.
4. Later replace ICS-only export with direct Google Calendar OAuth sync.

This path avoids OAuth complexity at first while still giving users a calendar-ready product.

## Implementation Notes

- Generate all affirmations locally before creating Google events.
- Keep Google scope minimal.
- Use one event per day because each description is unique.
- Store Google event IDs immediately after successful insertion.
- Never duplicate events if the user retries sync.
- Use clear user-facing language about permissions.
- Keep the first release simple: fixed title, affirmation in description, one all-day event per day.

## Open Questions

- Should the MVP be static-first with ICS export, or Laravel-first with OAuth?
- Should affirmations be all-day events or timed morning reminders?
- Should users choose tones such as calm, bold, spiritual, practical, or business-minded?
- Should the app support deleting an entire generated year from Google Calendar?
- Should the app eventually support recurring yearly regeneration?
