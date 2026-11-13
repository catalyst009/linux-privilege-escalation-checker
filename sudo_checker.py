import os
import subprocess


def check_sudo():
    """Check sudo privileges and sudoers file permissions without hanging."""
    findings = []

    try:
        result = subprocess.run(
            ["sudo", "-n", "-l"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            for line in result.stdout.splitlines():
                line = line.strip()
                if "NOPASSWD" in line or "(ALL" in line or "(root)" in line:
                    findings.append({
                        "category": "Sudo Configuration",
                        "item": line,
                        "details": "Elevated sudo execution rule detected for current user.",
                        "raw_identifier": line.split()[-1] if line.split() else line
                    })
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        pass

    if os.path.exists("/etc/sudoers") and os.access("/etc/sudoers", os.R_OK) and os.geteuid() != 0:
        findings.append({
            "category": "Sudo Configuration",
            "item": "/etc/sudoers",
            "details": "The /etc/sudoers file is readable by a non-root user.",
            "raw_identifier": "/etc/sudoers"
        })

    return findings
