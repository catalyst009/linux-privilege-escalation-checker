import os
import platform
import pwd
import subprocess


def get_system_info():
    """Collect basic local Linux system and user context."""
    return {
        "os": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "hostname": platform.node(),
        "current_user": pwd.getpwuid(os.getuid()).pw_name,
        "uid": os.getuid()
    }


def check_capabilities(target_paths=None):
    """Identify binaries with sensitive Linux capabilities assigned."""
    if target_paths is None:
        target_paths = ["/usr/bin", "/usr/local/bin"]

    findings = []
    sensitive_caps = ("cap_setuid", "cap_setgid", "cap_dac_override", "cap_sys_admin")

    for path in target_paths:
        if not os.path.exists(path):
            continue

        try:
            result = subprocess.run(
                ["getcap", "-r", path],
                capture_output=True,
                text=True,
                timeout=10
            )
            for line in result.stdout.splitlines():
                if any(cap in line for cap in sensitive_caps):
                    binary_path = line.split()[0]
                    findings.append({
                        "category": "Linux Capabilities",
                        "item": line.strip(),
                        "details": "Binary has high-privilege Linux capabilities assigned.",
                        "raw_identifier": os.path.basename(binary_path)
                    })
        except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError):
            continue

    return findings
