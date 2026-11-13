import os
import stat

STANDARD_SUID_ALLOWLIST = {
    "/usr/bin/passwd", "/usr/bin/sudo", "/usr/bin/su",
    "/usr/bin/chsh", "/usr/bin/chfn", "/usr/bin/newgrp",
    "/usr/bin/gpasswd", "/usr/bin/mount", "/usr/bin/umount",
    "/usr/bin/fusermount", "/usr/bin/fusermount3", "/usr/bin/pkexec"
}


def check_suid(target_paths=None):
    """Scan scoped directories for non-standard SUID and SGID binaries."""
    if target_paths is None:
        target_paths = ["/usr/bin", "/usr/local/bin"]

    findings = []

    for base_path in target_paths:
        if not os.path.exists(base_path):
            continue

        for root, _, files in os.walk(base_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    file_stat = os.lstat(filepath)
                    if not stat.S_ISREG(file_stat.st_mode):
                        continue

                    is_suid = bool(file_stat.st_mode & stat.S_ISUID)
                    is_sgid = bool(file_stat.st_mode & stat.S_ISGID)

                    if (is_suid or is_sgid) and filepath not in STANDARD_SUID_ALLOWLIST:
                        perm_type = "SUID & SGID" if (is_suid and is_sgid) else ("SUID" if is_suid else "SGID")
                        findings.append({
                            "category": f"{perm_type} Binary",
                            "item": filepath,
                            "details": f"Non-standard {perm_type} bit set (permissions: {oct(file_stat.st_mode)[-4:]}).",
                            "raw_identifier": filename
                        })
                except (PermissionError, FileNotFoundError):
                    continue

    return findings
