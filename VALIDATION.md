# Validation record

Built and checked on **23 October 2026**.

## Passed

**48 tests passed** using `python -m unittest discover -s tests -v`.

- Streamlit AppTest: all eleven pages render, navigation works, native theme controls are delegated to Streamlit, daily check-in saves, task creation saves, focus timer starts/stops, monthly budget calculation saves, coding attempts and debugging records save, all coding tracks render, practice can be added to the planner, AI is the primary direction, and job-requirement evidence mapping saves.
- Updated flows: text-button navigation without radios, no demo bypass of sign-in, New/Ongoing/Completed transitions and filters, task-to-focus routing, Pomodoro pause/resume and focus-to-break logging, transaction creation/correction/removal driving dashboard metrics, daily schedule persistence/reset, grid time edits, empty recurring routines, and check-ins preserving custom schedules. These tests use an in-memory authenticated-store substitute, never real personal records.
- Added business rules: day overrides replace default blocks, empty schedules clear the routine without deleting separate appointments, invalid schedule backups are rejected, legacy task statuses remain usable, pause/resume preserves remaining time, every fourth interval receives a long break, future transactions are excluded from actuals, transfers are separate from expenses, comparable current periods and full historical months are calculated correctly, and month/year boundaries work.
- Domain rules: protected work/meals/events do not overlap focus suggestions; optical-shop windows conflict with weekday work; approved leave and suitable weekend slots allow the task; low-energy days are capped; zero budgets produce no focus suggestions; past time is not suggested; completed and not-yet-available tasks are excluded.
- Calculations and storage: allocation shortfalls, zero-contribution / achieved-goal cases, recall intervals, SQLite persistence and updates, per-run cache invalidation, and complete backup validation.
- Cloud contract tests with mocked HTTP: user filters and authorization headers are applied; writes/deletes include the correct record/user; historical reads paginate past 500 rows; connection failures are explicit rather than silently replacing data.
- Authored learning materials: seven Python worked solutions pass their supplied checks; the SQL worked solution returns the expected totals including the user with no transactions, using an isolated in-memory SQLite database. Review recommendation and review-date logic pass.
- Python application modules compile successfully.
- Compact navigation changes pages, and touch-friendly schedule forms add/remove blocks. Browser-editor configurations include the correct checks/setup; bounded editor reports reject unknown statuses and malformed values. JavaScript modules pass Node syntax checks.
- The production worker was tested using the same Pyodide 314.0.7 WASM runtime under Node: all seven Python worked solutions and the SQLite exercise pass; syntax errors are returned; run namespaces are independent; runaway execution can be terminated. Run the reproducible check with `node tests/run_runtime_checks.mjs /path/to/installed/pyodide-package` after installing `pyodide@314.0.7` in a separate development directory. This verifies worker execution, not visual rendering.

Test runtime: Python 3.12.14, Streamlit 1.66.1, requests 2.34.2, pandas 2.2.3.

## Not yet verified

- **Live deployment:** the app has an existing deployment at https://becoming.streamlit.app/. Successful local tests do not by themselves verify Streamlit Cloud has completed an update.
- **Live Supabase Auth/RLS:** database schema and request contracts are included, but no user-owned project credentials were supplied. Mocked HTTP tests do not prove a deployed database's policies or cross-device persistence. Follow DEPLOY.md to verify those properties after setup.
- **Visual browser/device QA:** native Light/Dark themes are retained. CSS now restores column stacking and adds explicit tablet/container breakpoints, compact navigation, scrolling tab labels, readable metrics, and card summaries. Actual physical-device and authenticated live-page rendering remain unverified; server-side AppTest does not render CSS. The earlier generated planner image is a design preview, not browser QA evidence.
- **Dart compilation:** the two Dart samples were reviewed for their contracts and edge cases but were not run because this environment did not provide the Dart SDK. Run the included starter/solution checks locally using `dart run FILE.dart`.
- **SQL on PostgreSQL:** the exercise uses shared SQL syntax and passes SQLite checks, but it was not executed against a live PostgreSQL instance.
- **Background notifications and automatic external feeds:** not included. The open app has a live PHT clock, input-driven records and planner updates, explicit refresh, and manual calendar export. It does not notify you while closed or automatically fetch jobs, exam prices, bank balances, or new research.

## Known behavior

Same-record concurrent edits use last saved edit wins. Unfinished timers are session state and may reset on reconnect; completed focus intervals are saved explicitly, and breaks are not logged as work. Cloud personal records require login and a properly configured Supabase table; there is no demo access. Local SQLite mode is only for private local use. No database migration is needed: custom schedules, recurring routines, and task statuses use the existing JSON payloads. Backup imports validate first, then merge by ID; cloud imports are not an atomic multi-record transaction. These limits are explained in README.md and DEPLOY.md.
