import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from evolution import rank_candidates, validate_topology, feedback_decision, validate_law_proposal


class EvolutionTests(unittest.TestCase):
    def test_rank_candidates_prefers_verified_complete_branch(self):
        candidates = [
            {"id":"branch-a","tests_passed":3,"tests_total":3,"breaker_resolved":True,
             "risk_score":0.1,"complexity":0.2,"evidence_sha256":"a"*64},
            {"id":"branch-b","tests_passed":2,"tests_total":3,"breaker_resolved":True,
             "risk_score":0.2,"complexity":0.1,"evidence_sha256":"b"*64},
        ]
        ranked = rank_candidates(candidates)
        self.assertEqual(ranked[0]["id"], "branch-a")
        self.assertTrue(ranked[0]["eligible"])

    def test_rank_candidates_rejects_missing_or_invalid_evidence(self):
        ranked = rank_candidates([
            {"id":"unverified","tests_passed":3,"tests_total":3,"breaker_resolved":True,
             "risk_score":0,"complexity":0,"evidence_sha256":"not-a-hash"}
        ])
        self.assertFalse(ranked[0]["eligible"])

    def test_topology_requires_independent_read_only_magistrate(self):
        topology = [
            {"id":"breaker","role":"breaker","permissions":["read","test"],"sandboxed":True},
            {"id":"builder","role":"builder","permissions":["read","write_branch","test"],"sandboxed":True},
            {"id":"magistrate","role":"magistrate","permissions":["read","test"],"sandboxed":True},
        ]
        result = validate_topology(topology)
        self.assertTrue(result["valid"])

    def test_topology_rejects_magistrate_write_authority(self):
        topology = [
            {"id":"breaker","role":"breaker","permissions":["read","test"],"sandboxed":True},
            {"id":"builder","role":"builder","permissions":["read","write_branch","test"],"sandboxed":True},
            {"id":"magistrate","role":"magistrate","permissions":["read","write_branch"],"sandboxed":True},
        ]
        result = validate_topology(topology)
        self.assertFalse(result["valid"])

    def test_feedback_loop_is_bounded(self):
        self.assertEqual(feedback_decision(attempt=1,max_attempts=3,passed=False),"repair")
        self.assertEqual(feedback_decision(attempt=3,max_attempts=3,passed=False),"escalate")
        self.assertEqual(feedback_decision(attempt=1,max_attempts=3,passed=True),"complete")

    def test_law_update_is_proposal_only_and_cannot_weaken_invariants(self):
        current={"version":1,"invariants":["magistrate_read_only","sealed_plan","no_auto_deploy"]}
        safe={"version":2,"invariants":["magistrate_read_only","sealed_plan","no_auto_deploy","max_feedback_attempts=3"],"evidence_sha256":"c"*64}
        unsafe={"version":2,"invariants":["sealed_plan"],"evidence_sha256":"d"*64}
        self.assertTrue(validate_law_proposal(current,safe)["valid"])
        self.assertFalse(validate_law_proposal(current,unsafe)["valid"])


if __name__ == "__main__":
    unittest.main()
