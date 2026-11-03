import subprocess
import unittest
import urllib.error
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import refresh_upstreams


class ResolveGitHeadTests(unittest.TestCase):
    def test_private_repository_falls_back_to_git_ls_remote(self):
        api_error = urllib.error.HTTPError(
            url="https://api.github.com/repos/private/repo/commits/main",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=None,
        )
        completed = subprocess.CompletedProcess(
            args=["git", "ls-remote"],
            returncode=0,
            stdout="0123456789abcdef0123456789abcdef01234567\trefs/heads/main\n",
            stderr="",
        )
        with patch.object(refresh_upstreams, "request_json", side_effect=api_error):
            with patch("subprocess.run", return_value=completed):
                resolved, error = refresh_upstreams.resolve_git_head(
                    "git@github.com:private/repo.git", "main", None
                )
        self.assertEqual(resolved, "0123456789abcdef0123456789abcdef01234567")
        self.assertIsNone(error)


class RuntimeUpgradeTests(unittest.TestCase):
    def test_npm_package_resolution_does_not_overwrite_runtime_product_version(self):
        payload = {
            "sources": [{"id": "cline", "kind": "npm", "resolved": "0.0.13"}]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runtime-sources.yaml"
            path.write_text(
                "runtimes:\n  cline:\n    package_version: 3.0.62\n    runtime_version: 3.0.62\n",
                encoding="utf-8",
            )
            examined, updated = refresh_upstreams.apply_upgrades_to_runtime_sources(payload, path)
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(examined, 1)
        self.assertEqual(updated, 1)
        self.assertEqual(data["runtimes"]["cline"]["package_version"], "0.0.13")
        self.assertEqual(data["runtimes"]["cline"]["runtime_version"], "3.0.62")

    def test_lower_npm_version_is_flagged_and_not_selected(self):
        inventory = {"version": 1, "sources": [{"id": "pkg", "kind": "npm", "package": "pkg", "version": "3.0.0", "required": True}]}
        with patch.object(refresh_upstreams, "resolve_npm_latest", return_value=("0.9.0", None)):
            lock, report = refresh_upstreams.refresh(inventory, {"sources": []})
        item = lock["sources"][0]
        self.assertEqual(item["resolved"], "3.0.0")
        self.assertEqual(item["status"], "degraded")
        self.assertIn("npm_version_downgrade_detected", item["error"])
        self.assertTrue(report["requires_manual_attention"])


if __name__ == "__main__":
    unittest.main()
