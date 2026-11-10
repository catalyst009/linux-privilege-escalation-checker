import argparse
import platform


def build_parser():
    parser = argparse.ArgumentParser(
        description="Linux Privilege Escalation Checker (authorized audits only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 main.py                      (interactive menu)
  python3 main.py --scan all
  python3 main.py --scan sudo --format json
  python3 main.py --scan suid --dry-run
  python3 main.py --scan all --output reports/""",
    )
    parser.add_argument("--scan", choices=["all", "sudo", "suid", "cron"], default=None,
                        help="run a scan directly (omit for the interactive menu)")
    parser.add_argument("--target", default="localhost",
                        help="hostname you are authorized to audit (default: localhost)")
    parser.add_argument("--format", choices=["txt", "json"], default="txt")
    parser.add_argument("--output", default="output",
                        help="report directory (default: output/)")
    parser.add_argument("--dry-run", action="store_true",
                        help="show what would run, scan nothing")
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


def display_menu():
    print("\n========== MAIN MENU ==========")
    print("1. System Information")
    print("2. Sudo Permission Check")
    print("3. SUID/SGID File Detection")
    print("4. Cron Job Permission Check")
    print("5. Generate Security Report")
    print("6. Exit")
    print("===============================")


def main(args):
    if platform.system() != "Linux":
        print("Error: This tool only supports Linux systems.")
        return

    if not confirm_authorization():
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