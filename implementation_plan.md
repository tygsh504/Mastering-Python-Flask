# Implementation Plan: Mastering Python Flask Web App

This plan outlines the steps to build the Python Flask web application requested, based on the `website for prompt.mp4` video. The app will have separated HTML, CSS, and JS files, use Supabase for authentication and database management, and be prepared for deployment on Vercel.

## Goal Description

Recreate the "Mastering Python Flask" educational platform as seen in the video. The platform includes authentication, a dashboard/profile, video lessons, slides, an interactive worksheet, and account settings.

## User Review Required

> [!IMPORTANT]
> Please review the proposed Database Schema to ensure it meets your expectations for Supabase.
> Note: Vercel deployment requires a specific file structure (using an `api/` folder or setting up `vercel.json` with WSGI handlers). I will configure it using `vercel.json` and a standard Flask structure.
> Supabase credentials will be loaded from environment variables. You will need to add these (`SUPABASE_URL`, `SUPABASE_KEY`) in your Vercel project settings later.

## Open Questions

- Should the videos and slides be hardcoded into the templates as static placeholders for now, or would you prefer a basic database structure for them as well? (I plan to use placeholders to match the visual design exactly as in the video).
- Do you want me to write all the static content (text, paragraphs) exactly as shown in the video?

## Proposed Architecture and Database Schema

### Database Schema (Supabase)
We will need the following tables in Supabase:
1. **profiles**: Extends the default Supabase `auth.users` with `id`, `full_name`, `university`, `major`, `python_level`, `short_bio`, `avatar_url`, `lessons_completed`, `worksheets_saved`, `current_level`.
2. **worksheets**: Stores user's worksheet progress. Columns: `id`, `user_id` (foreign key to profiles), `purpose`, `target_user`, `mission`, `relevant_research`, `scoping_features`, `idea_finalising`.
3. **preferences**: Stores user account settings. Columns: `user_id`, `course_updates`, `lesson_reminders`, `product_news`.

### Proposed Changes

#### [NEW] requirements.txt
Dependencies including `Flask`, `supabase`, `gunicorn`, `python-dotenv`.

#### [NEW] vercel.json
Vercel configuration to deploy the Flask application using `@vercel/python`.

#### [NEW] app.py
The main Flask application containing the routes:
- `/`: Home page
- `/login`, `/signup`, `/logout`: Authentication routes
- `/videos`: Video lessons page
- `/slides`: Slides page
- `/worksheet`: Interactive worksheet page
- `/profile`: User profile dashboard
- `/settings`: Account settings

#### [NEW] static/css/style.css
A single comprehensive CSS file replicating the modern design, typography, colors, and layout seen in the video.

#### [NEW] static/js/script.js
JavaScript file for handling the worksheet progress bar, slide navigation, dropdowns, and form submissions.

#### [NEW] templates/base.html
The base layout containing the navigation bar and footer.

#### [NEW] templates/*.html
Individual pages: `index.html`, `login.html`, `signup.html`, `videos.html`, `slides.html`, `worksheet.html`, `profile.html`, `settings.html`.

## Verification Plan

### Automated / Local Tests
- Run `python app.py` (or `flask run`) locally.
- Navigate through all routes (`/`, `/login`, `/worksheet`, etc.) to verify rendering.
- Test responsive layout and JavaScript interactions (e.g., slide Next/Prev buttons).

### Manual Verification
- User will need to add their Supabase URL and Key to their `.env` file (locally) and Vercel environment variables (in production).
- Verify that user signup and login successfully create rows in Supabase.
- Verify Vercel deployment works as expected by running `vercel` CLI or pushing to GitHub.
