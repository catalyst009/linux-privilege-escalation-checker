
"""Member 3: Linux Privilege Escalation Risk Assessment."""

import grp
import os
import re
import stat
import subprocess

# Programs potentially dangerous when assigned SUID permissions
DANGEROUS_BINARIES = {
    "find", "vim", "vi", "nvim", "nano",
    "perl", "ruby", "bash", "sh", "dash",
    "zsh", "env", "awk", "gawk",
    "less", "more", "cp", "tar",
    "nmap", "php", "node", "busybox",
}

# Expected SGID configurations on Debian/Kali systems
# Format: allowed packages, group, file permissions
EXPECTED_SGID = {
    "/usr/bin/expiry": (
        {"passwd"}, "shadow", 0o2755
    ),
    "/usr/bin/chage": (
        {"passwd"}, "shadow", 0o2755
    ),
    "/usr/bin/ssh-agent": (
        {"openssh-client"}, "_ssh", 0o2755
    ),
    "/usr/bin/plocate": (
        {"plocate"}, "plocate", 0o2755
    ),
    "/usr/bin/crontab": (
        {"cron", "cronie", "systemd-cron"},
        "crontab", 0o2755
    ),
}


def get_package_name(path):
    """Identify the Debian package owning a file."""
    try:
        result = subprocess.run(
            ["dpkg-query", "-S", path],
            capture_output=True,
            text=True,
            timeout=3,
            check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if result.returncode != 0:
        return None

    for line in result.stdout.splitlines():
        package, separator, file_path = line.rpartition(": ")

        if separator and file_path == path:
            return package.split(":")[0].split(",")[0].strip()

    return None


def is_dangerous(name):
    """Check whether a program is a potential SUID risk."""
    if name in DANGEROUS_BINARIES:
        return True

    if re.fullmatch(r"python(?:\d+(?:\.\d+)?)?", name):
        return True

    return name.startswith("vim.")


def has_unsafe_write_permissions(path):
    """Detect privileged binaries writable by group or others."""
    try:
        info = os.lstat(path)

        return bool(
            info.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
        )
    except OSError:
        return False


def is_expected_privileged_binary(path, category):
    """Verify package, owner, group and permissions."""

    try:
        info = os.lstat(path)

        if not stat.S_ISREG(info.st_mode):
            return False

        mode = stat.S_IMODE(info.st_mode)
        group = grp.getgrgid(info.st_gid).gr_name

    except (OSError, KeyError):
        return False

    # Expected privileged files must be root-owned.
    if info.st_uid != 0:
        return False

    package = get_package_name(path)

    if package is None:
        return False

    # Standard SGID utilities
    if (
        path in EXPECTED_SGID
        and "sgid" in category
        and "suid" not in category
    ):
        packages, expected_group, expected_mode = (
            EXPECTED_SGID[path]
        )

        return (
            package in packages
            and group == expected_group
            and mode == expected_mode
        )

    # Kismet capture helpers
    if (
        path.startswith("/usr/bin/kismet_cap_")
        and "suid" in category
        and "sgid" not in category
    ):
        return (
            package.startswith("kismet-capture-")
            and group == "kismet"
            and mode == 0o4754
        )

    return False


def assess_risks(findings):
    """
    Input: List of security findings.

    Output: Original findings with:
        risk
        reason
        recommendation
    """

    assessed = []

    for finding in findings:

        category = str(
            finding.get("category", "")
        ).lower()

        item = str(finding.get("item", ""))
        path = item.strip()
        name = os.path.basename(path).lower()

        risk = "Medium"
        reason = "This finding requires manual verification."
        recommendation = (
            "Review ownership, permissions and intended use."
        )

        # ==================================
        # SUID / SGID RISK CLASSIFICATION
        # ==================================
        if "suid" in category or "sgid" in category:

            if has_unsafe_write_permissions(path):
                risk = "High"
                reason = (
                    "This privileged executable is writable "
                    "by its group or other users."
                )
                recommendation = (
                    "Investigate file ownership and remove "
                    "unauthorized write permissions."
                )

            elif "suid" in category and is_dangerous(name):
                risk = "High"
                reason = (
                    f"SUID-enabled {name} may allow "
                    "privileged command execution."
                )
                recommendation = (
                    "Review whether SUID is necessary and "
                    "remove unnecessary privileged permissions."
                )

            elif is_expected_privileged_binary(path, category):
                risk = "Low"
                reason = (
                    "Package, owner, group and permissions "
                    "match a known privileged utility configuration."
                )
                recommendation = (
                    "Keep the package updated and regularly "
                    "verify permissions and group access."
                )

            elif name in {
                "ntfs-3g",
                "rsh-redone-rsh",
                "rsh-redone-rlogin"
            }:
                risk = "Medium"
                reason = (
                    f"{name} uses elevated permissions and "
                    "requires further security review."
                )
                recommendation = (
                    "Confirm the package is required, "
                    "patched and appropriately restricted."
                )

            else:
                risk = "Medium"
                reason = (
                    "Privileged binary is unrecognized or its "
                    "expected permissions could not be verified."
                )
                recommendation = (
                    "Inspect owner, group, mode, package "
                    "origin and security updates."
                )

        # ==================================
        # SUDO RISK CLASSIFICATION
        # ==================================
        elif "sudo" in category:

            upper_item = item.upper()

            if item == "/etc/sudoers":
                risk = "Medium"
                reason = (
                    "The sudoers file can be read "
                    "by a non-root user."
                )
                recommendation = (
                    "Review file ownership and permissions."
                )

            elif (
                "NOPASSWD" in upper_item
                and re.search(
                    r"NOPASSWD\s*:\s*ALL\b", upper_item
                )
            ):
                risk = "High"
                reason = (
                    "A sudo rule permits passwordless "
                    "execution of any command."
                )
                recommendation = (
                    "Restrict passwordless sudo to "
                    "approved commands only."
                )

            elif "NOPASSWD" in upper_item:
                risk = "Medium"
                reason = (
                    "A sudo rule permits passwordless "
                    "execution of selected commands."
                )
                recommendation = (
                    "Review permitted commands and "
                    "apply least privilege."
                )

            else:
                risk = "Medium"
                reason = (
                    "A potentially privileged sudo "
                    "rule was detected."
                )
                recommendation = (
                    "Review allowed users and commands."
                )

        # ==================================
        # CRON RISK CLASSIFICATION
        # ==================================
        elif "cron" in category:

            risk = "Medium"
            reason = (
                "The scanner reported a writable "
                "scheduled-task file."
            )
            recommendation = (
                "Check which account runs the task "
                "and restrict write access."
            )

        # ==================================
        # LINUX CAPABILITIES
        # ==================================
        elif "capabilit" in category:

            risk = "Medium"
            reason = (
                "A privileged Linux capability was detected. "
                "Its impact depends on the binary and capability."
            )
            recommendation = (
                "Review whether the assigned capability "
                "is necessary."
            )

        # Preserve the original finding fields
        updated = dict(finding)

        updated.update({
            "risk": risk,
            "reason": reason,
            "recommendation": recommendation
        })

        assessed.append(updated)

    return assessed
