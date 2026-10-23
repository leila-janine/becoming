import os
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP=Path(__file__).resolve().parents[1]/'app.py'

class AppTests(unittest.TestCase):
    def setUp(self):
        os.environ.pop('BECOMING_LOCAL',None)
        self.at=AppTest.from_file(str(APP),default_timeout=20)
        self.at.run()
        self.at.button[0].click().run()
    def assert_clean(self):
        self.assertFalse(self.at.exception, str(self.at.exception))
    def nav(self,page):
        self.at.sidebar.radio[0].set_value(page).run()
        self.assert_clean()
    def test_every_page_renders(self):
        self.assert_clean()
        for page in ['Planner','Focus','Coding practice','Career & learning','Job market','Voice & confidence','Money','Reflect','Resources','Your space','Today']:
            self.nav(page)
    def test_checkin_persists(self):
        self.at.text_input[0].set_value('One useful next step')
        next(b for b in self.at.button if b.label=='Shape my day').click().run()
        self.assert_clean()
        data=self.at.session_state['demo_records']['checkins']
        self.assertEqual(next(iter(data.values()))['intention'],'One useful next step')
    def test_money_plan(self):
        self.nav('Money')
        for label,amount in [('Expected take-home income (₱)',20000.),('Essentials & debt payments (₱)',12000.),('Enjoyment I choose (₱)',1500.),('Emergency savings contribution (₱)',1000.)]:
            next(x for x in self.at.number_input if x.label==label).set_value(amount)
        next(b for b in self.at.button if b.label=='Save my monthly plan').click().run()
        self.assert_clean()
        self.assertEqual(self.at.metric[2].value,'₱5,500')
    def test_task_creation(self):
        self.nav('Planner')
        inputs=self.at.text_input
        next(x for x in inputs if x.label=='Task').set_value('Portfolio update')
        next(x for x in inputs if x.label=='Smallest useful next action').set_value('Write one README paragraph')
        next(b for b in self.at.button if b.label=='Save task').click().run()
        self.assert_clean()
        self.assertTrue(any(x['title']=='Portfolio update' for x in self.at.session_state['demo_records']['tasks'].values()))
    def test_focus_timer(self):
        self.nav('Focus')
        next(x for x in self.at.text_input if x.label=='What will I work on?').set_value('Read the schema')
        next(b for b in self.at.button if b.label=='Begin focus').click().run()
        self.assert_clean()
        self.assertEqual(self.at.session_state['timer']['minutes'],15)
        next(b for b in self.at.button if b.label=='End timer without logging').click().run()
        self.assert_clean()

    def test_coding_practice_and_debugging(self):
        self.nav('Coding practice')
        next(x for x in self.at.text_area if x.label=='My approach and edge cases').set_value('Use a set plus a list; test empty input.')
        next(x for x in self.at.text_input if x.label=='What I learned / what I will change next').set_value('Preserve the order of first occurrence.')
        next(b for b in self.at.button if b.label=='Save coding practice').click().run()
        self.assert_clean()
        attempts=self.at.session_state['demo_records']['coding']
        self.assertEqual(len(attempts),1)
        self.assertEqual(len(self.at.session_state['demo_records']['sessions']),1)
        next(x for x in self.at.text_input if x.label=='Bug or confusing behavior').set_value('Shared state')
        next(x for x in self.at.text_area if x.label=='Actual behavior / exact error').set_value('A new call retains an old task.')
        next(b for b in self.at.button if b.label=='Keep this debugging lesson').click().run()
        self.assert_clean()
        self.assertEqual(len(self.at.session_state['demo_records']['coding']),2)
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
        tasks=self.at.session_state['demo_records']['tasks'].values()
        self.assertTrue(any(t['title']=='Practice · Evaluate binary predictions' for t in tasks))

    def test_job_market_evidence_mapping(self):
        self.nav('Job market')
        next(b for b in self.at.button if b.key=='exampleaccenture-r00288844').click().run()
        self.assert_clean()
        next(x for x in self.at.selectbox if x.label=='Evidence type').set_value('Research / project evidence')
        next(x for x in self.at.text_input if x.label=='Specific example / proof link').set_value('My local RAG evaluation notes')
        next(b for b in self.at.button if b.label=='Save requirement mapping').click().run()
        self.assert_clean()
        row=self.at.session_state['demo_records']['jobs']['accenture-r00288844']
        self.assertEqual(row['status'],'Research example')
        self.assertTrue(any(v['detail']=='My local RAG evaluation notes' for v in row['evidence_map'].values()))

    def test_ai_is_primary(self):
        self.assertEqual(self.at.session_state['demo_records']['profile']['main']['target_role'],'AI Engineer')
        self.nav('Career & learning')
        self.assertEqual(next(x for x in self.at.selectbox if x.label=='My current direction').value,'AI Engineer')

if __name__=='__main__': unittest.main()
