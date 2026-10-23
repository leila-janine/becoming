import unittest
from coding import CHALLENGES
from coding_runner import runner_config, validate_editor_result


class RunnerContractTests(unittest.TestCase):
    def test_supported_challenges_include_checks_and_draft(self):
        for challenge in CHALLENGES:
            config=runner_config(challenge,'my saved draft')
            if challenge['extension'] in ['py','sql']:
                self.assertEqual(config['code'],'my saved draft')
                self.assertEqual(config['challengeId'],challenge['id'])
                self.assertTrue(config['checks'] or config['expected'])
                if challenge['extension']=='sql': self.assertIn('CREATE TEMP TABLE',config['setup'])
            else: self.assertIsNone(config)

    def test_only_bounded_known_editor_reports_are_accepted(self):
        valid={'code':'print(1)','revision':'run-1','status':'passed','unexpected':'discard me'}
        self.assertEqual(validate_editor_result(valid),{'code':'print(1)','revision':'run-1','status':'passed'})
        for invalid in [None,{}, {**valid,'code':'x'*30001},{**valid,'status':'server-verified'},{**valid,'revision':1}]:
            self.assertIsNone(validate_editor_result(invalid))
