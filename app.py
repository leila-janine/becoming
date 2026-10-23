from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
import json
import os
import time

import pandas as pd
import requests
import streamlit as st

from content import SOURCES, TRACKS, PROMPTS, WEEKLY_PROMPTS, CAREER_PRIORITIES, RESUME_FOUNDATIONS
from career import CHECKED_ON, JOB_EXAMPLES, EVIDENCE_TYPES, EXPERIENCE_BRIDGES
from coding import CHALLENGES, practice_file, recommend, review_date
from domain import (TZ, AREAS, DAYS, now, uid, minute, clock, default_profile, seed_tasks,
                    make_plan, day_blocks, budget_summary, months_to_goal, next_review,
                    routine_blocks, validate_schedule, task_status)
from focus_timer import start_timer, remaining, pause, resume, advance
from money_analytics import money_dashboard
from storage import (LocalStore, CloudStore, StorageError, auth_request,
                     get_record, export_records, COLLECTIONS, RunStore, validate_backup)
from ui import style, hero, card, gentle, stat, esc

st.set_page_config(page_title='Becoming · your daily space', page_icon='🌿', layout='wide')
ROOT = Path(__file__).parent
TODAY = now().date()


def secret(name):
    try:
        return st.secrets.get(name, os.environ.get(name, ''))
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return os.environ.get(name, '')


@st.fragment(run_every='60s')
def live_clock():
    stamp=now()
    st.caption(stamp.strftime('%a %d %b · %I:%M %p PHT'))
    if stamp.date()!=TODAY:
        st.rerun(scope='app')


def save(collection, row):
    store.put(collection, row)
    st.toast('Saved.')


def initialize():
    if not store.all('profile'):
        store.put('profile', default_profile())
        for task in seed_tasks():
            store.put('tasks', task)
    # Upgrade only the old generated default; preserve a target the user customized.
    existing=get_record(store,'profile','main',{})
    if existing.get('target_role')=='Backend / AI application developer':
        store.put('profile',{**existing,'target_role':'AI Engineer','coding_track':'AI engineering'})


def records(collection):
    return store.all(collection)


def complete(task):
    saved=get_record(store,'tasks',task['id'],task)
    save('tasks', {**saved, 'done': True, 'status':'Completed', 'completed_at': now().isoformat()})
    st.rerun()


def quick_start(title, task_id=None):
    if not st.session_state.get('timer'):
        st.session_state.timer = start_timer(title,5,pomodoro=False)
        if task_id:
            task=get_record(store,'tasks',task_id)
            if task and not task.get('done'): store.put('tasks',{**task,'status':'Ongoing'})
    st.session_state.page = 'Focus'


def navigate(page):
    st.session_state.page=page


def plan_for(day, check, budget=None, energy=None, leave=None):
    logged=sum(s.get('minutes',0) for s in records('sessions') if s['date']==day.isoformat())
    return make_plan(profile,day,records('tasks'),records('events'),
                     max(0,(check.get('minutes',45) if budget is None else budget)-logged),
                     check.get('energy',3) if energy is None else energy,
                     check.get('leave',False) if leave is None else leave,
                     schedule=check.get('schedule'))


def label_date(value):
    return date.fromisoformat(value).strftime('%b %d, %Y') if value else 'No exact deadline'


def authenticate():
    url, key = secret('SUPABASE_URL'), secret('SUPABASE_ANON_KEY')
    if os.environ.get('BECOMING_LOCAL') == '1':
        return LocalStore(ROOT / 'data' / 'becoming.sqlite')
    if url and key and st.session_state.get('auth'):
        session = st.session_state.auth
        if session.get('expires_at', 0) <= time.time() + 60:
            try:
                session = auth_request(url, key, {'refresh_token':session['refresh_token']}, 'refresh_token')
                st.session_state.auth = session
            except StorageError:
                st.session_state.pop('auth', None)
                st.info('Your session ended. Sign in again to continue.')
                st.stop()
        return CloudStore(url, key, session)
    hero('A little more you, every day', 'Welcome to Becoming.', 'A quiet place to make room for your work, your goals, and yourself. Start with what is possible today.')
    left, right = st.columns([1.2, 1], gap='large')
    with left:
        card('Structure with room to breathe', 'Plan around your commitments. Build your skills. Practice your voice. Make money decisions with more clarity.', 'PLAN · GROW · REFLECT')
        gentle('You do not have to earn rest or kindness. Progress can be small and still count.')
    with right:
        if url and key:
            with st.form('signin'):
                st.subheader('Your personal space')
                email = st.text_input('Email', autocomplete='email')
                password = st.text_input('Password', type='password', autocomplete='current-password')
                if st.form_submit_button('Sign in', type='primary', width='stretch'):
                    try:
                        st.session_state.auth = auth_request(url, key, {'email':email.strip(),'password':password})
                        st.rerun()
                    except StorageError as exc:
                        st.error(str(exc))
            st.caption('Use the account created in your Supabase project. Reset a forgotten password through your project administrator.')
        else:
            st.info('Your personal space is being connected. Add SUPABASE_URL and SUPABASE_ANON_KEY in the app’s Streamlit secrets to enable sign-in.')
    st.stop()


def today_page():
    hour = now().hour
    greeting = 'Good morning' if hour < 12 else 'Good afternoon' if hour < 18 else 'Good evening'
    hero(TODAY.strftime('%A, %d %B %Y')+' · Philippine time', f'{greeting}, {profile["name"]}.', 'You do not need to change everything today. Choose a small, honest step and give it your attention.')
    check = get_record(store, 'checkins', TODAY.isoformat(), {'energy':3,'minutes':45,'intention':''})
    with st.expander('Start here · a 30-second check-in', expanded=not bool(check.get('saved_at'))):
        with st.form('checkin'):
            a, b = st.columns(2)
            energy = a.select_slider('Energy today', options=[1,2,3,4,5], value=int(check['energy']), format_func=lambda x:{1:'1 · very low',2:'2 · low',3:'3 · steady',4:'4 · good',5:'5 · high'}[x])
            budget = b.number_input('Focus minutes outside work', min_value=0, max_value=240, value=int(check['minutes']), step=5)
            intention = st.text_input('What would make today feel worthwhile?', value=check.get('intention',''), placeholder='One thing that matters, even if it is small.')
            if st.form_submit_button('Shape my day', type='primary'):
                save('checkins', {**check,'id':TODAY.isoformat(),'energy':energy,'minutes':budget,'intention':intention,'saved_at':now().isoformat()})
                st.rerun()
    tasks, events = records('tasks'), records('events')
    done = [t for t in tasks if t.get('completed_at','').startswith(TODAY.isoformat()) and t.get('done')]
    study = sum(x.get('minutes',0) for x in records('sessions') if x['date']==TODAY.isoformat())
    plan = plan_for(TODAY, check)
    a,b,c = st.columns(3)
    with a: stat(f'{len(done)}', 'steps finished today')
    with b: stat(f'{plan["used"]} min', 'suggested focus outside work')
    with c: stat(f'{study} min', 'focus you have logged today')
    main, side = st.columns([1.6,1], gap='large')
    with main:
        st.subheader('Your next small steps')
        st.caption('Up to three suggestions, based on deadlines, energy, time windows, and your remaining day. You choose what to do.')
        if not plan['plan']:
            gentle('There is no suitable focus slot left in this plan. Rest, adjust your availability, or choose a smaller step for another day.')
        for i,t in enumerate(plan['plan']):
            with st.container(border=True):
                st.caption(f'{i+1:02d}  /  {t["area"].upper()}  ·  {clock(t["start"])}–{clock(t["end"])} PHT')
                st.markdown(f'### {t["title"]}')
                st.write(t['next'])
                if t['slice']: st.caption('This is a focus slice, not the whole task. Mark the task done only when it is finished.')
                a,b=st.columns(2)
                a.button('Start a 5-minute step', key='start_'+t['id'], width='stretch',on_click=quick_start,args=(t['title'],t['id']))
                if b.button('Mark task done',key='done_'+t['id'],width='stretch'): complete(t)
        if plan['deferred']:
            with st.expander(f'{len(plan["deferred"])} other tasks · no need to do them all today'):
                for t,reason in plan['deferred']:
                    st.markdown(f'**{t["title"]}**')
                    st.caption(reason)
                    if t.get('window'): st.caption('Optical shop: 10am–3pm. Confirm opening days and travel, or arrange approved leave before a weekday visit.')
    with side:
        st.subheader('The shape of today')
        schedule = sorted(plan['blocks'] + [{'start':t['start'],'end':t['end'],'title':t['title'],'kind':'focus'} for t in plan['plan']],key=lambda x:x['start'])
        for block in schedule:
            if block['end'] <= now().hour*60+now().minute: continue
            st.markdown(f'<div class="timeline"><div class="time">{clock(block["start"])} – {clock(block["end"])} PHT</div><p><strong>{esc(block["title"])}</strong></p><div class="time">{esc(block["kind"].title())}</div></div>',unsafe_allow_html=True)
        st.caption('Edit today’s time blocks in Planner. Your saved schedule guides focus suggestions here.')
        card('A small promise', 'If I notice myself waiting to feel ready, I will open the task and do its first five minutes.', 'TRY AN IF–THEN PLAN')
        gentle('A difficult day is information. Tomorrow’s plan can be smaller.')


def task_form(task=None):
    t = task or {'id':uid(),'title':'','area':'Life admin','next':'','minutes':25,'priority':2,'due':None,'note':'','done':False,'window':None,'not_before':None}
    with st.form('task_'+(t['id'] if task else 'new')):
        title=st.text_input('Task',value=t['title'])
        action=st.text_input('Smallest useful next action',value=t['next'])
        a,b,c=st.columns(3)
        area=a.selectbox('Area',AREAS,index=AREAS.index(t['area']))
        minutes=b.number_input('Estimated total minutes',5,480,int(t['minutes']),5)
        priority=c.selectbox('Importance',[1,2,3],index=int(t['priority'])-1,format_func=lambda n:{1:'Useful',2:'Important',3:'Essential'}[n])
        status=st.selectbox('Task status',['New','Ongoing','Completed'],index=['New','Ongoing','Completed'].index(task_status(t)))
        due=st.date_input('Deadline (clear if unknown)',value=date.fromisoformat(t['due']) if t.get('due') else None)
        not_before=st.date_input('Available from (optional)',value=date.fromisoformat(t['not_before']) if t.get('not_before') else None)
        note=st.text_area('Notes / unconfirmed details',value=t.get('note',''))
        window=st.checkbox('Needs a specific time window',value=bool(t.get('window')))
        a,b=st.columns(2)
        wstart=a.time_input('Earliest start',value=dtime.fromisoformat(t['window'][0]) if t.get('window') else dtime(10))
        wend=b.time_input('Latest finish',value=dtime.fromisoformat(t['window'][1]) if t.get('window') else dtime(15))
        if st.form_submit_button('Save task',type='primary'):
            if not title.strip() or not action.strip(): st.info('Add a task and a concrete next action.')
            elif window and wend<=wstart: st.info('The time window must end after it starts.')
            elif due and not_before and not_before>due: st.info('Availability must start on or before the deadline.')
            else:
                save('tasks',{**t,'title':title.strip(),'next':action.strip(),'area':area,'minutes':minutes,'priority':priority,'status':status,'done':status=='Completed','completed_at':(t.get('completed_at') or now().isoformat()) if status=='Completed' else '', 'due':due.isoformat() if due else None,'not_before':not_before.isoformat() if not_before else None,'note':note,'window':[wstart.strftime('%H:%M'),wend.strftime('%H:%M')] if window else None})
                st.rerun()


def schedule_editor(blocks, key):
    kinds={'work':'Work','rest':'Rest','personal':'Personal'}
    rows=[{'Activity':b['title'],'Start':dtime(b['start']//60,b['start']%60),
           'End':dtime(b['end']//60,b['end']%60),'Kind':kinds[b['kind']]} for b in blocks]
    frame=pd.DataFrame(rows,columns=['Activity','Start','End','Kind'])
    return st.data_editor(frame,hide_index=True,num_rows='dynamic',width='stretch',key=key,
        column_config={'Activity':st.column_config.TextColumn(required=True),
                       'Start':st.column_config.TimeColumn('Start (PHT)',format='HH:mm',required=True,step=60),
                       'End':st.column_config.TimeColumn('End (PHT)',format='HH:mm',required=True,step=60),
                       'Kind':st.column_config.SelectboxColumn(options=['Work','Rest','Personal'],default='Personal',required=True)})


def schedule_rows(frame):
    blocks=[]
    for row in frame.to_dict('records'):
        if not isinstance(row['Activity'],str) or not row['Activity'].strip() or not isinstance(row['Start'],dtime) or not isinstance(row['End'],dtime):
            raise ValueError('Give each row an activity, start, and end, or delete the unused row.')
        blocks.append({'title':row['Activity'].strip(),'start':row['Start'].hour*60+row['Start'].minute,
                       'end':row['End'].hour*60+row['End'].minute,'kind':str(row.get('Kind','Personal')).lower()})
    return validate_schedule(blocks)


def planner_page():
    hero('Make room for what matters', 'A plan that fits your life.', 'Keep your commitments visible. Leave enough space for meals, transitions, and life happening.')
    tab1,tab2,tab3=st.tabs(['Day & week','Tasks','Appointments'])
    with tab1:
        selected=st.date_input('Plan for',value=TODAY)
        check=get_record(store,'checkins',selected.isoformat(),{'energy':3,'minutes':45})
        a,b,c=st.columns(3)
        energy=a.select_slider('Planning energy',[1,2,3,4,5],value=int(check['energy']))
        budget=b.number_input('Focus budget (minutes)',0,240,int(check['minutes']),5)
        leave=c.checkbox('Day off from work',value=bool(check.get('leave',False)),help='Excludes blocks marked Work from this day’s plan. You can also edit individual work hours below.')
        if st.button('Save this day’s capacity'):
            save('checkins',{**check,'id':selected.isoformat(),'energy':energy,'minutes':budget,'leave':leave,'saved_at':now().isoformat()})
            st.rerun()
        st.markdown('#### Your schedule')
        st.caption('Change any block when your day changes. Add a row at the bottom; select a row to delete it. Appointments are managed in the Appointments tab.')
        if check.get('schedule') is not None: st.caption('Using your custom schedule for this date.')
        else: st.caption('Starting from your recurring routine in Your space.')
        with st.form('schedule_'+selected.isoformat()):
            edited=schedule_editor(check.get('schedule') if check.get('schedule') is not None else day_blocks(profile,selected,[]),
                                   f'daily_schedule_{selected}_{check.get("schedule_version",0)}')
            if st.form_submit_button('Save schedule',type='primary'):
                try:
                    blocks=schedule_rows(edited)
                    save('checkins',{**check,'id':selected.isoformat(),'schedule':blocks,'schedule_version':check.get('schedule_version',0)+1})
                    st.rerun()
                except ValueError as exc: st.info(str(exc))
        if st.button('Reset this day to my routine'):
            updated={k:v for k,v in check.items() if k!='schedule'}
            save('checkins',{**updated,'id':selected.isoformat(),'schedule_version':check.get('schedule_version',0)+1})
            st.rerun()
        plan=plan_for(selected,check,budget,energy,leave)
        if selected<TODAY: st.caption('Historical planning view. This does not recreate previously suggested schedules.')
        for i,block in enumerate(plan['blocks']):
            for other in plan['blocks'][:i]:
                if block['start']<other['end'] and other['start']<block['end'] and not ({block['kind'],other['kind']}=={'work','rest'}):
                    st.caption(f'Time overlap: {block["title"]} and {other["title"]}. Edit the blocks if these need separate time.')
        st.markdown('#### Suggested focus')
        for t in plan['plan']: card(t['title'],t['next'],f'{clock(t["start"])}–{clock(t["end"])} PHT · {t["area"]}')
        if not plan['plan']: gentle('No free focus slot fits. Try a smaller task, another day, or a different focus budget.')
        for t,reason in plan['deferred']:
            st.caption(f'{t["title"]}: {reason}')
        st.markdown('#### The next seven days')
        rows=[]
        for i in range(7):
            day=selected+timedelta(days=i)
            ch=get_record(store,'checkins',day.isoformat(),{'energy':3,'minutes':45})
            p=plan_for(day,ch)
            work=', '.join(clock(b['start'])+'–'+clock(b['end']) for b in p['blocks'] if b['kind']=='work') or 'Off'
            rows.append({'Day':day.strftime('%a %d %b'),'Work':work,'Focus suggestions':', '.join(x['title'] for x in p['plan']) or 'Open / rest','Minutes':p['used']})
        st.dataframe(pd.DataFrame(rows),hide_index=True,width='stretch')
        st.caption('Each day is an independent preview, so an unfinished task may appear more than once. Mark it complete or change “Available from” to move it.')
        ics=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Becoming//Personal planner//EN']
        def clean(value): return str(value).replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,')
        for t in plan['plan']:
            start=datetime.combine(selected,dtime(t['start']//60,t['start']%60),TZ).astimezone(__import__('datetime').timezone.utc)
            end=datetime.combine(selected,dtime(t['end']//60,t['end']%60),TZ).astimezone(__import__('datetime').timezone.utc)
            ics.extend(['BEGIN:VEVENT',f'UID:{t["id"]}-{selected.isoformat()}@becoming',f'DTSTAMP:{now().astimezone(__import__("datetime").timezone.utc).strftime("%Y%m%dT%H%M%SZ")}',f'DTSTART:{start.strftime("%Y%m%dT%H%M%SZ")}',f'DTEND:{end.strftime("%Y%m%dT%H%M%SZ")}',f'SUMMARY:{clean(t["title"])}',f'DESCRIPTION:{clean(t["next"])}','END:VEVENT'])
        ics.append('END:VCALENDAR')
        st.download_button('Download this day’s focus calendar','\r\n'.join(ics)+'\r\n',f'becoming-{selected}.ics','text/calendar')
        st.caption('Calendar export is manual. This app does not send reminders while closed.')
    with tab2:
        with st.expander('Add a task'): task_form()
        view=st.selectbox('Filter status',['New','Ongoing','Completed'])
        visible=[t for t in records('tasks') if task_status(t)==view]
        if not visible: gentle(f'No {view.lower()} tasks here. Change the filter or add your next step.')
        for t in visible:
            with st.expander(t['title']+' · '+view+' · '+label_date(t.get('due'))):
                st.caption(t.get('note',''))
                a,b=st.columns(2)
                next_status={'New':'Ongoing','Ongoing':'Completed','Completed':'New'}[view]
                if a.button({'New':'Start task','Ongoing':'Mark completed','Completed':'Reopen task'}[view],key='toggle'+t['id']):
                    save('tasks',{**t,'status':next_status,'done':next_status=='Completed','completed_at':now().isoformat() if next_status=='Completed' else ''}); st.rerun()
                if view!='Completed': b.button('Focus on this task',key='taskfocus'+t['id'],on_click=quick_start,args=(t['title'],t['id']))
                task_form(t)
    with tab3:
        with st.form('event'):
            title=st.text_input('Appointment or personal commitment')
            day=st.date_input('Date',value=TODAY,key='eventday')
            a,b=st.columns(2)
            start=a.time_input('Start (PHT)',value=dtime(19))
            end=b.time_input('End (PHT)',value=dtime(20))
            if st.form_submit_button('Add commitment',type='primary'):
                if not title.strip() or end<=start: st.info('Add a title and an end time after the start. Split overnight commitments into two days.')
                else:
                    save('events',{'id':uid(),'title':title.strip(),'date':day.isoformat(),'start':start.strftime('%H:%M'),'end':end.strftime('%H:%M')}); st.rerun()
        for e in sorted(records('events'),key=lambda x:(x['date'],x['start'])):
            with st.container(border=True):
                st.write(f'{label_date(e["date"])} · {e["start"]}–{e["end"]} · {e["title"]}')
                with st.form('event_edit_'+e['id']):
                    title=st.text_input('Activity',e['title'])
                    day=st.date_input('Reschedule date',date.fromisoformat(e['date']))
                    a,b=st.columns(2)
                    start=a.time_input('Starts (PHT)',dtime.fromisoformat(e['start']))
                    end=b.time_input('Ends (PHT)',dtime.fromisoformat(e['end']))
                    if st.form_submit_button('Save appointment'):
                        if not title.strip() or end<=start: st.info('Add an activity and an end after the start.')
                        else:
                            save('events',{**e,'title':title.strip(),'date':day.isoformat(),'start':start.strftime('%H:%M'),'end':end.strftime('%H:%M')}); st.rerun()
                if st.button('Remove commitment',key='evdel'+e['id']): store.delete('events',e['id']); st.rerun()


@st.fragment(run_every='1s')
def running_timer():
    timer=st.session_state.get('timer')
    if not timer: return
    seconds=remaining(timer)
    st.caption(f'{timer["phase"].upper()} · ROUND {timer["round"]}'+(' · PAUSED' if timer.get('paused') else ''))
    st.markdown(f'<div class="timer-face" role="timer" aria-label="{timer["phase"]} time remaining">{seconds//60:02d}:{seconds%60:02d}</div>',unsafe_allow_html=True)
    st.progress(min(1.,max(0.,1-seconds/timer['duration'])))
    st.write(timer['title'])
    if seconds==0:
        if timer['phase']=='Focus':
            gentle('Your focus interval is complete. Save it, then take a break. Breaks are not counted as focus time.')
            label='Save focus & start break' if timer['pomodoro'] else 'Save focus session'
            if st.button(label,type='primary'):
                save('sessions',{'id':timer['id']+'-'+str(timer['round']),'date':now().date().isoformat(),'minutes':timer['minutes'],'title':timer['title']})
                if timer['pomodoro']: st.session_state.timer=advance(timer)
                else: st.session_state.pop('timer',None)
                st.rerun()
        else:
            gentle('Break complete. Choose one small next action when you are ready.')
            if st.button('Start next focus interval',type='primary'):
                st.session_state.timer=advance(timer); st.rerun()
    else:
        a,b=st.columns(2)
        if a.button('Resume' if timer.get('paused') else 'Pause',width='stretch'):
            st.session_state.timer=resume(timer) if timer.get('paused') else pause(timer)
            st.rerun()
        if timer['phase']!='Focus' and b.button('Skip break',width='stretch'):
            st.session_state.timer=advance(timer); st.rerun()
    if st.button('End timer without logging'):
        st.session_state.pop('timer',None); st.rerun()


def focus_page():
    hero('One thing at a time', 'A little focus. A real break.', 'Choose one action, give it a short interval, then step away. Adjust the rhythm to your energy.')
    a,b=st.columns([1.3,1],gap='large')
    with a:
        if st.session_state.get('timer'): running_timer()
        else:
            technique=st.selectbox('Focus rhythm',['Pomodoro · 25 / 5','Gentle start · 15 / 5','Deep work · 50 / 10','Custom Pomodoro','Single focus session'])
            with st.form('focus'):
                title=st.text_input('What will I work on?',placeholder='Open the file and write one paragraph.')
                presets={'Pomodoro · 25 / 5':(25,5),'Gentle start · 15 / 5':(15,5),'Deep work · 50 / 10':(50,10)}
                mins,short=presets.get(technique,(25,5))
                if technique in ['Custom Pomodoro','Single focus session']:
                    mins=st.number_input('Focus minutes',1,120,25)
                if technique=='Custom Pomodoro': short=st.number_input('Short break minutes',1,60,5)
                long=st.number_input('Long break minutes',1,60,15,disabled=technique=='Single focus session')
                every=st.number_input('Long break after this many focus intervals',1,8,4,disabled=technique=='Single focus session')
                if technique!='Single focus session': st.caption(f'{mins} minutes focus → {short} minutes rest. Take a {long}-minute break after every {every} focus intervals.')
                if st.form_submit_button('Begin focus',type='primary'):
                    if not title.strip(): st.info('Name one concrete action first.')
                    else:
                        st.session_state.timer=start_timer(title.strip(),mins,short,long,every,technique!='Single focus session'); st.rerun()
        st.caption('Pause or resume any interval. Save a finished focus interval to log it and begin its break. The timer continues across pages in this session; a reload or sign-out may reset it. No alerts are sent while the app is closed.')
        with st.expander('Already focused offline? Log it here'):
            with st.form('manual_focus'):
                title=st.text_input('What did you work on?')
                day=st.date_input('Session date',value=TODAY,max_value=TODAY)
                mins=st.number_input('Minutes worked',1,480,15)
                if st.form_submit_button('Log focus'):
                    if title.strip(): save('sessions',{'id':uid(),'date':day.isoformat(),'minutes':mins,'title':title.strip()}); st.rerun()
    with b:
        card('Your focus rhythm', 'Work on one action. When the timer finishes, save the interval and take your break. After four focus intervals, take a longer break. Shorten the intervals on a demanding day.', 'POMODORO')
        card('When I feel stuck', 'Name the obstacle: unclear, too big, uncomfortable, or interrupted. Change one thing: write the next action, shrink it, allow an imperfect draft, or move to a quieter place.', 'A PRACTICAL RESET')
        card('Make a specific plan', 'If [a reliable cue] happens, then I will [one visible action] for [a small amount of time].', 'IF → THEN')
        st.link_button('Read CCI’s procrastination workbook',SOURCES[0]['url'])


def growth_page():
    hero('Skill → evidence → opportunity', 'Build a career you can show.', 'Choose one direction, practice deliberately, and keep proof of your work. Recruiter interest cannot be guaranteed; clear evidence makes your strengths easier to assess.')
    st.caption('Target role: '+profile['target_role']+' · change this in Your space.')
    tab0,tab1,tab2,tab3=st.tabs(['My direction','Learning path','Recall practice','Career evidence'])
    with tab0:
        st.markdown('#### Your career priorities')
        for index,role in enumerate(CAREER_PRIORITIES,1):
            st.write(f'**{index}. {role}**')
        gentle('Keep AI engineering as the main destination. Use data engineering, analytics, and software engineering as supporting capabilities and alternative entry routes that you choose deliberately.')
        st.caption('The foundations below come from the resume you supplied. They describe starting evidence, not an independent assessment of mastery or employment eligibility.')
        for role,foundation,next_step in RESUME_FOUNDATIONS:
            with st.expander(role,expanded=role=='AI Engineer'):
                st.write(foundation)
                st.write('**Next evidence to build:** '+next_step)
        card('One project can connect the four paths', 'Extend your local-manual RAG project: ingest documents reproducibly, evaluate retrieval and grounded answers, expose a tested API, and summarize quality and latency. Label it as a personal or academic project unless it was actually professional work.', 'AI FIRST · DATA PIPELINE · ANALYTICS · SOFTWARE QUALITY')
        st.caption('Your resume lists Oracle Cloud Infrastructure AI Certified Associate, issued 2025. Add its credential link and check its current status before using it in applications. Other credentials remain goals until you record them.')
    with tab1:
        path=st.selectbox('My current direction',list(TRACKS))
        for i,(title,exercise,url) in enumerate(TRACKS[path]):
            card(title,exercise,f'STEP {i+1:02d}')
            st.link_button('Official learning resource',url,key='resource'+path+str(i))
        gentle('A manageable week: two short study sessions, one practical improvement, and one clear explanation. Adapt the amount to your graduation and move.')
        with st.expander('Add a certification or learning goal',expanded=True):
            with st.form('learning_goal'):
                title=st.text_input('Goal / credential',placeholder='AI-103: Developing AI Apps and Agents on Azure')
                kind=st.selectbox('Type',['Certification','Skill','Project'])
                deadline=st.date_input('Target date (optional)',value=None)
                status=st.selectbox('Status',['Considering','Studying','Scheduled','Earned / completed'])
                note=st.text_area('Next lab, exam status, or official resource URL')
                if st.form_submit_button('Save learning goal',type='primary'):
                    if title.strip(): save('learning',{'id':uid(),'kind':'goal','title':title.strip(),'type':kind,'due':deadline.isoformat() if deadline else None,'status':status,'note':note}); st.rerun()
        for g in [x for x in records('learning') if x.get('kind')=='goal']:
            with st.expander(g['title']+' · '+g['status']):
                st.write(g.get('note','')); st.caption(label_date(g.get('due')))
                status=st.selectbox('Update status',['Considering','Studying','Scheduled','Earned / completed'],index=['Considering','Studying','Scheduled','Earned / completed'].index(g['status']),key='gstatus'+g['id'])
                if st.button('Save status',key='gup'+g['id']): save('learning',{**g,'status':status}); st.rerun()
                if st.button('Remove goal',key='gdel'+g['id']): store.delete('learning',g['id']); st.rerun()
        st.caption('Official credential pages were checked on 23 October 2026. They are not a live exam-price or availability feed. Open the current source before booking.')
    with tab2:
        st.write('Answer without notes first. Then reveal your answer, compare, and schedule another recall attempt.')
        with st.expander('Create a recall card'):
            with st.form('recall_new'):
                q=st.text_input('Question',placeholder='When would I use an index in SQL?')
                answer=st.text_area('Answer / explanation')
                if st.form_submit_button('Add recall card'):
                    if q.strip() and answer.strip(): save('learning',{'id':uid(),'kind':'card','title':q.strip(),'answer':answer.strip(),'interval':0,'due':TODAY.isoformat()}); st.rerun()
        due=[x for x in records('learning') if x.get('kind')=='card' and x['due']<=TODAY.isoformat()]
        st.caption(f'{len(due)} cards ready to revisit. Suggested intervals are a simple heuristic.')
        for c in due:
            with st.container(border=True):
                st.markdown('### '+c['title'])
                st.text_area('Try recalling it',key='attempt'+c['id'])
                with st.expander('Reveal answer'):
                    st.write(c['answer'])
                    for col, recalled, text in zip(st.columns(2),[False,True],['Revisit tomorrow','Recalled it · space it out']):
                        if col.button(text,key='recall'+str(recalled)+c['id']):
                            interval,next_day=next_review(c['interval'],recalled,TODAY)
                            save('learning',{**c,'interval':interval,'due':next_day}); st.rerun()
        with st.expander('All recall cards'):
            for c in [x for x in records('learning') if x.get('kind')=='card']:
                st.write(c['title']+' · next: '+c['due'])
                if st.button('Delete card',key='cdel'+c['id']): store.delete('learning',c['id']); st.rerun()
    with tab3:
        card('This week’s proof', 'Ship a useful improvement. Show the problem, your decision, the tradeoff, how you tested it, and the result. Add a readable README and a working demo when appropriate.', 'A PROJECT REVIEWER CAN VERIFY')
        with st.form('evidence'):
            title=st.text_input('Achievement or project')
            source_type=st.selectbox('Where this experience came from',EVIDENCE_TYPES)
            situation=st.text_area('Situation / problem')
            action=st.text_area('What I personally did')
            result=st.text_area('Result and how I verified it',placeholder='Use measured results where available. Do not invent metrics.')
            link=st.text_input('Evidence URL (optional)')
            if st.form_submit_button('Keep this evidence',type='primary'):
                if title.strip() and action.strip(): save('evidence',{'id':uid(),'title':title.strip(),'date':TODAY.isoformat(),'source_type':source_type,'situation':situation,'action':action,'result':result,'url':link}); st.rerun()
        for e in sorted(records('evidence'),key=lambda x:x['date'],reverse=True):
            with st.expander(e['title']+' · '+e['date']):
                st.caption(e.get('source_type','Experience type not yet labelled'))
                st.write('**Problem:** '+e['situation']); st.write('**Action:** '+e['action']); st.write('**Result:** '+e['result'])
                if e.get('url','').startswith(('https://','http://')): st.link_button('View evidence',e['url'])
                if st.button('Remove evidence',key='edel'+e['id']): store.delete('evidence',e['id']); st.rerun()
        evidence=records('evidence')
        if evidence:
            text='\n\n'.join(f"{e['title']} ({e['date']})\nProblem: {e['situation']}\nAction: {e['action']}\nResult: {e['result']}\nEvidence: {e['url']}" for e in evidence)
            st.download_button('Export my career evidence',text,'career-evidence.txt','text/plain')


def voice_page():
    hero('Be heard, at your own pace', 'Your voice deserves space.', 'Practice making your meaning clear and standing up for your needs while staying kind. You do not need flawless speech to have something valuable to say.')
    a,b=st.columns([1.4,1],gap='large')
    with a:
        exercise=st.selectbox('Today’s practice',list(PROMPTS))
        structure,prompt=PROMPTS[exercise]
        card(exercise,prompt,structure)
        st.caption('These speaking structures are practice scaffolds. They are not a treatment protocol or an automated speech assessment.')
        with st.form('voice'):
            draft=st.text_area('Arrange my thoughts',placeholder='One point. One reason. One example. A clear close.',height=150)
            level=st.selectbox('A manageable next step',['Say it privately','Say it to someone I trust','Contribute once in a meeting','Have a boundary conversation'])
            participation=st.checkbox('I tried the speaking step')
            clarity=st.slider('How clear did my message feel? (self-rating)',1,5,3)
            takeaway=st.text_input('One thing I did well / one thing to try next')
            if st.form_submit_button('Save my practice',type='primary'):
                if not draft.strip() and not participation: st.info('Add your thoughts or record an attempt.')
                else: save('practice',{'id':uid(),'date':TODAY.isoformat(),'exercise':exercise,'draft':draft,'level':level,'participated':participation,'clarity':clarity,'takeaway':takeaway}); st.rerun()
        with st.expander('My earlier practice'):
            for p in sorted(records('practice'),key=lambda x:x['date'],reverse=True):
                st.write(f'**{p["date"]} · {p["exercise"]}**'); st.write(p['draft']); st.caption(p['takeaway'])
                if st.button('Remove entry',key='pdel'+p['id']): store.delete('practice',p['id']); st.rerun()
    with b:
        card('A kind, clear “no”', '“I can finish A by Friday. Adding B would move A to Monday. Which should I prioritize?”', 'TRY IT IN YOUR OWN WORDS')
        card('When your mind goes blank', '“Give me a moment to organize my thoughts.” Take the time you need, then return to one main point.', 'YOU CAN ASK FOR TIME')
        gentle('Stuttering is not a measure of intelligence or worth. If it affects your daily life, a speech-language pathologist can help you choose appropriate communication goals. These exercises support practice; they do not diagnose or treat stuttering.')
        st.link_button('Read professional guidance on stuttering',SOURCES[4]['url'])
        st.link_button('Explore the CCI assertiveness workbook',SOURCES[1]['url'])


def coding_page():
    hero('Read → attempt → test → explain', 'Become a stronger problem solver.', 'Practice in small sessions, use help thoughtfully, and return to what you learned. The aim is code you understand and can explain.')
    tracks=['AI engineering','Data engineering','Data analytics','Python','SQL & systems','Dart / Flutter']
    track=st.selectbox('Practice track',tracks,index=tracks.index(profile.get('coding_track','AI engineering')) if profile.get('coding_track','AI engineering') in tracks else 0)
    if st.button('Use this as my default coding track'):
        save('profile',{**profile,'coding_track':track}); st.rerun()
    attempts=[a for a in records('coding') if a['kind']=='attempt']
    filtered=[c for c in CHALLENGES if c['track']==track]
    suggested,reason=recommend(filtered,attempts,TODAY)
    tab1,tab2,tab3=st.tabs(['Practice lab','Debugging notebook','My coding growth'])
    with tab1:
        if suggested: st.caption('Suggested: '+suggested['title']+' · '+reason)
        challenge_id=st.selectbox('Choose a challenge',[c['id'] for c in filtered],index=[c['id'] for c in filtered].index(suggested['id']) if suggested else 0,format_func=lambda i:next(c['title'] for c in filtered if c['id']==i))
        challenge=next(c for c in filtered if c['id']==challenge_id)
        card(challenge['title'],challenge['prompt'],f'{challenge["level"]} · {challenge["skill"]} · about {challenge["minutes"]} minutes')
        st.markdown('#### Expected behavior')
        st.code(challenge['cases'],language='text')
        gentle('Try explaining the inputs, expected output, and edge cases before writing code. Take a first attempt, then use a hint if it helps. Revisit the idea later without copying.')
        a,b=st.columns(2)
        a.download_button('Download starter + checks',practice_file(challenge),challenge['id']+'.'+challenge['extension'],'text/plain',width='stretch')
        b.link_button('Read the official reference',challenge['url'],width='stretch')
        if challenge['extension'] in ['py','dart']:
            command='python '+challenge['id']+'.py' if challenge['extension']=='py' else 'dart run '+challenge['id']+'.dart'
            st.caption('Edit the downloaded file in VS Code and run: '+command+'. The starter may intentionally fail until you implement it. No extra packages are required for these checks.')
        elif challenge['extension']=='sql':
            st.caption('Run the script in a new disposable SQLite or PostgreSQL practice session. Compare its output with the three expected rows above.')
        else: st.caption('Write a short design note and check each failure case. This exercise is reviewed by reasoning, not an automated correctness score.')
        with st.expander('A hint when I need it'): st.write(challenge['hint'])
        with st.expander('Compare with one possible solution'):
            st.code(challenge['solution'],language=challenge['language'])
            st.write(challenge['review'])
            st.download_button('Download this worked solution',practice_file(challenge,True),challenge['id']+'-solution.'+challenge['extension'],'text/plain')
        with st.form('coding_attempt_'+challenge_id):
            st.markdown('#### Save my attempt')
            approach=st.text_area('My approach and edge cases',placeholder='What is the simplest correct approach? What can go wrong?')
            code=st.text_area('My code / design notes',height=200,placeholder='Paste code you wrote or your design proposal here.')
            a,b=st.columns(2)
            minutes=a.number_input('Minutes I practiced',1,240,challenge['minutes'])
            assistance=b.selectbox('Support I used',['Independent attempt','Documentation / hint','AI or worked solution','Pairing / reviewer'])
            test_status=st.selectbox('My local check result',['Not run / design review','Some checks failed','Checks passed (self-reported)'])
            lesson=st.text_input('What I learned / what I will change next')
            log_focus=st.checkbox('Also log these minutes as focus time',value=True,help='Leave off if you already logged this session with the focus timer.')
            if st.form_submit_button('Save coding practice',type='primary'):
                if not approach.strip() and not code.strip(): st.info('Record an approach or an attempt first.')
                else:
                    identifier=uid()
                    save('coding',{'id':identifier,'kind':'attempt','date':TODAY.isoformat(),'logged_at':now().isoformat(),'challenge_id':challenge_id,'title':challenge['title'],'track':track,'minutes':minutes,'approach':approach,'code':code,'assistance':assistance,'test_status':test_status,'lesson':lesson,'review_on':review_date(TODAY,assistance=='Independent attempt',test_status=='Checks passed (self-reported)')})
                    if log_focus: store.put('sessions',{'id':'coding-'+identifier,'date':TODAY.isoformat(),'minutes':minutes,'title':'Coding · '+challenge['title']})
                    st.rerun()
        st.caption('Code is stored as text. It is not executed on the Streamlit server, and local test results are self-reported. Review dates are simple practice prompts, not a validated mastery score.')
        with st.expander('Fit this exercise into my schedule'):
            practice_day=st.date_input('Available for practice from',TODAY,min_value=TODAY,key='practice_day')
            if st.button('Add a 15-minute coding task'):
                identifier='coding-'+challenge_id+'-'+practice_day.isoformat()
                existing=get_record(store,'tasks',identifier,{})
                save('tasks',{**existing,'id':identifier,'title':'Practice · '+challenge['title'],'area':'Learning','next':'Attempt the '+challenge['title']+' exercise in Coding practice; write an approach and one edge-case test.','minutes':15,'priority':2,'due':None,'not_before':practice_day.isoformat(),'window':None,'note':'Self-directed coding practice. Expand the session only if there is room in the day.','done':False})
                st.success('Added to Planner. The daily plan will suggest it when your commitments and focus budget allow.')
    with tab2:
        card('Keep a useful bug record', 'Reproduce → isolate → form a hypothesis → test one change → add a regression check. Focus on what you observed and verified.', 'A REPEATABLE DEBUGGING LOOP')
        with st.form('debug'):
            title=st.text_input('Bug or confusing behavior')
            expected=st.text_area('Expected behavior and smallest reproducible case')
            actual=st.text_area('Actual behavior / exact error')
            cause=st.text_area('Cause, or current hypothesis')
            fix=st.text_area('What I changed and how I verified it')
            regression=st.text_input('Regression test / next experiment')
            if st.form_submit_button('Keep this debugging lesson',type='primary'):
                if title.strip() and actual.strip():
                    save('coding',{'id':uid(),'kind':'debug','date':TODAY.isoformat(),'title':title.strip(),'expected':expected,'actual':actual,'cause':cause,'fix':fix,'regression':regression}); st.rerun()
        for entry in sorted([x for x in records('coding') if x['kind']=='debug'],key=lambda x:x['date'],reverse=True):
            with st.expander(entry['title']+' · '+entry['date']):
                for key,label in [('expected','Expected'),('actual','Observed'),('cause','Cause / hypothesis'),('fix','Change & verification'),('regression','Regression / next test')]: st.write('**'+label+':** '+entry[key])
                if st.button('Remove debugging entry',key='debugdel'+entry['id']): store.delete('coding',entry['id']); st.rerun()
    with tab3:
        selected_attempts=[a for a in attempts if a['track']==track]
        a,b,c=st.columns(3)
        a.metric('Practice attempts',len(selected_attempts))
        b.metric('Minutes practiced',sum(x['minutes'] for x in selected_attempts))
        c.metric('Independent attempts',sum(x['assistance']=='Independent attempt' for x in selected_attempts))
        st.caption('These are activity records and self-reports. They are not verified skill ratings. Using documentation, AI, or a reviewer can be useful; record what you can now explain yourself.')
        card('A flexible four-week rhythm', 'Week 1: evaluate an AI component and inspect failure cases. Week 2: make its input data repeatable and reliable. Week 3: serve the component through a tested interface. Week 4: summarize the results and explain the tradeoffs. Repeat or slow down as needed.', 'AI FIRST · SUPPORTING DATA AND SOFTWARE SKILLS')
        st.markdown('#### Transfer to real work')
        st.write('Choose one task in your app: separate a pure rule from the UI, add validation, handle an error state, improve a query, or write a meaningful test. Keep a before/after note in Career & learning → Career evidence.')
        for entry in sorted(selected_attempts,key=lambda x:x['logged_at'],reverse=True):
            with st.expander(entry['title']+' · '+entry['date']):
                st.caption(entry['assistance']+' · '+entry['test_status']+' · revisit '+entry['review_on'])
                st.write(entry['approach']); st.code(entry['code'],language='text'); st.write(entry['lesson'])
                if st.button('Remove attempt',key='codedel'+entry['id']):
                    store.delete('coding',entry['id'])
                    store.delete('sessions','coding-'+entry['id'])
                    st.rerun()
        if selected_attempts:
            st.download_button('Export this track’s practice',json.dumps(selected_attempts,ensure_ascii=False,indent=2),'coding-practice.json','application/json')


def market_page():
    hero('Your goals, grounded in actual roles', 'Turn job requirements into evidence.', 'Compare the role, level, and exact requirements. Track what you can demonstrate, what is transferable, and what still needs experience.')
    st.caption('Your order: AI Engineer → Data Engineer → Data Analytics → Software Engineering.')
    tab1,tab2,tab3=st.tabs(['Employer examples','My opportunities','Build relevant experience'])
    with tab1:
        gentle('Experience requirements are real, and they vary. Projects and certifications can strengthen an application, but they do not automatically satisfy a stated requirement for professional tenure.')
        st.caption('Small, nonrepresentative sample of employer postings reviewed '+CHECKED_ON+'. These are dated research examples, not confirmed live vacancies or a market-wide survey. Reopen the employer page before applying.')
        for job in JOB_EXAMPLES:
            with st.expander(job['employer']+' · '+job['title']):
                st.caption(job['role']+' · '+job['location'])
                st.write('**Experience wording:** '+job['experience'])
                st.write('**Capabilities requested:** '+', '.join(job['requirements']))
                st.write('**How to use it:** '+job['lesson'])
                st.link_button('Check the employer’s current page',job['url'])
                if st.button('Keep this example in my tracker',key='example'+job['id']):
                    save('jobs',{**job,'checked_on':CHECKED_ON,'status':'Research example','evidence_map':{}})
                    st.success('Saved as a research example. Confirm that the vacancy is open before changing its status.')
    with tab2:
        with st.expander('Add an opportunity',expanded=True):
            with st.form('new_job'):
                title=st.text_input('Job title')
                employer=st.text_input('Employer')
                role=st.selectbox('Career direction',CAREER_PRIORITIES)
                location=st.text_input('Location / work arrangement')
                url=st.text_input('Employer posting URL')
                experience=st.text_area('Exact experience / degree / eligibility wording',placeholder='Separate mandatory requirements from preferences. Keep conflicting wording visible.')
                requirements=st.text_area('Skills or deliverables to compare, one per line',placeholder='Python\nModel evaluation\nAPI deployment\nSQL')
                checked=st.date_input('Date I checked this posting',TODAY,max_value=TODAY)
                if st.form_submit_button('Save opportunity',type='primary'):
                    if not title.strip() or not employer.strip(): st.info('Add the employer and job title.')
                    elif url and not url.startswith(('https://','http://')): st.info('Use a full http or https URL.')
                    else:
                        save('jobs',{'id':uid(),'title':title.strip(),'employer':employer.strip(),'role':role,'location':location,'url':url,'experience':experience,'requirements':[s.strip() for s in requirements.splitlines() if s.strip()][:15],'checked_on':checked.isoformat(),'status':'Saved','evidence_map':{}}); st.rerun()
        for job in sorted(records('jobs'),key=lambda j:(CAREER_PRIORITIES.index(j['role']),j['title'])):
            with st.expander(job['employer']+' · '+job['title']+' · '+job['status']):
                st.caption(job['role']+' · '+job['location']+' · last checked '+job['checked_on'])
                st.write(job['experience'])
                if job['url'].startswith(('https://','http://')): st.link_button('Open employer posting',job['url'],key='jurl'+job['id'])
                evidence_map=job.get('evidence_map',{})
                statuses=['Research example','Saved','Evaluating','Applied','Interview','Offer','Closed / not pursuing']
                with st.form('jobmap'+job['id']):
                    status=st.selectbox('Application status',statuses,index=statuses.index(job['status']) if job['status'] in statuses else 1)
                    mapping={}
                    for i,requirement in enumerate(job['requirements']):
                        st.markdown('**'+requirement+'**')
                        previous=evidence_map.get(requirement,{})
                        options=['Not yet mapped','Professional / freelance evidence','Internship evidence','Research / project evidence','Learning only / gap']
                        kind=st.selectbox('Evidence type',options,index=options.index(previous.get('kind','Not yet mapped')) if previous.get('kind','Not yet mapped') in options else 0,key='jk'+job['id']+str(i))
                        detail=st.text_input('Specific example / proof link',value=previous.get('detail',''),key='jd'+job['id']+str(i))
                        mapping[requirement]={'kind':kind,'detail':detail}
                    notes=st.text_area('Next action / interview feedback',value=job.get('notes',''))
                    if st.form_submit_button('Save requirement mapping'):
                        save('jobs',{**job,'status':status,'evidence_map':mapping,'notes':notes}); st.rerun()
                mapped=sum(bool(x.get('detail','').strip()) and x.get('kind') not in ['Not yet mapped','Learning only / gap'] for x in evidence_map.values())
                st.caption(f'{mapped} of {len(job["requirements"])} requirements have a self-entered evidence example. This is not a match score, hiring probability, or verification of eligibility. Review years of experience and other mandatory conditions separately.')
                if st.button('Remove opportunity',key='jdel'+job['id']): store.delete('jobs',job['id']); st.rerun()
    with tab3:
        st.write('Your resume already records paid freelance development and internships. Describe dates, scope, and personal contributions accurately. Relevant transfer is useful; it does not turn mobile-development tenure into AI-production tenure.')
        for index,(title,body) in enumerate(EXPERIENCE_BRIDGES,1): card(title,body,f'{index:02d} · OPTIONAL NEXT STEP')
        gentle('A realistic week can contain one small technical improvement, one evidence note, and one or two careful job-description reviews. Reduce that during your move and graduation deadlines. You do not need to study four separate careers every day.')
        if st.button('Add a job-market review task to Planner'):
            save('tasks',{'id':'market-review-'+TODAY.isoformat(),'title':'Review two AI / data opportunities','area':'Career','next':'Compare two relevant employer postings: mandatory experience, capabilities, and one concrete evidence gap.','minutes':15,'priority':2,'due':None,'not_before':TODAY.isoformat(),'window':None,'note':'Use Job market. Select suitable levels; do not treat a project as professional tenure.','done':False})
            st.success('Added to Planner within the same daily capacity limits.')


def money_dashboard_view(month,budget):
    data=money_dashboard(records('transactions'),month,budget,TODAY)
    st.subheader('Your money at a glance')
    st.caption(date.fromisoformat(month+'-01').strftime('%B %Y')+' · updates whenever you save an entry')
    a,b=st.columns(2)
    c,d=st.columns(2)
    a.metric('Income received',f'₱{data["income"]:,.2f}')
    b.metric('Expenses',f'₱{data["expense"]:,.2f}')
    c.metric('Savings & investment transfers',f'₱{data["transfers"]:,.2f}')
    d.metric('Net logged cash flow',f'₱{data["net"]:,.2f}')
    st.caption('Net logged cash flow = income − expenses − transfers. It is not your bank balance. Transfers stay separate from spending; future-dated entries are excluded.')
    if not data['rows']:
        gentle('Your dashboard starts with your entries. Add income or an expense in Money log, then come back to see your patterns.')
    elif not data['expense_count']:
        gentle('Income or transfers are logged. Add expenses to see your spending patterns.')
    else:
        top=max(data['categories'],key=data['categories'].get)
        share=100*data['categories'][top]/data['expense']
        st.write(f'**{top}** is your largest spending category: **₱{data["categories"][top]:,.2f}** ({share:.0f}% of logged expenses).')
        st.caption(f'{data["expense_count"]} expense entries · average ₱{data["daily_average"]:,.2f} per calendar day in this period. Missing entries affect these figures.')
        prior=data['previous']['expense']
        if prior:
            delta=data['expense']-prior
            st.write(f'Logged expenses are ₱{abs(delta):,.2f} {"higher" if delta>=0 else "lower"} than the comparable previous period.')
            st.caption('Previous comparison ends '+data['previous_cutoff']+'. This compares your manual logs, not a complete bank statement.')
    st.markdown('#### Where your spending goes')
    if data['categories']:
        frame=pd.DataFrame([{'Category':k,'Expenses (₱)':v} for k,v in data['categories'].items()]).sort_values('Expenses (₱)',ascending=False)
        st.bar_chart(frame,x='Category',y='Expenses (₱)',color='#8E7B67',horizontal=True)
        st.dataframe(frame,hide_index=True,width='stretch')
    else: st.caption('No expense entries for this month yet.')
    st.markdown('#### Daily spending')
    if data['daily']:
        start=date.fromisoformat(month+'-01')
        stop=min(TODAY,(start.replace(day=28)+timedelta(days=4)).replace(day=1)-timedelta(days=1))
        days=pd.date_range(start,stop,freq='D')
        daily=pd.DataFrame({'Date':days,'Expenses (₱)':[data['daily'].get(d.date().isoformat(),0.) for d in days]})
        st.line_chart(daily,x='Date',y='Expenses (₱)',color='#8E7B67')
        st.caption('A zero means no expense was logged that day.')
    else: st.caption('Your daily trend will appear after you log expenses.')
    st.markdown('#### Plan versus actual')
    st.dataframe(pd.DataFrame(data['comparison']),hide_index=True,width='stretch',
                 column_config={k:st.column_config.NumberColumn(format='₱ %.2f') for k in ['Planned (₱)','Actual (₱)','Remaining (₱)']})
    st.caption('Negative remaining means the logged amount exceeds your plan. Savings and investment rows show transfers toward those goals, not spending.')
    joy=float(budget.get('joy',0))-data['categories'].get('Enjoyment',0)
    if budget.get('joy',0): gentle(f'Your chosen enjoyment budget has ₱{joy:,.2f} remaining.' if joy>=0 else f'Enjoyment is ₱{abs(joy):,.2f} above this month’s plan. You can review the plan as your needs change.')
    st.markdown('#### The last six months')
    if any(row['Income'] or row['Expenses'] or row['Transfers'] for row in data['trend']):
        trend=pd.DataFrame(data['trend'])
        st.bar_chart(trend,x='Month',y=['Income','Expenses','Transfers'],stack=False,color=['#73836A','#8E7B67','#8A8096'])
        st.dataframe(trend,hide_index=True,width='stretch')
    else: st.caption('Monthly comparisons will grow as you add your entries.')


def money_page():
    hero('Enough for now. Room for later.', 'Make your money feel intentional.', 'Start with your real income and expenses. Give each priority a place, including enjoyment, without assuming a perfect month.')
    month=st.date_input('Budget month',TODAY.replace(day=1)).strftime('%Y-%m')
    budget=get_record(store,'budgets',month,{'income':0.,'needs':0.,'joy':0.,'buffer':0.,'learning':0.,'emergency':0.,'investing':0.,'current_emergency':0.,'emergency_target':5000.})
    dashboard,tab1,tab2,tab3=st.tabs(['Dashboard','Monthly plan','Money log','Savings goal'])
    with dashboard: money_dashboard_view(month,budget)
    with tab1:
        with st.form('budget'):
            income=st.number_input('Expected take-home income (₱)',min_value=0.,value=float(budget['income']),step=500.)
            a,b=st.columns(2)
            needs=a.number_input('Essentials & debt payments (₱)',min_value=0.,value=float(budget['needs']),step=100.)
            joy=b.number_input('Enjoyment I choose (₱)',min_value=0.,value=float(budget['joy']),step=100.)
            buffer=a.number_input('Move / glasses / irregular costs (₱)',min_value=0.,value=float(budget['buffer']),step=100.)
            learning=b.number_input('Learning & certification fund (₱)',min_value=0.,value=float(budget['learning']),step=100.)
            emergency=a.number_input('Emergency savings contribution (₱)',min_value=0.,value=float(budget['emergency']),step=100.)
            investing=b.number_input('Investing contribution (₱)',min_value=0.,value=float(budget['investing']),step=100.)
            summary=budget_summary(dict(income=income,needs=needs,joy=joy,buffer=buffer,learning=learning,emergency=emergency,investing=investing))
            st.caption('The saved summary updates when you submit. Amounts are your choices, not recommended percentages.')
            if st.form_submit_button('Save my monthly plan',type='primary'):
                save('budgets',{**budget,'id':month,'income':income,'needs':needs,'joy':joy,'buffer':buffer,'learning':learning,'emergency':emergency,'investing':investing}); st.rerun()
        summary=budget_summary(budget)
        a,b,c=st.columns(3)
        a.metric('Planned income',f'₱{summary["income"]:,.0f}')
        b.metric('Assigned to priorities',f'₱{summary["allocated"]:,.0f}')
        c.metric('Unassigned / shortfall',f'₱{summary["remaining"]:,.0f}')
        if summary['remaining']<0: st.info('This plan allocates more than expected income. Adjust amounts before committing; an entry does not move money.')
        elif not summary['income']: gentle('No income assumed. Enter your actual expected take-home pay to build a useful plan.')
        else: gentle('An enjoyment category gives you permission to spend intentionally. Revisit it when your needs or income change.')
    with tab2:
        with st.form('transaction'):
            day=st.date_input('Transaction date',TODAY,max_value=TODAY,key='txday')
            title=st.text_input('Description')
            kind=st.selectbox('Type',['Expense','Income','Savings transfer','Investment transfer'])
            category=st.selectbox('Category',['Essentials','Enjoyment','Move / glasses / irregular','Learning','Emergency savings','Investing','Other'])
            amount=st.number_input('Amount (₱)',min_value=0.01,value=100.,step=10.)
            if st.form_submit_button('Add to money log',type='primary'):
                if title.strip(): save('transactions',{'id':uid(),'date':day.isoformat(),'title':title.strip(),'type':kind,'category':category,'amount':amount}); st.rerun()
        tx=sorted([t for t in records('transactions') if t['date'].startswith(month)],key=lambda x:x['date'],reverse=True)
        expenses=sum(t['amount'] for t in tx if t['type']=='Expense')
        income=sum(t['amount'] for t in tx if t['type']=='Income')
        transfers=sum(t['amount'] for t in tx if t['type'] in ['Savings transfer','Investment transfer'])
        a,b,c=st.columns(3)
        a.metric('Logged income',f'₱{income:,.2f}'); b.metric('Logged expenses',f'₱{expenses:,.2f}'); c.metric('Logged transfers',f'₱{transfers:,.2f}')
        st.caption('Transfers are separate from spending. This is a manual log, not a bank balance or bank connection.')
        joy_spend=sum(t['amount'] for t in tx if t['type']=='Expense' and t['category']=='Enjoyment')
        st.write(f'Enjoyment plan remaining: ₱{budget["joy"]-joy_spend:,.2f}')
        for t in tx:
            with st.expander(f'{t["date"]} · {t["title"]} · ₱{t["amount"]:,.2f}'):
                st.write(t['type']+' / '+t['category'])
                with st.form('transaction_edit_'+t['id']):
                    tx_title=st.text_input('Entry description',t['title'])
                    tx_date=st.date_input('Entry date',date.fromisoformat(t['date']),max_value=max(TODAY,date.fromisoformat(t['date'])))
                    types=['Expense','Income','Savings transfer','Investment transfer']
                    tx_type=st.selectbox('Entry type',types,index=types.index(t['type']))
                    cats=['Essentials','Enjoyment','Move / glasses / irregular','Learning','Emergency savings','Investing','Other']
                    if t['category'] not in cats: cats.append(t['category'])
                    tx_cat=st.selectbox('Entry category',cats,index=cats.index(t['category']))
                    tx_amount=st.number_input('Entry amount (₱)',min_value=0.01,value=float(t['amount']),step=10.)
                    if st.form_submit_button('Save money entry'):
                        if not tx_title.strip(): st.info('Add a description for this entry.')
                        elif tx_date>TODAY: st.info('Use the date money actually moved. Use Monthly plan for future amounts.')
                        else:
                            save('transactions',{**t,'title':tx_title.strip(),'date':tx_date.isoformat(),'type':tx_type,'category':tx_cat,'amount':tx_amount}); st.rerun()
                if st.button('Remove transaction',key='txdel'+t['id']): store.delete('transactions',t['id']); st.rerun()
        if tx: st.download_button('Export this month’s transactions',pd.DataFrame(tx).drop(columns='id').to_csv(index=False),'money-'+month+'.csv','text/csv')
    with tab3:
        with st.form('savings'):
            current=st.number_input('Current emergency cash reserve (₱)',min_value=0.,value=float(budget.get('current_emergency',0.)),step=100.)
            target=st.number_input('My next emergency fund milestone (₱)',min_value=1.,value=float(budget.get('emergency_target',5000.)),step=500.)
            if st.form_submit_button('Save reserve & milestone'):
                save('budgets',{**budget,'id':month,'current_emergency':current,'emergency_target':target}); st.rerun()
        current,target=float(budget.get('current_emergency',0)),float(budget.get('emergency_target',5000))
        st.progress(min(1.,current/target),text=f'₱{current:,.0f} of ₱{target:,.0f}')
        months=months_to_goal(current,target,float(budget['emergency']))
        st.write('Milestone reached.' if months==0 else f'About {months} monthly contributions at your planned rate, with no withdrawals or returns.' if months is not None else 'Add a monthly emergency contribution to estimate the time needed.')
        st.caption('Reserve is a balance you enter manually. Transfers do not automatically change it. Reconcile against your actual account each month.')
        st.link_button('Read the CFPB emergency savings guide',SOURCES[6]['url'])
        st.caption('Educational planning only. No returns, investment safety, local tax treatment, or financial product suitability are assumed.')


def reflect_page():
    hero('Notice. Adjust. Begin again.', 'Progress is more than output.', 'Keep a record of what is working and what needs to change. Compare with your own earlier choices, rather than an imaginary perfect person.')
    tab1,tab2,tab3=st.tabs(['Evening reflection','Weekly reset','My history'])
    with tab1:
        day=st.date_input('Reflect on',TODAY,max_value=TODAY)
        r=get_record(store,'reflections',day.isoformat(),{})
        with st.form('reflection'):
            win=st.text_area('One thing I handled or moved forward',value=r.get('win',''))
            obstacle=st.text_area('What made today harder?',value=r.get('obstacle',''))
            kindness=st.text_input('A kind or assertive action I took',value=r.get('kindness',''))
            tomorrow=st.text_input('One smaller next step for tomorrow',value=r.get('tomorrow',''))
            if st.form_submit_button('Close the day gently',type='primary'):
                save('reflections',{'id':day.isoformat(),'date':day.isoformat(),'win':win,'obstacle':obstacle,'kindness':kindness,'tomorrow':tomorrow}); st.rerun()
        gentle('If the plan did not happen, ask what made it difficult. Make the next action clearer or smaller. Rest can be the right choice.')
    with tab2:
        week=TODAY-timedelta(days=TODAY.weekday())
        review=get_record(store,'reviews',week.isoformat(),{})
        with st.form('review'):
            answers=[st.text_area(prompt,value=review.get('answers',['']*len(WEEKLY_PROMPTS))[i],key='week'+str(i)) for i,prompt in enumerate(WEEKLY_PROMPTS)]
            if st.form_submit_button('Save this week’s reset',type='primary'):
                save('reviews',{'id':week.isoformat(),'date':week.isoformat(),'answers':answers}); st.rerun()
        sessions=[s for s in records('sessions') if s['date']>=week.isoformat() and s['date']<=TODAY.isoformat()]
        practices=[p for p in records('practice') if p['date']>=week.isoformat() and p['date']<=TODAY.isoformat() and p.get('participated')]
        a,b=st.columns(2)
        a.metric('Logged focus this week',f'{sum(s["minutes"] for s in sessions)} min')
        b.metric('Speaking steps attempted',len(practices))
        st.caption('These measures describe activity, not personal worth or a clinical outcome. Blank days mean no record, not failure.')
    with tab3:
        checkins=sorted(records('checkins'),key=lambda x:x['id'])[-30:]
        if checkins:
            chart=pd.DataFrame([{'Date':x['id'],'Energy (self-rating)':x['energy']} for x in checkins]).set_index('Date')
            st.line_chart(chart,color='#8A9A83',height=200)
        else: st.caption('Your energy trend appears after your first daily check-in.')
        for r in sorted(records('reflections'),key=lambda x:x['date'],reverse=True):
            with st.expander(r['date']+' · '+(r['win'][:60] or 'Reflection')):
                for key,label in [('win','Moved forward'),('obstacle','Obstacle'),('kindness','Kindness / boundary'),('tomorrow','Next step')]: st.write(f'**{label}:** {r.get(key,"")}')
                if st.button('Remove reflection',key='rdel'+r['id']): store.delete('reflections',r['id']); st.rerun()
        with st.expander('Earlier weekly resets'):
            for r in sorted(records('reviews'),key=lambda x:x['date'],reverse=True):
                st.write('**Week of '+r['date']+'**')
                for q,a in zip(WEEKLY_PROMPTS,r['answers']): st.write(f'**{q}** {a}')


def sources_page():
    hero('Grounded in useful evidence', 'A small, credible resource shelf.', 'Practical frameworks, with their sources and limits visible. The app adapts them into exercises you can try and revise.')
    st.caption('Sources checked 23 October 2026. These summaries are curated; they are not a real-time research feed. Dates, deadlines, and your records update from your inputs.')
    for source in SOURCES:
        with st.container(border=True):
            st.caption(source['publisher']+' · '+source['basis'])
            st.subheader(source['title']); st.write(source['use'])
            st.link_button('Open source',source['url'],key=source['title'])
    gentle('The scheduling limits, five-minute starts, reflection prompts, and speaking outlines are product design choices informed by these resources. They are not a validated treatment program or a promise of career outcomes.')


def settings_page():
    hero('Your life, your settings', 'Make this space yours.', 'Update your work pattern and daily rhythm as life changes. Your plan uses Philippine time on every device.')
    with st.form('profile'):
        name=st.text_input('Name',profile['name'])
        role=st.text_input('Current role',profile['role'])
        target=st.text_input('Target role / direction',profile['target_role'])
        days=st.multiselect('Workdays (initial assumption: Monday–Friday)',DAYS,default=profile['workdays'])
        a,b=st.columns(2)
        start=a.time_input('Work begins (PHT)',dtime.fromisoformat(profile['work_start']))
        end=b.time_input('Work ends (PHT)',dtime.fromisoformat(profile['work_end']))
        wake=a.time_input('Day can begin',dtime.fromisoformat(profile['wake']))
        sleep=b.time_input('Day winds down',dtime.fromisoformat(profile['sleep']))
        buffer=st.slider('Transition minutes between focus blocks',0,30,int(profile['buffer']),5)
        if st.form_submit_button('Save my rhythm',type='primary'):
            if not name.strip() or start>=end or wake>=sleep: st.info('Add your name and use end times after start times. Overnight schedules need two separate commitments.')
            else:
                save('profile',{**profile,'name':name.strip(),'role':role,'target_role':target,'workdays':days,'work_start':start.strftime('%H:%M'),'work_end':end.strftime('%H:%M'),'wake':wake.strftime('%H:%M'),'sleep':sleep.strftime('%H:%M'),'buffer':buffer}); st.rerun()
    st.subheader('Recurring meal & personal blocks')
    st.caption('These blocks start each day’s schedule. Work hours come from the settings above. Daily overrides in Planner stay as you saved them.')
    with st.form('routine'):
        edited=schedule_editor(routine_blocks(profile),f'routine_editor_{profile.get("routine_version",0)}')
        if st.form_submit_button('Save recurring blocks',type='primary'):
            try:
                blocks=schedule_rows(edited)
                save('profile',{**profile,'routine':blocks,'routine_version':profile.get('routine_version',0)+1})
                st.rerun()
            except ValueError as exc: st.info(str(exc))
    st.markdown('### My data')
    st.caption('Cloud records are loaded on each interaction. Use Refresh to fetch updates from another device. Avoid editing the same record on two devices at once: the last saved edit wins.')
    if st.button('Refresh from my saved records'): st.rerun()
    backup=json.dumps(export_records(store),ensure_ascii=False,indent=2)
    st.download_button('Download a full backup',backup,f'becoming-backup-{TODAY}.json','application/json')
    with st.expander('Restore a backup (merges by record ID)'):
        upload=st.file_uploader('Becoming JSON backup',type='json')
        confirm=st.checkbox('I understand matching records will be overwritten. Download a backup first.')
        if st.button('Restore records',disabled=not (upload and confirm)):
            try:
                data=json.load(upload)
                total=validate_backup(data)
                # All structural checks above run before writes; see README for non-atomic cloud restore.
                for collection,rows in data['collections'].items():
                    for row in rows: store.put(collection,row)
                st.success(f'Restored {total} records. Refresh to load them.')
            except (ValueError,TypeError,StorageError) as exc: st.error('Restore could not finish: '+str(exc))
    with st.expander('Remove a saved record'):
        collection=st.selectbox('Record category',sorted(COLLECTIONS-{'profile'}))
        rows=records(collection)
        if rows:
            row_id=st.selectbox('Record', [r['id'] for r in rows],format_func=lambda i: next((r.get('title') or r.get('date') or r['id'] for r in rows if r['id']==i),i))
            confirm=st.checkbox('Permanently remove this record')
            if st.button('Delete selected record',disabled=not confirm): store.delete(collection,row_id); st.rerun()
    st.caption('No advertising, external analytics, AI scoring, microphone capture, bank connection, or paid API key is used. Your entries are not sent to a language model. Authentication and synced records use your configured Supabase project.')


style()
try:
    store=RunStore(authenticate())
    initialize()
    profile=get_record(store,'profile','main',default_profile())
    if st.session_state.get('timer') and 'phase' not in st.session_state.timer:
        old=st.session_state.timer
        st.session_state.timer={**start_timer(old['title'],old['minutes'],pomodoro=False),**old}
    with st.sidebar:
        st.markdown('<div class="brand">becoming<span style="font-size:1.4rem"> ✧</span></div><div class="brand-sub">Room to grow, at your pace</div>',unsafe_allow_html=True)
        pages=['Today','Planner','Focus','Coding practice','Career & learning','Job market','Voice & confidence','Money','Reflect','Resources','Your space']
        page=st.session_state.get('page','Today')
        if page not in pages: page='Today'
        for name in pages:
            st.button(f'**{name}**' if name==page else name,key='nav_'+name,type='tertiary',width='stretch',on_click=navigate,args=(name,))
        st.divider()
        live_clock()
        st.caption('Asia/Manila · UTC+8')
        st.caption('Private local records' if store.mode=='local' else 'Signed in · synced records')
        if st.session_state.get('timer'):
            st.caption('Timer paused · return to Focus' if st.session_state.timer.get('paused') else 'Timer active · return to Focus')
        if store.mode=='cloud':
            if st.button('Sign out'):
                try:
                    requests.post(secret('SUPABASE_URL').rstrip('/')+'/auth/v1/logout',headers={'apikey':secret('SUPABASE_ANON_KEY'),'Authorization':'Bearer '+st.session_state.auth['access_token']},timeout=10)
                except requests.RequestException: pass
                st.session_state.clear(); st.rerun()
        st.markdown('---')
        st.caption('A small step is still a step.')
    {'Today':today_page,'Planner':planner_page,'Focus':focus_page,'Coding practice':coding_page,'Career & learning':growth_page,'Job market':market_page,'Voice & confidence':voice_page,'Money':money_page,'Reflect':reflect_page,'Resources':sources_page,'Your space':settings_page}[page]()
except StorageError as exc:
    st.error(str(exc))
    st.caption('Your existing records were not replaced with a blank local copy. Retry, or sign in again if your session expired.')
    if st.button('Retry'): st.rerun()
