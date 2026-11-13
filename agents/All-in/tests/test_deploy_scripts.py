import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DeployScriptTests(unittest.TestCase):
    def test_safe_install_is_project_local_and_preserves_existing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "All-in"
            (root / "skills" / "alpha").mkdir(parents=True)
            (root / "skills" / "alpha" / "SKILL.md").write_text("new-alpha")
            (root / "skills" / "beta").mkdir()
            (root / "skills" / "beta" / "SKILL.md").write_text("new-beta")
            target = root / ".openhands" / "skills"
            (target / "alpha").mkdir(parents=True)
            (target / "alpha" / "SKILL.md").write_text("existing-alpha")
            script = ROOT / "deploy" / "safe-install.sh"
            proc = subprocess.run(["bash", str(script), "--apply"], env={**os.environ, "ALLIN_ROOT": str(root)}, text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual((target / "alpha" / "SKILL.md").read_text(), "existing-alpha")
            self.assertEqual((target / "beta" / "SKILL.md").read_text(), "new-beta")
            self.assertFalse((Path.home() / ".claude" / "skills" / "beta").exists())
            self.assertFalse((Path.home() / ".agents" / "skills" / "beta").exists())

    def test_safe_install_defaults_to_dry_run(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "All-in"
            (root / "skills" / "alpha").mkdir(parents=True)
            (root / "skills" / "alpha" / "SKILL.md").write_text("alpha")
            proc = subprocess.run(["bash", str(ROOT / "deploy" / "safe-install.sh")], env={**os.environ, "ALLIN_ROOT": str(root)}, text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("DRY_RUN_ONLY", proc.stdout)
            self.assertFalse((root / ".openhands" / "skills" / "alpha" / "SKILL.md").exists())

    def test_verify_script_uses_injected_checks_and_is_read_only(self):
        with tempfile.TemporaryDirectory() as td:
            bin_dir = Path(td) / "bin"
            bin_dir.mkdir()
            for name, body in {
                "systemctl": "#!/bin/sh\n[ \"$1\" = is-active ] && exit 0\nexit 1\n",
                "curl": "#!/bin/sh\necho 200\n",
                "docker": "#!/bin/sh\ncase \"$1\" in ps|volume) echo fake-id;; esac\n",
                "df": "#!/bin/sh\necho 'Filesystem 1024-blocks Used Available Capacity Mounted on'; echo '/dev/fake 1000 400 600 40% /'\n",
            }.items():
                p = bin_dir / name
                p.write_text(body)
                p.chmod(0o755)
            env = {**os.environ, "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
                   "CHECK_UNITS": "fake-a fake-b", "CHECK_URLS": "canvas=http://127.0.0.1/health",
                   "CHECK_DOCKER": "1", "DISK_WARN_PERCENT": "90"}
            proc = subprocess.run(["bash", str(ROOT / "deploy" / "verify-current-vps.sh")], env=env, text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("fake-a", proc.stdout)
            self.assertIn("canvas", proc.stdout)
            self.assertIn("PASS", proc.stdout)


if __name__ == "__main__":
    unittest.main()
