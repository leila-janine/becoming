import sys
import unittest
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from domain import default_profile, day_blocks, make_plan, task_status, validate_schedule, TZ
from focus_timer import start_timer, remaining, pause, resume, advance
from money_analytics import money_dashboard, previous_month
from storage import MemoryStore, export_records, validate_backup


class PlannerTests(unittest.TestCase):
    def test_daily_changes_replace_defaults_and_empty_schedule_means_free_day(self):
        profile=default_profile(); day=date(2026,10,26)
        schedule=[{'title':'Changed shift','start':660,'end':900,'kind':'work'}]
        task={'id':'t','title':'Repair glasses','minutes':60,'priority':2,'window':['10:00','15:00'],'done':False}
        plan=make_plan(profile,day,[task],[],90,5,current=datetime(2026,10,25,tzinfo=TZ),schedule=schedule)
        self.assertEqual(plan['plan'][0]['start'],600)
        self.assertEqual(plan['blocks'],schedule)
        self.assertEqual(day_blocks(profile,day,[],schedule=[]),[])
        self.assertEqual(day_blocks(profile,day,[],leave=True,schedule=schedule),[])

    def test_recurring_blocks_and_date_specific_appointments(self):
        profile={**default_profile(),'routine':[]}
        events=[{'date':'2026-10-26','title':'School','start':'19:00','end':'20:00'}]
        blocks=day_blocks(profile,date(2026,10,26),events,schedule=[])
        self.assertEqual([b['title'] for b in blocks],['School'])
        self.assertEqual(day_blocks(profile,date(2026,10,27),events,schedule=[]),[])
        self.assertEqual(len(day_blocks(profile,date(2026,10,26),[])),1)

    def test_invalid_schedule_cannot_be_restored(self):
        for block in [{'title':'','start':10,'end':20,'kind':'rest'},
                      {'title':'Late','start':1380,'end':60,'kind':'rest'},
                      {'title':'Invalid','start':10,'end':20,'kind':'unknown'}]:
            with self.assertRaises(ValueError): validate_schedule([block])
        store=MemoryStore({})
        store.put('checkins',{'id':'2026-10-26','energy':3,'minutes':45,'schedule':[{'title':'Broken','start':120,'end':60,'kind':'rest'}]})
        with self.assertRaises(ValueError): validate_backup(export_records(store))

    def test_status_compatibility(self):
        self.assertEqual(task_status({'done':False}),'New')
        self.assertEqual(task_status({'done':False,'status':'Ongoing'}),'Ongoing')
        self.assertEqual(task_status({'done':True,'status':'Ongoing'}),'Completed')


class TimerTests(unittest.TestCase):
    def test_pause_does_not_consume_time_and_resume_rebases_clock(self):
        timer=start_timer('Read',25,stamp=100)
        paused=pause(timer,stamp=160)
        self.assertEqual(remaining(paused,stamp=5000),1440)
        running=resume(paused,stamp=5000)
        self.assertEqual(remaining(running,stamp=5060),1380)
        self.assertEqual(remaining(running,stamp=7000),0)

    def test_breaks_and_fourth_interval_long_break(self):
        timer=start_timer('Build',25,5,15,4,stamp=0)
        for n in range(1,5):
            self.assertEqual(timer['phase'],'Focus')
            self.assertEqual(timer['round'],n)
            timer=advance(timer,stamp=100)
            self.assertEqual(timer['phase'],'Long break' if n==4 else 'Short break')
            self.assertEqual(timer['duration'],900 if n==4 else 300)
            timer=advance(timer,stamp=200)
            self.assertEqual(timer['duration'],1500)


class MoneyTests(unittest.TestCase):
    def tx(self,kind,amount,category='Other',day='2026-10-10'):
        return {'date':day,'type':kind,'amount':amount,'category':category}

    def test_transfers_not_spending_future_excluded_and_months_separated(self):
        rows=[self.tx('Income',20000),self.tx('Expense',200,'Enjoyment'),self.tx('Expense',300,'Essentials'),
              self.tx('Savings transfer',1500),self.tx('Investment transfer',500),
              self.tx('Expense',9000,'Enjoyment','2026-10-30'),self.tx('Expense',100,'Enjoyment','2026-09-10')]
        data=money_dashboard(rows,'2026-10',{'joy':1000,'needs':500},date(2026,10,23))
        self.assertEqual(data['income'],20000)
        self.assertEqual(data['expense'],500)
        self.assertEqual(data['transfers'],2000)
        self.assertEqual(data['net'],17500)
        self.assertEqual(data['previous']['expense'],100)
        self.assertEqual(data['comparison'][1]['Remaining (₱)'],800)
        self.assertEqual(data['expense_count'],2)

    def test_no_data_and_year_boundary(self):
        self.assertEqual(previous_month('2026-01'),'2025-12')
        data=money_dashboard([],'2026-01',{},date(2026,10,23))
        self.assertEqual(data['net'],0)
        self.assertEqual(data['categories'],{})
        self.assertEqual(len(data['trend']),6)
        self.assertEqual(data['trend'][0]['Month'],'2025-08')

    def test_comparable_prior_period_and_decimal_amounts(self):
        rows=[self.tx('Expense',0.1,day='2026-10-01'),self.tx('Expense',0.2,day='2026-10-02'),
              self.tx('Expense',50,day='2026-09-24')]
        data=money_dashboard(rows,'2026-10',{},date(2026,10,23))
        self.assertEqual(data['expense'],0.3)
        self.assertEqual(data['previous']['expense'],0)

    def test_complete_historical_month_compares_full_previous_month(self):
        rows=[self.tx('Expense',100,day='2026-01-31')]
        data=money_dashboard(rows,'2026-02',{},date(2026,10,23))
        self.assertEqual(data['previous']['expense'],100)
        self.assertEqual(data['previous_cutoff'],'2026-01-31')


if __name__=='__main__': unittest.main()
