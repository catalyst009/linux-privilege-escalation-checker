import os
import socket
import tempfile
import unittest

from report_generator import generate_report


class TestGenerateReport(unittest.TestCase):

    def test_wrong_format_raises_error(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                generate_report({"hostname": "kali"}, [], folder, "pdf")

    def test_no_findings_saves_report(self):
        with tempfile.TemporaryDirectory() as folder:
            path = generate_report({"hostname": "kali"}, [], folder, "txt")
            with open(path, encoding="utf-8") as f:
                self.assertIn("FINDINGS (0)", f.read())

    def test_missing_hostname_uses_computer_name(self):
        with tempfile.TemporaryDirectory() as folder:
            path = generate_report({}, [], folder, "json")
            filename = os.path.basename(path)
            self.assertTrue(filename.startswith(socket.gethostname()))

    def test_missing_keys_show_na(self):
        with tempfile.TemporaryDirectory() as folder:
            findings = [{"check": "Cron"}]
            path = generate_report({"hostname": "kali"}, findings, folder, "txt")
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Risk: N/A", content)
            self.assertIn("Fix: N/A", content)

    def test_real_finding_keys_in_txt(self):
        with tempfile.TemporaryDirectory() as folder:
            findings = [{
                "category": "SUID Binary",
                "item": "/usr/bin/ntfs-3g",
                "risk": "Medium",
                "details": "SUID bit set (permissions: 4755).",
                "reason": "Requires further security review.",
                "recommendation": "Confirm the package is required.",
            }]
            path = generate_report({"hostname": "kali"}, findings, folder, "txt")
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("SUID Binary: /usr/bin/ntfs-3g", content)
            self.assertIn("Reason: Requires further security review.", content)


if __name__ == "__main__":
    unittest.main()
