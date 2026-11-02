import os
import tempfile
import unittest
from pathlib import Path

from oh_my_agent.server import skills_list


class SkillsListTests(unittest.TestCase):
    def test_deduplicates_and_paginates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root_a = Path(tmp) / "a"
            root_b = Path(tmp) / "b"
            for root, names in ((root_a, ("alpha", "beta")), (root_b, ("alpha", "gamma"))):
                for name in names:
                    d = root / name
                    d.mkdir(parents=True, exist_ok=True)
                    (d / "SKILL.md").write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
            (root_a / "not-a-skill").mkdir()
            old = os.environ.get("OHMA_SKILL_ROOTS")
            os.environ["OHMA_SKILL_ROOTS"] = os.pathsep.join((str(root_a), str(root_b)))
            try:
                first = skills_list({"limit": 2, "offset": 0})
                second = skills_list({"limit": 2, "offset": 2})
            finally:
                if old is None:
                    os.environ.pop("OHMA_SKILL_ROOTS", None)
                else:
                    os.environ["OHMA_SKILL_ROOTS"] = old
            self.assertEqual(first["total"], 3)
            self.assertEqual(first["count"], 2)
            self.assertEqual(second["count"], 1)
            names = [x["name"] for x in first["skills"] + second["skills"]]
            self.assertEqual(names, ["alpha", "beta", "gamma"])
            self.assertTrue(all(x["has_skill_md"] for x in first["skills"] + second["skills"]))


if __name__ == "__main__":
    unittest.main()
