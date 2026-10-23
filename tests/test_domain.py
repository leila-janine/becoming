import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from domain import *
from storage import LocalStore, MemoryStore, export_records

class DomainTests(unittest.TestCase):
    def setUp(self):
        self.profile=default_profile()
        self.day=date(2026,10,26) # Monday
        self.current=datetime(2026,10,23,7,0,tzinfo=TZ)
    def task(self,**extra):
        return {'id':'a','title':'Task','next':'Start','area':'Career','minutes':25,'priority':2,'due':None,'window':None,'done':False,**extra}
    def test_work_meals_events_never_overlap_focus(self):
        events=[{'date':str(self.day),'start':'07:00','end':'08:00','title':'Appointment'}]
        p=make_plan(self.profile,self.day,[self.task(id=str(i)) for i in range(6)],events,90,5,current=self.current)
        for t in p['plan']:
            for b in p['blocks']:
                self.assertTrue(t['end']<=b['start'] or t['start']>=b['end'])
        self.assertLessEqual(p['used'],90)
        self.assertLessEqual(len(p['plan']),3)
    def test_optical_window_conflicts_with_work(self):
        t=self.task(minutes=60,window=['10:00','15:00'])
        p=make_plan(self.profile,self.day,[t],[],90,5,current=self.current)
        self.assertEqual(p['plan'],[])
        self.assertEqual(len(p['deferred']),1)
        p=make_plan(self.profile,date(2026,10,24),[t],[],90,5,current=self.current)
        self.assertEqual(p['plan'][0]['start'],600)
        p=make_plan(self.profile,self.day,[t],[],90,5,leave=True,current=self.current)
        self.assertEqual(p['plan'][0]['start'],600)
    def test_low_energy_one_short_step(self):
        p=make_plan(self.profile,self.day,[self.task(id=str(i)) for i in range(5)],[],120,1,current=self.current)
        self.assertEqual(len(p['plan']),1)
        self.assertLessEqual(p['used'],15)
        self.assertTrue(p['plan'][0]['slice'])
    def test_zero_budget(self):
        p=make_plan(self.profile,self.day,[self.task()],[],0,current=self.current)
        self.assertFalse(p['plan'])
    def test_past_time_is_not_scheduled(self):
        current=datetime(2026,10,26,20,30,tzinfo=TZ)
        p=make_plan(self.profile,self.day,[self.task()],[],30,current=current)
        self.assertGreater(p['plan'][0]['start'],1230)
    def test_future_task_and_done_task_excluded(self):
        p=make_plan(self.profile,self.day,[self.task(not_before='2026-11-01'),self.task(id='b',done=True)],[],60,current=self.current)
        self.assertFalse(p['plan'])
    def test_interval_subtraction(self):
        self.assertEqual(subtract_intervals(0,100,[(10,40),(20,60),(90,120)]),[(0,10),(60,90)])
    def test_budget_shortfall(self):
        self.assertEqual(budget_summary({'income':1000,'needs':800,'joy':300})['remaining'],-100)
    def test_goal_edge_cases(self):
        self.assertEqual(months_to_goal(0,100000,1500),67)
        self.assertIsNone(months_to_goal(0,100,0))
        self.assertEqual(months_to_goal(100,100,0),0)
    def test_recall_intervals(self):
        self.assertEqual(next_review(0,True,self.day),(1,'2026-10-27'))
        self.assertEqual(next_review(2,True,self.day),(4,'2026-10-30'))
        self.assertEqual(next_review(20,False,self.day),(1,'2026-10-27'))
    def test_sqlite_persists_and_updates(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'records.sqlite'
            a=LocalStore(path); a.put('tasks',self.task())
            b=LocalStore(path); self.assertEqual(len(b.all('tasks')),1)
            b.put('tasks',self.task(done=True)); self.assertTrue(a.all('tasks')[0]['done'])
            self.assertEqual(export_records(a)['format'],'becoming-v1')
            a.delete('tasks','a'); self.assertFalse(b.all('tasks'))

if __name__=='__main__': unittest.main()
