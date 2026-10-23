import os
import unittest
import time
from datetime import date
from unittest.mock import patch
from pathlib import Path
from streamlit.testing.v1 import AppTest
from storage import MemoryStore

APP=Path(__file__).resolve().parents[1]/'app.py'

class AppTests(unittest.TestCase):
    def setUp(self):
        self.env=patch.dict(os.environ,{'BECOMING_LOCAL':'0','SUPABASE_URL':'https://test.supabase.co','SUPABASE_ANON_KEY':'test-key'})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.data={}
        backend=MemoryStore(self.data)
        backend.mode='cloud'
        cloud=patch('storage.CloudStore',return_value=backend)
        cloud.start()
        self.addCleanup(cloud.stop)
        self.at=AppTest.from_file(str(APP),default_timeout=20)
        self.at.session_state['auth']={'expires_at':time.time()+3600,'user':{'id':'test-user'},'access_token':'test'}
        self.at.run()
    def assert_clean(self):
        self.assertFalse(self.at.exception, str(self.at.exception))
    def nav(self,page):
        next(b for b in self.at.sidebar.button if b.key=='nav_'+page).click().run()
        self.assert_clean()
    def test_every_page_renders(self):
        self.assert_clean()
        for page in ['Planner','Focus','Coding practice','Career & learning','Job market','Voice & confidence','Money','Reflect','Resources','Your space','Today']:
            self.nav(page)
    def test_checkin_persists(self):
        self.at.text_input[0].set_value('One useful next step')
        next(b for b in self.at.button if b.label=='Shape my day').click().run()
        self.assert_clean()
        data=self.data['checkins']
        self.assertEqual(next(iter(data.values()))['intention'],'One useful next step')
    def test_money_plan(self):
        self.nav('Money')
        for label,amount in [('Expected take-home income (₱)',20000.),('Essentials & debt payments (₱)',12000.),('Enjoyment I choose (₱)',1500.),('Emergency savings contribution (₱)',1000.)]:
            next(x for x in self.at.number_input if x.label==label).set_value(amount)
        next(b for b in self.at.button if b.label=='Save my monthly plan').click().run()
        self.assert_clean()
        self.assertEqual(next(m for m in self.at.metric if m.label=='Unassigned / shortfall').value,'₱5,500')
    def test_task_creation(self):
        self.nav('Planner')
        inputs=self.at.text_input
        next(x for x in inputs if x.label=='Task').set_value('Portfolio update')
        next(x for x in inputs if x.label=='Smallest useful next action').set_value('Write one README paragraph')
        next(b for b in self.at.button if b.label=='Save task').click().run()
        self.assert_clean()
        self.assertTrue(any(x['title']=='Portfolio update' for x in self.data['tasks'].values()))
    def test_focus_timer(self):
        self.nav('Focus')
        next(x for x in self.at.text_input if x.label=='What will I work on?').set_value('Read the schema')
        next(b for b in self.at.button if b.label=='Begin focus').click().run()
        self.assert_clean()
        self.assertEqual(self.at.session_state['timer']['minutes'],25)
        next(b for b in self.at.button if b.label=='Pause').click().run()
        self.assertTrue(self.at.session_state['timer']['paused'])
        next(b for b in self.at.button if b.label=='Resume').click().run()
        self.at.session_state['timer']={**self.at.session_state['timer'],'end':time.time()-1}
        self.at.run()
        next(b for b in self.at.button if b.label=='Save focus & start break').click().run()
        self.assert_clean()
        self.assertEqual(self.at.session_state['timer']['phase'],'Short break')
        self.assertEqual(len(self.data['sessions']),1)
        next(b for b in self.at.button if b.label=='Skip break').click().run()
        self.assertEqual(self.at.session_state['timer']['round'],2)
        next(b for b in self.at.button if b.label=='End timer without logging').click().run()
        self.assert_clean()

    def test_coding_practice_and_debugging(self):
        self.nav('Coding practice')
        next(x for x in self.at.text_area if x.label=='My approach and edge cases').set_value('Use a set plus a list; test empty input.')
        next(x for x in self.at.text_input if x.label=='What I learned / what I will change next').set_value('Preserve the order of first occurrence.')
        next(b for b in self.at.button if b.label=='Save coding practice').click().run()
        self.assert_clean()
        attempts=self.data['coding']
        self.assertEqual(len(attempts),1)
        self.assertEqual(len(self.data['sessions']),1)
        next(x for x in self.at.text_input if x.label=='Bug or confusing behavior').set_value('Shared state')
        next(x for x in self.at.text_area if x.label=='Actual behavior / exact error').set_value('A new call retains an old task.')
        next(b for b in self.at.button if b.label=='Keep this debugging lesson').click().run()
        self.assert_clean()
        self.assertEqual(len(self.data['coding']),2)
        next(x for x in self.at.selectbox if x.label=='Practice track').set_value('Dart / Flutter').run()
        self.assert_clean()
        next(x for x in self.at.selectbox if x.label=='Practice track').set_value('SQL & systems').run()
        self.assert_clean()
        for track in ['Data engineering','Data analytics','Python','AI engineering']:
            next(x for x in self.at.selectbox if x.label=='Practice track').set_value(track).run()
            self.assert_clean()

    def test_schedule_coding_task(self):
        self.nav('Coding practice')
        next(b for b in self.at.button if b.label=='Add a 15-minute coding task').click().run()
        self.assert_clean()
        tasks=self.data['tasks'].values()
        self.assertTrue(any(t['title']=='Practice · Evaluate binary predictions' for t in tasks))

    def test_job_market_evidence_mapping(self):
        self.nav('Job market')
        next(b for b in self.at.button if b.key=='exampleaccenture-r00288844').click().run()
        self.assert_clean()
        next(x for x in self.at.selectbox if x.label=='Evidence type').set_value('Research / project evidence')
        next(x for x in self.at.text_input if x.label=='Specific example / proof link').set_value('My local RAG evaluation notes')
        next(b for b in self.at.button if b.label=='Save requirement mapping').click().run()
        self.assert_clean()
        row=self.data['jobs']['accenture-r00288844']
        self.assertEqual(row['status'],'Research example')
        self.assertTrue(any(v['detail']=='My local RAG evaluation notes' for v in row['evidence_map'].values()))

    def test_ai_is_primary(self):
        self.assertEqual(self.data['profile']['main']['target_role'],'AI Engineer')
        self.nav('Career & learning')
        self.assertEqual(next(x for x in self.at.selectbox if x.label=='My current direction').value,'AI Engineer')

    def test_no_demo_or_radio_navigation(self):
        self.assertFalse(self.at.sidebar.radio)
        self.at.session_state['auth']=None
        self.at.session_state['demo']=True  # A previous demo session cannot bypass sign-in.
        self.at.run()
        self.assert_clean()
        self.assertTrue(any(x.label=='Email' for x in self.at.text_input))
        self.assertFalse(any('demo' in b.label.lower() for b in self.at.button))
        self.assertFalse(any(b.key=='nav_Planner' for b in self.at.button))

    def test_task_status_transitions_and_filters(self):
        self.nav('Planner')
        next(b for b in self.at.button if b.key=='togglegraduation').click().run()
        self.assertEqual(self.data['tasks']['graduation']['status'],'Ongoing')
        next(x for x in self.at.selectbox if x.label=='Filter status').set_value('Ongoing').run()
        next(b for b in self.at.button if b.key=='togglegraduation').click().run()
        self.assertTrue(self.data['tasks']['graduation']['done'])
        next(x for x in self.at.selectbox if x.label=='Filter status').set_value('Completed').run()
        next(b for b in self.at.button if b.key=='togglegraduation').click().run()
        self.assertEqual(self.data['tasks']['graduation']['status'],'New')
        self.assertFalse(self.data['tasks']['graduation']['done'])
        self.assert_clean()

    def test_money_entry_drives_dashboard_and_can_be_corrected(self):
        self.nav('Money')
        next(x for x in self.at.text_input if x.label=='Description').set_value('Lunch')
        next(x for x in self.at.number_input if x.label=='Amount (₱)').set_value(250.)
        next(b for b in self.at.button if b.label=='Add to money log').click().run()
        self.assert_clean()
        self.assertEqual(next(m for m in self.at.metric if m.label=='Expenses').value,'₱250.00')
        next(x for x in self.at.number_input if x.label=='Entry amount (₱)').set_value(200.)
        next(b for b in self.at.button if b.label=='Save money entry').click().run()
        self.assertEqual(next(m for m in self.at.metric if m.label=='Expenses').value,'₱200.00')
        next(b for b in self.at.button if b.label=='Remove transaction').click().run()
        self.assertEqual(next(m for m in self.at.metric if m.label=='Expenses').value,'₱0.00')
        self.assert_clean()

    def test_day_schedule_saves_and_checkin_preserves_it(self):
        self.nav('Planner')
        next(b for b in self.at.button if b.label=='Save schedule').click().run()
        self.assert_clean()
        check=next(iter(self.data['checkins'].values()))
        self.assertIsInstance(check['schedule'],list)
        self.nav('Today')
        next(b for b in self.at.button if b.label=='Shape my day').click().run()
        self.assertEqual(next(iter(self.data['checkins'].values()))['schedule'],check['schedule'])
        self.nav('Planner')
        next(b for b in self.at.button if b.label=='Reset this day to my routine').click().run()
        self.assertNotIn('schedule',next(iter(self.data['checkins'].values())))
        self.assert_clean()

    def test_schedule_grid_edits_and_empty_routine(self):
        self.data['profile']['main']['routine']=[]
        self.nav('Your space')
        self.assert_clean()
        self.nav('Planner')
        next(x for x in self.at.date_input if x.label=='Plan for').set_value(date(2026,10,26)).run()
        # Exercise the grid edit payload that the browser sends to Streamlit.
        grid='daily_schedule_2026-10-26_0'
        self.at.session_state[grid]={'edited_rows':{0:{'Activity':'Shift changed','Start':'10:00:00','End':'14:00:00'}},'added_rows':[],'deleted_rows':[]}
        next(b for b in self.at.button if b.label=='Save schedule').click().run()
        self.assert_clean()
        schedule=next(iter(self.data['checkins'].values()))['schedule']
        self.assertEqual(schedule[0]['title'],'Shift changed')
        self.assertEqual(schedule[0]['start'],600)
        self.assertEqual(schedule[0]['end'],840)

    def test_focus_task_routes_and_marks_ongoing(self):
        self.nav('Planner')
        next(b for b in self.at.button if b.key=='taskfocusgraduation').click().run()
        self.assert_clean()
        self.assertEqual(self.data['tasks']['graduation']['status'],'Ongoing')
        self.assertEqual(self.at.session_state['page'],'Focus')
        self.assertEqual(self.at.session_state['timer']['minutes'],5)

    def test_compact_navigation_and_touch_schedule_form(self):
        next(x for x in self.at.selectbox if x.key=='compact_page').set_value('Planner').run()
        self.assertEqual(self.at.session_state['page'],'Planner')
        next(x for x in self.at.text_input if x.label=='New block activity').set_value('Walk outside')
        next(b for b in self.at.button if b.label=='Add time block').click().run()
        self.assert_clean()
        saved=next(iter(self.data['checkins'].values()))['schedule']
        self.assertTrue(any(b['title']=='Walk outside' for b in saved))
        key=next(b.key for b in self.at.button if b.key and '_remove_' in b.key and b.key.endswith('_'+str(len(saved)-1)))
        next(b for b in self.at.button if b.key==key).click().run()
        self.assert_clean()
        self.assertFalse(any(b['title']=='Walk outside' for b in next(iter(self.data['checkins'].values()))['schedule']))

if __name__=='__main__': unittest.main()
