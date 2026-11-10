# Linux Privilege Escalation Checker

## 1. Project Description
Linux Privilege Escalation Checker is a Python-based security auditing tool designed to identify potential privilege escalation misconfigurations in Linux systems.

The tool focuses on selected security checks and provides risk levels, explanations, and recommendations to help users understand and address potential security weaknesses.

## 2. Attack Category
**Category 4 – OS-Specific Attack**

## 3. Main Features
- System Information Gathering
- Sudo Permission Checking
- SUID/SGID File Detection
- Cron Job Permission Checking
- Risk Classification (Low, Medium, High)
- Security Recommendations
- TXT/JSON Report Generation

## 4. Attack Lifecycle Mapping
The tool supports the **Reconnaissance** stage by gathering Linux system information and identifying potential privilege escalation weaknesses.

## 5. Programming Language
Python

## 6. Target Operating System
- Kali Linux
- Ubuntu Linux

## 7. Project Status
Under Development

## 8. Ethical Considerations
- Only scan systems with proper authorization.
- Use read-only security checks.
- Do not execute exploits or attempt to gain unauthorized root access.
- Do not collect or store sensitive information unnecessarily.

## 9. Legal Disclaimer
This tool is developed for educational and authorized security auditing purposes only. Users must obtain explicit permission before conducting security assessments. Unauthorized access to computer systems may violate Malaysia's Computer Crimes Act 1997.

## 10. Limitations
The tool focuses on selected Linux privilege escalation misconfigurations. Its findings indicate potential risks and do not confirm that a vulnerability can be successfully exploited.
