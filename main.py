import argparse
import importlib
import platform
import socket

# Member 3 - Risk Assessment Module
from risk_assessment import assess_risks

# Member 4 - Report Generation
from report_generator import generate_report
from scanner import get_system_info


CHECKS = {
    "sudo": ("sudo_checker", "check_sudo"),
    "suid": ("suid_checker", "check_suid"),
    "cron": ("cron_checker", "check_cron"),
}


def build_parser():
    parser = argparse.ArgumentParser(
        description="Linux Privilege Escalation Checker (authorized audits only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 main.py
  python3 main.py --scan all
  python3 main.py --scan sudo --format json
  python3 main.py --scan suid --dry-run
  python3 main.py --scan all --output reports/""",
    )

    parser.add_argument(
        "--scan",
        choices=["all", "sudo", "suid", "cron"],
        default=None,
        help="run a scan directly (omit for interactive menu)"
    )

    parser.add_argument(
        "--target",
        default="localhost",
        help="hostname you are authorized to audit (default: localhost)"
    )

    parser.add_argument(
        "--format",
        choices=["txt", "json"],
        default="txt"
    )

    parser.add_argument(
        "--output",
        default="output",
        help="report directory (default: output/)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would run, scan nothing"
    )

    return parser


def display_disclaimer():
    print("\n" + "=" * 55)
    print("       LINUX PRIVILEGE ESCALATION CHECKER")
    print("=" * 55)

    print("\nLEGAL DISCLAIMER")
    print("This tool is for educational and authorized")
    print("security auditing purposes only.")
    print("Unauthorized access may violate the")
    print("Computer Crimes Act 1997 (Malaysia).")

    print("\nRULES OF ENGAGEMENT")
    print("- Only scan systems you own or have permission to test.")
    print("- This tool performs security checks only.")
    print("- No exploitation or unauthorized access.")
    print("- Default scope: Local Linux system only.")
    print("- Press Ctrl+C to stop the program.")

    print("=" * 55)


def confirm_authorization():
    display_disclaimer()

    confirmation = input(
        "\nDo you have authorization to scan this system? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("\nAuthorization not confirmed. Exiting...")
        return False

    print("\nAuthorization confirmed.")
    return True


def confirm_scope(target):
    allowed = ["localhost", "127.0.0.1", socket.gethostname()]

    if target not in allowed:
        print(f"\nError: '{target}' is out of scope.")
        print("This tool only audits the local machine.")
        return False

    print(f"\nTarget scope : {target}")
    print(f"This machine : {socket.gethostname()}")

    typed = input("Re-type the target to confirm: ").strip()

    if typed != target:
        print("\nScope mismatch. Exiting...")
        return False

    print("\nScope confirmed.")
    return True


def display_menu():
    print("\n========== MAIN MENU ==========")
    print("1. System Information")
    print("2. Sudo Permission Check")
    print("3. SUID/SGID File Detection")
    print("4. Cron Job Permission Check")
    print("5. Generate Security Report")
    print("6. Exit")
    print("===============================")


def call_checker(module_name, func_name):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, func_name)()

    except (ImportError, AttributeError):
        print(f"[!] {module_name}.{func_name} not available yet - skipping")
        return []


def run_scan(args):
    names = list(CHECKS) if args.scan == "all" else [args.scan]
    findings = []

    # 1. Dry-run mode
    if args.dry_run:
        print("[DRY RUN] The following checks would run:")

        for name in names:
            print(f"  - {name}")

        print("Dry run - nothing was scanned.")
        return findings

    # 2. Run security checkers
    print("\n========== SCANNING ==========")

    for name in names:
        result = call_checker(*CHECKS[name])

        findings += result

        print(f"{name}: {len(result)} finding(s)")

    # 3. Member 3 - Risk Assessment
    assessed_findings = assess_risks(findings)

    print("\n========== RISK ASSESSMENT ==========")

    if not assessed_findings:
        print("No findings to assess.")

    for index, finding in enumerate(assessed_findings, 1):
        print(f"\nFinding {index}")
        print(f"Category: {finding.get('category', 'Unknown')}")
        print(f"Item: {finding.get('item', 'Unknown')}")
        print(f"Risk Level: {finding['risk']}")
        print(f"Reason: {finding['reason']}")
        print(f"Recommendation: {finding['recommendation']}")
        print("-" * 45)

    # 4. Risk Summary
    high = sum(1 for f in assessed_findings if f["risk"] == "High")
    medium = sum(1 for f in assessed_findings if f["risk"] == "Medium")
    low = sum(1 for f in assessed_findings if f["risk"] == "Low")

    print("\n========== RISK SUMMARY ==========")
    print(f"Total Findings : {len(assessed_findings)}")
    print(f"High Risk      : {high}")
    print(f"Medium Risk    : {medium}")
    print(f"Low Risk       : {low}")
    print("==================================")

    # 5. Member 4 - Report Generation
    try:
        report_path = generate_report(
            get_system_info(), assessed_findings, args.output, args.format
        )
        print(f"\nReport saved to: {report_path}")
    except (OSError, ValueError) as error:
        print(f"[!] Could not save report: {error}")

    return assessed_findings


def main(args):
    if platform.system() != "Linux":
        print("Error: This tool only supports Linux systems.")
        return

    if not confirm_authorization():
        return

    if not confirm_scope(args.target):
        return

    if args.scan:
        run_scan(args)
        return

    while True:
        display_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            print("System Information - Coming Soon")

        elif choice == "2":
            print("Sudo Permission Check - Coming Soon")

        elif choice == "3":
            print("SUID/SGID Detection - Coming Soon")

        elif choice == "4":
            print("Cron Job Check - Coming Soon")

        elif choice == "5":
            print("Report Generation - Coming Soon")

        elif choice == "6":
            print("\nExiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    args = build_parser().parse_args()

    try:
        main(args)

    except KeyboardInterrupt:
        print("\n\nEmergency stop activated. Program terminated.")