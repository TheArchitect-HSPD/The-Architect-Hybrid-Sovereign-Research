import unittest
from engine import AGENTS, SCENARIOS, run_case, batch


class SandboxTests(unittest.TestCase):
    def test_registry(self):
        self.assertEqual(len(AGENTS),21)
        self.assertEqual(len({x['name'] for x in AGENTS}),21)
        self.assertEqual(AGENTS[-1]['name'],'The Arbiter')

    def test_exact_replay(self):
        first=run_case('copied_false_consensus',42,'arbiter')
        self.assertEqual(first,run_case('copied_false_consensus',42,'arbiter'))
        self.assertEqual(len(first['trace']),21)

    def test_majority_fails_false_consensus(self):
        self.assertEqual(run_case('copied_false_consensus',1,'majority')['correct_classification'],False)
        self.assertEqual(run_case('copied_false_consensus',1,'arbiter')['recommendation'],'HOLD_UNCERTAINTY')

    def test_independent_true_evidence_allowed_for_human_review(self):
        self.assertEqual(run_case('independently_confirmed_true',1,'arbiter')['recommendation'],'REQUEST_HUMAN_REVIEW')

    def test_intervention_data_excluded(self):
        r=run_case('intervention_feedback',1,'arbiter')
        self.assertEqual(r['correct_classification'],True)
        self.assertTrue(any('Excluded intervention-generated' in x for x in r['alerts']))

    def test_known_spoofing_failure_is_visible(self):
        r=run_case('spoofed_source_origins',1,'arbiter')
        self.assertFalse(r['correct_classification'])

    def test_true_event_can_be_missed(self):
        self.assertFalse(run_case('single_source_true',1,'arbiter')['correct_classification'])

    def test_ambiguous_case_not_scored(self):
        self.assertIsNone(run_case('mixed_unknown',1,'arbiter')['correct_classification'])

    def test_seed_changes_order_not_outcome(self):
        a=run_case('copied_false_consensus',1,'arbiter');b=run_case('copied_false_consensus',56,'arbiter')
        self.assertNotEqual([x['id'] for x in a['evidence']],[x['id'] for x in b['evidence']])
        self.assertEqual(a['recommendation'],b['recommendation'])

    def test_batch_size(self):
        self.assertEqual(len(batch(2)),len(SCENARIOS)*3*2)

    def test_safety_guards(self):
        with self.assertRaises(ValueError):run_case('unknown',1,'arbiter')
        with self.assertRaises(ValueError):run_case('copied_false_consensus',-5,'arbiter')
        with self.assertRaises(ValueError):run_case('copied_false_consensus',1,'danger')


if __name__=='__main__':unittest.main()
