"""Scheduling and budgeting rules, independent of Streamlit."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import math
import uuid

TZ = ZoneInfo('Asia/Manila')
AREAS = ['Life admin', 'Graduation', 'Career', 'Learning', 'Voice & confidence', 'Wellbeing']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def now():
    return datetime.now(TZ)


def uid():
    return uuid.uuid4().hex


def minute(value):
    h, m = value.split(':')[:2]
    return int(h) * 60 + int(m)


def clock(value):
    return f'{value // 60:02d}:{value % 60:02d}'


def default_profile():
    return {'id': 'main', 'name': 'Leila', 'role': 'Application developer',
            'work_start': '09:00', 'work_end': '18:00', 'workdays': DAYS[:5],
            'wake': '07:00', 'sleep': '22:30', 'buffer': 10, 'target_role': 'AI Engineer',
            'coding_track': 'AI engineering'}


def seed_tasks():
    # Planning targets are explicitly provisional; exact deadlines were not supplied.
    return [
        {'id': 'graduation', 'title': 'Confirm my graduation requirements', 'area': 'Graduation', 'next': 'Open the school checklist and list missing documents.', 'minutes': 25, 'priority': 3, 'due': None, 'note': 'Graduation planned for December 2026. Confirm each official deadline.', 'done': False, 'window': None, 'not_before': None},
        {'id': 'moving', 'title': 'Prepare to leave the dorm', 'area': 'Life admin', 'next': 'Confirm the move date and transport; pack one small box.', 'minutes': 25, 'priority': 3, 'due': '2026-11-07', 'note': 'Provisional end of the first week of November. Replace with your confirmed move date.', 'done': False, 'window': None, 'not_before': None},
        {'id': 'glasses', 'title': 'Arrange my glasses repair', 'area': 'Life admin', 'next': 'Confirm shop opening days, appointment needs, and travel time.', 'minutes': 60, 'priority': 2, 'due': None, 'note': 'Shop hours 10:00–15:00 PHT. Opening days and total travel time still need confirmation. Weekday visit needs approved work leave.', 'done': False, 'window': ['10:00', '15:00'], 'not_before': None},
    ]


def subtract_intervals(start, end, blocked):
    gaps = [(start, end)]
    for lo, hi in sorted(blocked):
        updated = []
        for a, b in gaps:
            if hi <= a or lo >= b:
                updated.append((a, b))
            else:
                if a < lo:
                    updated.append((a, min(lo, b)))
                if hi < b:
                    updated.append((max(hi, a), b))
        gaps = updated
    return gaps


def routine_blocks(profile):
    return profile.get('routine', [
        {'start':480,'end':510,'title':'Breakfast','kind':'rest'},
        {'start':720,'end':780,'title':'Lunch / break','kind':'rest'},
        {'start':1080,'end':1140,'title':'Dinner & decompress','kind':'rest'},
    ])


def validate_schedule(blocks):
    if not isinstance(blocks, list) or len(blocks)>100:
        raise ValueError('Use up to 100 time blocks.')
    for b in blocks:
        if not isinstance(b,dict) or not isinstance(b.get('title'),str) or not b['title'].strip():
            raise ValueError('Every time block needs an activity name.')
        if any(type(b.get(k)) is not int for k in ['start','end']) or not 0<=b['start']<b['end']<1440:
            raise ValueError('Each block needs an end after its start. Split overnight blocks into two days.')
        if b.get('kind') not in ['work','rest','personal']:
            raise ValueError('Choose Work, Rest, or Personal for each block.')
    return blocks


def task_status(task):
    # Old records remain compatible with the original completion checkbox.
    return 'Completed' if task.get('done') else 'Ongoing' if task.get('status')=='Ongoing' else 'New'


def day_blocks(profile, selected, events, leave=False, schedule=None):
    blocks = [dict(b) for b in schedule] if schedule is not None else [dict(b) for b in routine_blocks(profile)]
    if schedule is None and DAYS[selected.weekday()] in profile['workdays']:
        blocks.append({'start': minute(profile['work_start']), 'end': minute(profile['work_end']), 'title': 'Remote work', 'kind': 'work'})
    if leave:
        blocks=[b for b in blocks if b['kind']!='work']
    for e in events:
        if e['date'] == selected.isoformat():
            blocks.append({'start': minute(e['start']), 'end': minute(e['end']), 'title': e['title'], 'kind': 'event'})
    return sorted(blocks, key=lambda b:b['start'])


def rank_tasks(tasks, selected):
    active = [t for t in tasks if not t.get('done') and (not t.get('not_before') or t['not_before'] <= selected.isoformat())]
    def score(t):
        days = (date.fromisoformat(t['due']) - selected).days if t.get('due') else 9999
        return (0 if days <= 3 else 1, days if days <= 3 else 0, -t.get('priority', 2), days, t['title'])
    return sorted(active, key=score)


def make_plan(profile, selected, tasks, events, budget=45, energy=3, leave=False, current=None, schedule=None):
    blocks = day_blocks(profile, selected, events, leave, schedule)
    start, end = minute(profile['wake']), minute(profile['sleep'])
    current = current or now()
    if selected == current.date():
        start = max(start, current.hour * 60 + current.minute + 1)
    gaps = subtract_intervals(start, end, [(b['start'], b['end']) for b in blocks])
    # Low-energy days use one small step. The multiplier is a product heuristic, not a clinical scale.
    cap = min(int(budget), 15 if energy <= 2 else 60 if energy == 3 else 90)
    remaining = cap
    plan, deferred = [], []
    for t in rank_tasks(tasks, selected):
        if remaining <= 0 or len(plan) >= (1 if energy <= 2 else 3):
            deferred.append((t, 'Outside today’s focus budget; available for another day.'))
            continue
        # Errands need their full duration; knowledge tasks can take one small slice.
        duration = int(t['minutes']) if t.get('window') else min(int(t['minutes']), 25, remaining)
        win = t.get('window')
        found = False
        for i, (a, b) in enumerate(gaps):
            lo = max(a, minute(win[0])) if win else a
            hi = min(b, minute(win[1])) if win else b
            if duration <= remaining and lo + duration <= hi:
                plan.append({**t, 'start': lo, 'end': lo + duration, 'slice': duration < int(t['minutes'])})
                gaps = subtract_intervals(start, end, [(x['start'], x['end']) for x in blocks] + [(x['start'], x['end'] + profile['buffer']) for x in plan])
                remaining -= duration
                found = True
                break
        if not found:
            reason = 'No free slot within the task’s time window and focus budget.' if win else 'No free slot within today’s focus budget.'
            deferred.append((t, reason))
    return {'blocks': blocks, 'plan': plan, 'deferred': deferred, 'capacity': cap, 'used': cap - remaining}


def budget_summary(budget):
    income = float(budget.get('income', 0))
    allocated = sum(float(budget.get(k, 0)) for k in ['needs','joy','buffer','learning','emergency','investing'])
    return {'income': income, 'allocated': allocated, 'remaining': round(income - allocated, 2)}


def months_to_goal(current, target, monthly):
    if current >= target:
        return 0
    return math.ceil((target-current)/monthly) if monthly > 0 else None


def next_review(previous_interval, recalled, selected):
    interval = min(60, max(1, previous_interval * 2)) if recalled else 1
    return interval, (selected + timedelta(days=interval)).isoformat()
