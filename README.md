# 365-Day Affirmation Calendar

A single-file web app that generates a 365-day positive affirmation calendar as a downloadable `.ics` file — importable into Google Calendar, Apple Calendar, Outlook, and any standard calendar app.

## Live Site

Hosted via GitHub Pages at `https://<your-username>.github.io/<repo-name>/`

## How to deploy

1. Create a new GitHub repository
2. Upload `index.html` to the root
3. Go to **Settings → Pages → Source** and set branch to `main`, folder to `/ (root)`
4. GitHub will publish the page within a minute or two

## How it works

- Runs entirely in the browser — no server, no tracking, no external requests
- Generates one all-day calendar event per day for 365 days, starting tomorrow
- Downloads as a single `.ics` file on click
