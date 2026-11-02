import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import verify_repo


class PrivateMaterialDetectionTests(unittest.TestCase):
    def setUp(self):
        label = "PRIVATE" + chr(32) + "KEY"
        self.begin = "-----BEGIN " + label + "-----"
        self.end = "-----END " + label + "-----"
        self.pattern = verify_repo.SECRET_PATTERNS["Private key block"]

    def test_marker_only_documentation_placeholder_is_not_a_secret(self):
        sample = self.begin + "\n...\n" + self.end
        self.assertIsNone(self.pattern.search(sample))

    def test_base64_key_material_is_detected(self):
        sample = self.begin + "\n" + ("A" * 128) + "\n" + self.end
        self.assertIsNotNone(self.pattern.search(sample))

    def test_scanner_detects_private_key_spanning_multiple_lines(self):
        sample = self.begin + "\n" + ("A" * 64) + "\n" + ("B" * 64) + "\n" + self.end
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".md", dir=Path(__file__).parent, delete=False) as f:
            f.write(sample)
            path = Path(f.name)
        try:
            with patch.object(verify_repo, "iter_files", return_value=iter([path])):
                output = StringIO()
                with redirect_stdout(output):
                    self.assertFalse(verify_repo.scan_secrets())
                self.assertIn("Private key block", output.getvalue())
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
