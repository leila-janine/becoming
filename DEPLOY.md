# Deploy Becoming on Streamlit Community Cloud

This is a Python Streamlit application. Use the project files directly; do not use a static website host. You need a GitHub repository, a Streamlit Community Cloud account, and a Supabase project for private, durable records across devices.

## 1. Put the source in a new GitHub repository

Create a new **private** repository such as `becoming`. Keep this project separate from existing study or thesis repositories.

Upload the **contents** of this extracted project directory into the repository root. `app.py` and `requirements.txt` must be at the top level. Include the `.streamlit` directory and `config.toml`, but never upload a real `secrets.toml` file.

Do not upload `.venv`, `data`, personal JSON backups, or `__pycache__`. The included `.gitignore` handles Git-based workflows; when uploading through a website, you still need to select files carefully.

## 2. Set up your private database and login

1. Create a Supabase project in your own account. Choose a region appropriate for your use. Review the provider’s current plan, terms, and quotas before creating it; no paid service is required by this code.
2. Open **SQL Editor**, paste the complete `supabase_schema.sql`, and run it once.
3. In **Authentication → Users**, create or invite your own user. Complete your account/password setup using Supabase’s interface. A confirmed email/password user can sign in to this app. Password creation and recovery remain in Supabase’s account tools.
4. Since this is a personal app, disable new public signups in Authentication settings after you have your own account. Setting names may vary as the provider updates its UI.
5. From the project’s API settings/connect dialog, copy the **project URL** and **publishable key** (or legacy **anon key**). Never use a secret / service-role key. Those keys can bypass the row restrictions this app depends on.

Database schema: one row per record, associated with `auth.users.id`. RLS permits authenticated users to read and write only their own rows. Unauthenticated visitors cannot read this table. An unconfigured deployment shows a setup message; there is no public demo or shared personal SQLite fallback.

The configurable planner, task statuses, Pomodoro, and money dashboard update uses the existing JSON payloads. No schema migration or new secrets are required for an already configured app.

## 3. Deploy

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in. Review any requested terms and account permissions yourself.
2. Choose **Create app** and select your repository and branch.
3. Set the **main file path to `app.py`**. Choose **Python 3.12** in advanced settings if the option is available. The app was tested on Python 3.12.14.
4. In **Advanced settings → Secrets** (or the app’s settings after creation), paste:

```toml
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_ANON_KEY = "YOUR_PUBLISHABLE_OR_LEGACY_ANON_KEY"
```

5. Do **not** set `BECOMING_LOCAL` in Cloud. It is only for a private loopback development session on your computer.
6. Deploy and wait for Streamlit’s successful app page. If access settings allow it, restrict app viewers to yourself as an additional layer. Keep the app’s own Supabase login enabled for personal records.
7. Sign in with the user you created in Supabase. Set your workdays, confirm provisional dates, and add your first check-in.

You should then receive a `streamlit.app` URL. Open that same URL on your phone and tablet, sign in with the same account, and your saved records will be available there.

## 4. Verify before using it for daily records

- Save a check-in on your PC. Open the app on another device, sign in, and confirm the record after Refresh.
- Restart/reboot the Streamlit app and verify the record survives.
- Sign out. Verify personal records are not shown and there is no demo entry.
- If testing with a second account, verify it cannot see the first account’s entries. In Supabase, inspect the table’s RLS policy and confirm the table is not readable by the `anon` role.
- Add a weekday optical-shop task with a 10:00–15:00 window. Confirm the planner defers it while 09:00–18:00 work is scheduled. Edit that day’s work block and confirm Today and the weekly preview follow the saved change.
- Test light/dark mode and scrolling on phone, tablet, and PC. Phones/tablets use the page selector above the content; Account & sync provides refresh and sign-out. Check that form columns stack, tabs scroll without squeezing labels, schedule blocks edit by touch, and money summaries have readable labels.
- In Coding practice, run a Python exercise and its checks, then a SQL query. The first run downloads Pyodide from jsDelivr. Test a syntax error and Stop. Run/Save draft transfers code into the attempt form; Save coding practice persists it. The runner requires browser WebAssembly/module-worker support and an internet connection for its initial runtime download.
- Download and restore a test backup containing disposable records. Restore merges by ID; it does not replace the whole database.

The cloud request behavior is covered by mocked tests, but **live authentication, database policies, cross-device persistence, and physical-device rendering cannot be fully validated until you supply and configure your own deployment**.

## Troubleshooting

**Sign-in failed:** confirm the account exists, its email is confirmed, and its password is correct. The app does not create accounts or accept reset tokens. Use Supabase’s user-management / recovery tools.

**Could not load or sync:** run the SQL script, confirm the project URL and publishable key, and verify the project is active and reachable. Sign out and in again if the session expired. The app intentionally does not substitute an empty local database when cloud sync fails.

**A connection setup message appears:** deployment secrets are missing. Add the two top-level TOML settings exactly as shown and reboot the app.

**Module not found:** confirm `requirements.txt` is at the repository root and the entry point is `app.py`. Reboot after pushing corrected dependency files.

**Phone shows stale data:** use Your space → Refresh, or interact with a page. Same-record edits made simultaneously use last saved edit wins. Avoid keeping two editing sessions open on the same record.

**Timer resets after reload:** focus timers are session state, not durable background jobs. Log completed work manually if the browser reconnects. A logged session is durable; an unfinished running timer is not.

**Code runtime fails to load:** check the browser’s WebAssembly/module-worker support and access to `cdn.jsdelivr.net`. Click Run again after reconnecting. Code stays in the editor while the runtime loads. No server execution fallback is used. Download the code for local use if the browser cannot load the runtime.

**No suitable slot:** check the selected date, current PHT time, remaining focus budget, task duration, allowed window, and saved time blocks. Edit Your schedule for one-off changes or Your space for recurring changes. An appointment never silently cancels another block.

**Need reminders while the app is closed:** download the day’s `.ics` file and import it into your calendar. Set any notifications in that calendar. Becoming does not currently send notifications or automatically sync calendar changes.

## Official references

- [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
- [Streamlit secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Supabase password authentication](https://supabase.com/docs/guides/auth/passwords)
- [Supabase row-level security](https://supabase.com/docs/guides/database/postgres/row-level-security)

## After connecting an existing deployment

Reload the app after saving the two Secrets values. A configured app shows Email and Password sign-in. Use the email/password user in your Supabase project; your Supabase dashboard password and database password are different accounts/credentials. Keep row-level security enabled. Test by saving one non-sensitive check-in, reloading, and signing in on a second device.

The schema creates the table and access rules only. It does not create the project, create your user account, or automatically connect Streamlit. Use the API Project URL (`https://PROJECT.supabase.co`), not a PostgreSQL connection string. A new `sb_publishable_...` key can be placed in the app's existing `SUPABASE_ANON_KEY` setting; the legacy setting name is retained for compatibility. Never substitute a secret/service-role key.
