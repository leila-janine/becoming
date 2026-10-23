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

Database schema: one row per record, associated with `auth.users.id`. RLS permits authenticated users to read and write only their own rows. Unauthenticated visitors cannot read this table. An unconfigured deployment shows only a temporary per-session demo, never a shared personal SQLite file.

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
- Sign out. Verify personal records are not shown in the login or demo views.
- If testing with a second account, verify it cannot see the first account’s entries. In Supabase, inspect the table’s RLS policy and confirm the table is not readable by the `anon` role.
- Add a weekday optical-shop task with a 10:00–15:00 window. Confirm the planner defers it while 09:00–18:00 work is protected.
- Test light/dark mode and scrolling on phone, tablet, and PC. Check that the sidebar can be opened on a small screen and that forms are readable.
- Download and restore a test backup containing disposable records. Restore merges by ID; it does not replace the whole database.

The cloud request behavior is covered by mocked tests, but **live authentication, database policies, cross-device persistence, and physical-device rendering cannot be fully validated until you supply and configure your own deployment**.

## Troubleshooting

**Sign-in failed:** confirm the account exists, its email is confirmed, and its password is correct. The app does not create accounts or accept reset tokens. Use Supabase’s user-management / recovery tools.

**Could not load or sync:** run the SQL script, confirm the project URL and publishable key, and verify the project is active and reachable. Sign out and in again if the session expired. The app intentionally does not substitute an empty local database when cloud sync fails.

**Only the demo appears:** deployment secrets are missing. Add the two top-level TOML settings exactly as shown and reboot the app.

**Module not found:** confirm `requirements.txt` is at the repository root and the entry point is `app.py`. Reboot after pushing corrected dependency files.

**Phone shows stale data:** use Your space → Refresh, or interact with a page. Same-record edits made simultaneously use last saved edit wins. Avoid keeping two editing sessions open on the same record.

**Timer resets after reload:** focus timers are session state, not durable background jobs. Log completed work manually if the browser reconnects. A logged session is durable; an unfinished running timer is not.

**No suitable slot:** check the selected date, current PHT time, remaining focus budget, task duration, allowed window, workdays, meals, and commitments. A time budget cannot create free time inside a protected block.

**Need reminders while the app is closed:** download the day’s `.ics` file and import it into your calendar. Set any notifications in that calendar. Becoming does not currently send notifications or automatically sync calendar changes.

## Official references

- [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
- [Streamlit secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Supabase password authentication](https://supabase.com/docs/guides/auth/passwords)
- [Supabase row-level security](https://supabase.com/docs/guides/database/postgres/row-level-security)
