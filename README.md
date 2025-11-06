# Lost-Found
A fast, terminal-based Lost &amp; Found Management System built in Python — featuring dual portals, smart search, automated matching, analytics, and PDF reporting. Clean, scalable, and designed to bring order to chaos in campus item tracking.

A comprehensive, interactive command-line Lost & Found management system developed for VIT by Team Titans. The portal allows users to report, search, retrieve, and claim lost and found items with strong admin capabilities for data and claim management.

Features
Client Portal:

Registration and login for users.

Report lost or found items, with intuitive questionnaire.

Search for items by name, category, or color.

Claim found items and monitor claim status.

View personal item reporting history.

Admin Dashboard:

Secure admin login.

View and manage all lost/found reports and registered clients.

Process and update claims with approval workflows.

Smart matching of lost and found items (by keywords, color, location, dates, etc.).

Generate analytics (charts for statistics) and summary PDF reports.

Persistent data storage via CSV files.

Reports/Analytics:

Exportable analytics via matplotlib (bar, line, and pie charts).

Professional PDF reports of summary statistics.

Installation
Requirements
Install the following Python libraries before running the portal:

text
pip install pandas numpy matplotlib reportlab
Required Libraries
Library	Purpose
pandas	Data loading/saving and analytics
numpy	Numeric and array operations
matplotlib	Analytics visualizations
reportlab	Generating PDF summary reports
The portal also relies on Python’s built-in csv, os, hashlib, and datetime modules (these are standard with Python).

Environment
Python 3.7 or above recommended.

Runs on Windows, macOS, and Linux (uses os.system('cls' or 'clear') for terminal cleaning).

Run the main script:

text
python test_3.py
At the first launch: The program will create/load four CSV files:

lostitems.csv

founditems.csv

clients.csv

claims.csv
These will store persistent data for all features.

Basic Operation Flow
Users/clients first register, then log in to access reporting and search.

Admin logs in using pre-set credentials (see below) for full database and claim control.

Admin Credentials (default)
Username: admin, Password: admin123

Username: superadmin, Password: pass123

Change these in the code for better security before deploying!​

Functional Overview
Data Structures
Data are loaded from/saved to CSVs (lostitems.csv, founditems.csv, etc.).

Each item and client is stored as a record with unique IDs, with auto-incrementing counters for each type.

Passwords are hashed with SHA256 for security.

Menu Navigation
Main menu offers options for admin login, client portal, and exit.

Clients can report lost/found items, search, claim, and check claim status.

Admins can view reported items, user registry, manage and approve/reject claims, close cases, use smart matching/search/analytics, and generate a PDF report.

Generating Reports
On demand, admins can generate a summary PDF report of platform statistics (reportlab required).

Analytics (charts) are displayed on screen using matplotlib upon request.

Notes
Do not delete the CSV files unless you wish to clear all platform history.

All prompt input is expected in the terminal; no web/UI is included.

The code is partitioned for modularity, with separate functions for each feature and well-labeled sections.

Contributors: Samarth Agrawal, Arush Agrawal, Tanmay Khare, Parth Vats

