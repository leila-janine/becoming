import contextlib
import io
import sqlite3
from pathlib import Path
from datetime import date
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coding import CHALLENGES, practice_file, recommend, review_date


class CodingContentTests(unittest.TestCase):
    def test_authored_python_solutions_pass_checks(self):
        for challenge in CHALLENGES:
            if challenge['extension']=='py':
                with self.subTest(challenge=challenge['id']), contextlib.redirect_stdout(io.StringIO()):
                    # Only trusted, authored solutions are executed here. The app never runs submitted code.
                    exec(compile(practice_file(challenge,True),challenge['id'],'exec'),{})
    def test_sql_solution_keeps_zero_activity_user(self):
        challenge=next(c for c in CHALLENGES if c['id']=='sql-zero')
        with sqlite3.connect(':memory:') as db:
            db.executescript(challenge['setup'])
            self.assertEqual(db.execute(challenge['solution']).fetchall(),[(1,'Aya',3500),(2,'Mika',0),(3,'Lea',500)])
    def test_recommendation_prefers_due_review(self):
        options=[c for c in CHALLENGES if c['track']=='Python']
        result,_=recommend(options,[{'challenge_id':options[1]['id'],'review_on':'2026-10-22','logged_at':'2026-10-21T10:00:00'}],date(2026,10,23))
        self.assertEqual(result['id'],options[1]['id'])
    def test_review_is_soon_when_help_or_failure(self):
        self.assertEqual(review_date(date(2026,10,23),True,True),'2026-10-26')
        self.assertEqual(review_date(date(2026,10,23),False,True),'2026-10-24')
        self.assertEqual(review_date(date(2026,10,23),True,False),'2026-10-24')

if __name__=='__main__': unittest.main()
