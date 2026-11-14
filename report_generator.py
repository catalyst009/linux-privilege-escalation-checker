import json
import os
import socket
from datetime import datetime


def generate_report(system_info, findings, output_dir, fmt):
    fmt = fmt.lower()
    if fmt not in ("txt", "json"):
        raise ValueError("fmt must be 'txt' or 'json'")

    os.makedirs(output_dir, exist_ok=True)

    hostname = system_info.get("hostname") or socket.gethostname()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(output_dir, f"{hostname}_{timestamp}.{fmt}")

    if fmt == "json":
        write_json(path, system_info, findings)
    else:
        write_txt(path, system_info, findings)

    return path


def write_json(path, system_info, findings):
    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "system_info": system_info,
        "findings": findings,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def write_txt(path, system_info, findings):
    line = "=" * 60
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{line}\nLINUX PRIVILEGE ESCALATION REPORT\n{line}\n")
        f.write(f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")

        f.write("SYSTEM INFORMATION\n")
        for key, value in system_info.items():
            f.write(f"{key}: {value}\n")

        f.write(f"\nFINDINGS ({len(findings)})\n")
        for number, item in enumerate(findings, 1):
            f.write(f"\n[{number}] {item.get('check', 'Unknown')}\n")
            f.write(f"    Risk: {item.get('risk', 'N/A')}\n")
            f.write(f"    Details: {item.get('description', 'N/A')}\n")
            f.write(f"    Fix: {item.get('recommendation', 'N/A')}\n")
