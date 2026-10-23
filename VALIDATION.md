# Validation record

Built and checked on **23 October 2026**.

## Passed

**29 tests passed** using `python -m unittest discover -s tests -v`.

- Streamlit AppTest: all eleven pages render, navigation works, dark-mode toggle renders, daily check-in saves, task creation saves, focus timer starts/stops, monthly budget calculation saves, coding attempts and debugging records save, all coding tracks render, practice can be added to the planner, AI is the primary direction, and job-requirement evidence mapping saves.
- Domain rules: protected work/meals/events do not overlap focus suggestions; optical-shop windows conflict with weekday work; approved leave and suitable weekend slots allow the task; low-energy days are capped; zero budgets produce no focus suggestions; past time is not suggested; completed and not-yet-available tasks are excluded.
- Calculations and storage: allocation shortfalls, zero-contribution / achieved-goal cases, recall intervals, SQLite persistence and updates, per-run cache invalidation, and complete backup validation.
- Cloud contract tests with mocked HTTP: user filters and authorization headers are applied; writes/deletes include the correct record/user; historical reads paginate past 500 rows; connection failures are explicit rather than silently replacing data.
- Authored learning materials: seven Python worked solutions pass their supplied checks; the SQL worked solution returns the expected totals including the user with no transactions, using an isolated in-memory SQLite database. Review recommendation and review-date logic pass.
- Python application modules compile successfully.

Test runtime: Python 3.12.14, Streamlit 1.66.1, requests 2.34.2, pandas 2.2.3.

## Not yet verified

- **Live deployment:** no Streamlit app has been published. Streamlit's account page requires sign-in and review of its terms.
- **Live Supabase Auth/RLS:** database schema and request contracts are included, but no user-owned project credentials were supplied. Mocked HTTP tests do not prove a deployed database's policies or cross-device persistence. Follow DEPLOY.md to verify those properties after setup.
- **Visual browser/device QA:** the managed preview environment could not launch the Python runtime, so PC/mobile/tablet screenshots and native-browser layout checks were not available. The app uses Streamlit's responsive columns plus a small-screen stylesheet, accessible labels, and neutral themes; final rendering still needs a real browser/device check.
- **Dart compilation:** the two Dart samples were reviewed for their contracts and edge cases but were not run because this environment did not provide the Dart SDK. Run the included starter/solution checks locally using `dart run FILE.dart`.
- **SQL on PostgreSQL:** the exercise uses shared SQL syntax and passes SQLite checks, but it was not executed against a live PostgreSQL instance.
- **Background notifications and automatic external feeds:** not included. The open app has a live PHT clock, input-driven records and planner updates, explicit refresh, and manual calendar export. It does not notify you while closed or automatically fetch jobs, exam prices, bank balances, or new research.

## Known behavior

Same-record concurrent edits use last saved edit wins. Demo records and unfinished timers are session state. Cloud personal records require login and a properly configured Supabase table; local SQLite mode is only for private local use. Backup imports validate first, then merge by ID; cloud imports are not an atomic multi-record transaction. These limits are explained in README.md and DEPLOY.md.
