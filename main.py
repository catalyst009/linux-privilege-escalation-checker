
def display_menu():
    print("\n======================================")
    print("  LINUX PRIVILEGE ESCALATION CHECKER")
    print("======================================")
    print("1. System Information")
    print("2. Sudo Permission Check")
    print("3. SUID/SGID File Detection")
    print("4. Cron Job Permission Check")
    print("5. Generate Security Report")
    print("6. Exit")


def main():
    print("Welcome to Linux Privilege Escalation Checker")
    print("For authorized security auditing only.")

    while True:
        display_menu()
        choice = input("\nEnter your choice: ")

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
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
