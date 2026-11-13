import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "emat.py"
SPEC = importlib.util.spec_from_file_location("emat", SCRIPT)
emat = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(emat)


class EmatTests(unittest.TestCase):
    def test_seal_is_stable_and_detects_tampering(self):
        plan = {
            "objective": "test",
            "baseline_revision": "abc123",
            "acceptance_criteria": ["all pass"],
            "allowed_paths": ["src/**"],
            "forbidden_paths": [".env"],
            "test_commands": [["python", "-m", "unittest"]],
        }
        envelope = {"schema": "emat.sealed-plan.v1", "plan": plan, "plan_sha256": emat.sha256_bytes(emat.canonical_bytes(plan))}
        self.assertEqual(emat.check_seal(envelope), (True, envelope["plan_sha256"]))
        envelope["plan"]["objective"] = "tampered"
        self.assertFalse(emat.check_seal(envelope)[0])

    def test_verdict_ledger_hash_chain(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = Path(temp) / "verdicts.jsonl"
            record = {"schema": "emat.verdict.v1", "status": "PASS", "previous_record_sha256": "0" * 64}
            record["record_sha256"] = emat.sha256_bytes(emat.canonical_bytes(record))
            ledger.write_text(emat.canonical_bytes(record).decode(), encoding="utf-8")
            previous = "0" * 64
            parsed = json.loads(ledger.read_text())
            supplied = parsed.pop("record_sha256")
            self.assertEqual(parsed["previous_record_sha256"], previous)
            self.assertEqual(supplied, emat.sha256_bytes(emat.canonical_bytes(parsed)))


if __name__ == "__main__":
    unittest.main()
