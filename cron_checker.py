import os


def check_cron():
    """Check system cron files and directories for insecure write permissions."""
    findings = []
    cron_locations = [
        "/etc/crontab",
        "/etc/cron.d",
        "/etc/cron.daily",
        "/etc/cron.hourly",
        "/etc/cron.weekly",
        "/etc/cron.monthly"
    ]

    for location in cron_locations:
        if not os.path.exists(location):
            continue

        targets = [location] if os.path.isfile(location) else [
            os.path.join(location, f) for f in os.listdir(location)
        ]

        for target in targets:
            try:
                if os.path.isfile(target) and os.access(target, os.W_OK) and os.geteuid() != 0:
                    findings.append({
                        "category": "Cron Job Permissions",
                        "item": target,
                        "details": "Cron configuration or scheduled script is writable by the current user.",
                        "raw_identifier": target
                    })
            except (PermissionError, FileNotFoundError):
                continue

    return findings
