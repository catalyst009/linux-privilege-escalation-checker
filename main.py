
import platform


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


def main():
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
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nEmergency stop activated. Program terminated.")
