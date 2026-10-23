# Becoming

A personal daily workspace for Leila: calm structure, practical growth, and room for an ordinary human day. Built in **Streamlit**, with warm neutral light mode and a matching dark mode.

**Start with `DEPLOY.md` for deployment setup.** Cloud access requires your Supabase email/password account. The public demo entry has been removed. For private development on your own PC, use local mode below.

## What you can do

| Space | Working features |
| --- | --- |
| Today | PHT clock, energy check-in, intention, remaining focus budget, up to three feasible next steps, task completion |
| Planner | Editable daily time blocks, recurring routines, reschedulable appointments, New/Ongoing/Completed task filters, next actions, deadlines, availability dates, time windows, seven-day preview, `.ics` focus calendar export |
| Focus | Pomodoro 25/5, gentle 15/5, deep work 50/10, custom intervals, long breaks, pause/resume, five-minute quick start, focus-only session logging, manual offline entry |
| Coding practice | Eleven original exercises across AI engineering, data engineering, analytics, Python, Dart/Flutter, and SQL/systems, downloadable starters and checks, hints and worked solutions, scheduled practice tasks, attempt log, debugging notebook, review dates |
| Career & learning | AI Engineer, Data Engineer, Data Analytics, and Software Engineering paths in your priority order, official resource links, credential goals and status, recall cards with review dates, project evidence, text export |
| Job market | Dated employer examples, exact experience requirements, opportunity and application tracking, evidence mapping, and practical ways to gain relevant experience |
| Voice & confidence | Thought outlines, technical explanation, career story, question and boundary practice, self-rated clarity and participation history |
| Money | Input-driven dashboard, income/expense/transfer summaries, category chart, daily spending trend, six-month comparisons, plan versus actual, editable transaction log and CSV export, contribution-only savings estimate |
| Reflect | Evening reflection, weekly reset, energy history, logged practice and focus activity |
| Resources | Curated research / professional / official resources, applications and limitations |
| Your space | Name, work pattern, waking day, transitions, target role, refresh, full JSON export / validated restore, record deletion |

## Tailored starting points

- Remote development work: **09:00–18:00 Asia/Manila**. Monday–Friday is an editable assumption, not a confirmed fact.
- Graduation: December 2026 context; a task prompts you to confirm official requirements. No exact school deadline is invented.
- Move: first week of November 2026. **7 November is only a provisional planning target** and is labelled that way. Set the actual date in Planner → Tasks.
- Glasses: 10:00–15:00 shop window. Opening days, appointment availability, travel time, and exact duration are unconfirmed. A weekday visit conflicts with normal work and is not silently scheduled over it.
- Meals start at 08:00–08:30, 12:00–13:00, and 18:00–19:00. Edit the recurring blocks in Your space or change just one day in Planner. Work hours can also be changed per day.
- Money starts with **no assumed salary or account balances**. Enter your current situation.
- No credential, exam result, achievement, or project metric is assumed to be earned.

## Run on your own PC

Install Python **3.11 or 3.12**. This version was tested using Python 3.12.14 and Streamlit 1.66.1.

In VS Code, open this folder and run in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The normal app requires a configured Supabase account. There is no demo button or demo access through session state.

For durable records on your own PC, run these instead after installing dependencies:

```powershell
$env:BECOMING_LOCAL = '1'
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

Or run `run-local.ps1` from your terminal if your PowerShell script policy allows it. On macOS/Linux, `./run-local.sh` creates the environment and starts private local mode. The launchers bind to the local computer. **Do not enable `BECOMING_LOCAL` on a public server.** Local records are not authenticated and are not intended for sharing.

Local records live in `data/becoming.sqlite`. Back up both this file and periodic JSON exports. Streamlit Cloud should use Supabase, not a local SQLite file.

## Your first week

1. **First visit, 10 minutes:** set your workdays and waking day; confirm your move date and school deadlines. Add fixed appointments, including travel time.
2. **Morning, 1 minute:** check in with your actual energy. Choose a realistic number of focus minutes outside work. Fifteen minutes is a valid plan.
3. **After work:** eat and decompress. Follow one suggested step, or start a five-minute action. Logging focus reduces your remaining daily budget.
4. **Learning, two short sessions this week:** use one official resource and create one recall card. Build something small you can explain.
5. **Speaking, a few minutes when feasible:** arrange one thought, try one manageable speaking action, and record what helped. Do not grade yourself by stutter counts.
6. **Money, once this week:** enter actual take-home pay, essentials, near-term move / glasses costs, and an enjoyment amount. Plan savings only from what fits.
7. **Weekly reset:** keep what helped, remove one source of friction, and select one useful project improvement. No broken-streak penalties or comparison leaderboard.

## Scheduling behavior

Plans avoid the time blocks you configure and your appointments. Planner → Day & week → Your schedule lets you add, edit, or delete blocks for a selected date. Saving an empty schedule intentionally clears the routine for that date. Reset restores your recurring routine. Day off excludes Work blocks. Appointments stay separate and can be edited or rescheduled in their tab. Your space controls recurring workdays, work hours, and meal/personal blocks. Daily overrides are preserved when the routine changes.

Saved daily schedules also feed Today and the seven-day preview. Tasks use New, Ongoing, and Completed statuses; older unfinished records appear as New. A five-minute task start marks it Ongoing. Tasks with time windows need a full-duration slot; other tasks can receive a focus slice. Completing a slice does not complete the whole task.

Focus intervals use wall time and can be paused. Completed intervals are saved only when you choose to save them; Pomodoro then starts a short or long break. Breaks are not logged as worked minutes. Returning from another page preserves the active timer within that session, but reloading, reconnecting, signing out, or a server restart may lose it. Old active timers are upgraded as single focus sessions.

The Money dashboard updates after each saved ledger or budget entry. Net logged cash flow subtracts expenses and savings/investment transfers from logged income; it is not a bank balance. Charts exclude future-dated entries. Daily zeroes mean no expenses logged. Current-month spending compares to the same number of calendar days in the previous month; complete historical months compare to the complete prior month. Savings and investment transfers are shown separately from expenses.

The planner prioritizes tasks due within three days, then importance and deadline. Low energy caps suggestions at one short step; ordinary energy permits at most three. Capacity limits and transition buffers are **transparent product heuristics**, not diagnostic tools or claims about ideal productivity. A budget is not a promise that a free slot exists.

Each date in the seven-day view is an independent preview. Unfinished tasks can appear on several days. There is no automatic multi-day allocation or hidden rescheduling. Move a task with “Available from,” change its duration, or mark it done.

## Current information and sync

The PHT clock updates once a minute while the app is open and rolls the app to a new day at midnight. The focus timer uses wall-clock elapsed time. Personal records are reloaded on interactions; use Refresh to fetch changes made on another device. This is not background calendar sync or an internet-wide live recommendation feed. Curated resources were checked on **23 October 2026**, with current official links for rechecking.

Cloud authentication and row security separate each account. No cross-user Streamlit data cache is used. Reads are cached only within a single script run. Same-record concurrent editing uses **last saved edit wins**; avoid editing the same record on two devices simultaneously.

A JSON restore validates all rows before writing, then merges by ID. Cloud restore consists of separate requests: a network failure can leave a partial restore. Re-upload the same backup to resume; repeated IDs update records rather than duplicate them. Download a fresh backup first. Imports do not delete records absent from the file.

## Privacy and scope

No paid AI API, advertisement, external analytics, bank connection, microphone capture, automated recruiter scoring, or language-model processing is included. Passwords are checked through your configured Supabase Auth endpoint; tokens remain in the current server session and are not written to application files. Your records are stored in your own database with row-level security. Do not commit `secrets.toml`, local databases, or personal backups to GitHub.

The app supports reflection and communication practice. It cannot diagnose or treat stuttering or guarantee confidence, certification success, or recruiter interest. A speech-language pathologist can help with persistent speech difficulties. The money tools perform educational cash-flow calculations and assume no investment returns.

## Design decisions

The supplied reference principles informed a single primary task on Today, clear type hierarchy, repeated card patterns, large tap targets, readable contrast, whitespace, visible instructions, progressive disclosure, and minimal initial navigation work. There are no fabricated reviews, social-proof counts, streak punishments, or urgent red/yellow dashboard states. Native Streamlit layouts stack columns on smaller screens; wide tables keep their own horizontal scroll. Both themes preserve page scrolling. Reduced-motion preferences are respected.

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests cover editable scheduling, energy limits, task transitions, Pomodoro timing, transfer accounting, budget edge cases, local persistence, recall intervals, backup validation, cloud request scoping and pagination, plus Streamlit text navigation and core forms. See `VALIDATION.md` for the actual result and limits. A configured live Supabase project and a real phone/tablet check are still required during deployment.

## Project layout

- `app.py`: Streamlit interface and flows
- `domain.py`: scheduling, budget, and review rules
- `coding.py`: original coding challenges, starter-file generation, and review suggestions
- `storage.py`: SQLite, authenticated cloud storage, in-memory test store, backup validation
- `focus_timer.py`: focus/break intervals, pause/resume, and elapsed-time arithmetic
- `money_analytics.py`: ledger totals, monthly comparisons, categories, and plan-versus-actual calculations
- `ui.py`: neutral theme, cards, responsive typography
- `content.py`: cited resources, paths, and exercise prompts
- `supabase_schema.sql`: user-owned records and RLS policy
- `DEPLOY.md`: account/database/Streamlit setup
- `tests/`: business rules, cloud contract tests, and Streamlit AppTest flows

## Coding practice workflow

Choose one track in Coding practice. Attempt an exercise in VS Code, run the supplied checks, explain one edge case, and save your approach. The app never executes submitted code on its server. Results are self-reported; a saved entry is not a verified assessment. Python and Dart exercise files are standalone. Use a disposable database for the SQL exercise. The API exercise is a design note rather than an executable task.

Hints, documentation, AI, and reviewers can help; record the support you used. Return to the concept later without copying. Review prompts appear after one day when help was used or checks were not passed, and after three days for a self-reported independent passing attempt. These are simple practice heuristics. Use “Add a 15-minute coding task” to fit practice into the same capacity-limited daily plan. Logging coding minutes can also log focus; leave that option off if the focus timer already logged those minutes.

The download includes `practice_starters/` and `worked_solutions/` for offline use. Work from the starter first, then compare explanations. Dart examples were reviewed but not executed in the build environment because the Dart SDK was unavailable.

## Your confirmed career priorities

AI Engineer is first, followed by Data Engineer, Data Analytics, and Software Engineering. Coding defaults to AI engineering and includes model evaluation, repeatable batch loading, and analytical denominators alongside the existing foundations. Your resume informs starting strengths; it is not an independently verified skills assessment. See `CAREER-AND-MARKET.md` for the dated employer research and the distinction between professional work, internships, and project evidence. The original resume and its private contact details are not included in this source package.

For an existing database, rerun `supabase_schema.sql` to allow the new `jobs` record category. Existing records remain in place. The app upgrades the earlier generated “Backend / AI application developer” default to AI Engineer while preserving a target you customized.

## Appearance

Use the app’s upper-right menu → Settings → Theme → Light or Dark. This single native theme controls widgets, tables, menus, charts, and the custom cards together. The earlier sidebar CSS-only toggle was removed because it could leave controls in a conflicting palette. Text and button labels wrap, cards have no fixed text heights, and the main content clears the fixed header.
