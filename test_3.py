"""
========================================
SMART LOST & FOUND PORTAL for VIT
========================================
Developed By (Team Titans)
"""

import pandas as pd
import numpy as np
import csv
import datetime
from datetime import datetime as dt
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
import hashlib

# ==================== GLOBAL DATA STRUCTURES ====================
lost_items = []
found_items = []
claims = []
admins = {"admin": "admin123", "superadmin": "pass123", "Samarth": "Samarth02"}
clients = []  # List of registered clients {username, password_hash, name, contact, email}

# Counters for unique IDs
lost_id_counter = 1
found_id_counter = 1
claim_id_counter = 1
client_id_counter = 1

# Session management
current_client = None  # Stores logged-in client info

# ==================== HELPER FUNCTIONS ====================

def clear_screen():
    """Clear terminal screen for better UX"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print attractive header"""
    print("\n" + "=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60 + "\n")

def print_divider():
    """Print divider line"""
    print("-" * 60)

def pause():
    """Pause for user to read"""
    input("\nPress Enter to continue...")

def get_current_date():
    """Return current date as string"""
    return dt.now().strftime("%Y-%m-%d")

def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    try:
        dt.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

# The lines of code below are drafted by Samarth Agrawal

# ==================== ITEM QUESTIONNAIRE FUNCTION ====================

def get_item_questionnaire(item_type="lost"):
    """
    Standard questionnaire for item reporting
    Returns structured dictionary with all item details
    """
    print_header(f"ITEM DETAILS QUESTIONNAIRE ({item_type.upper()})")
    
    print("Please provide the following information about the item:\n")
    
    item_details = {}
    
    # 1. Item Name
    item_details['item_name'] = input("1. Item Name (e.g., iPhone 13, Blue Backpack): ").strip()
    
    # 2. Category
    print("\n2. Category:")
    print("   a) Electronics   b) Clothing   c) Documents")
    print("   d) Books         e) Accessories f) Others")
    category_choice = input("   Select (a-f): ").strip().lower()
    category_map = {
        'a': 'Electronics', 'b': 'Clothing', 'c': 'Documents',
        'd': 'Books', 'e': 'Accessories', 'f': 'Others'
    }
    item_details['category'] = category_map.get(category_choice, 'Others')
    
    # 3. Color
    item_details['color'] = input("\n3. Color (e.g., Black, Blue, Red): ").strip()
    
    # 4. Material
    item_details['material'] = input("\n4. Material (e.g., Leather, Plastic, Metal): ").strip()
    
    # 5. Batch/ID Number
    batch_id = input("\n5. Batch/ID/Serial Number (if any, press Enter to skip): ").strip()
    item_details['batch_id'] = batch_id if batch_id else "N/A"
    
    # 6. Additional Notes
    notes = input("\n6. Additional Notes (optional, press Enter to skip): ").strip()
    item_details['additional_notes'] = notes if notes else "N/A"
    
    # Create comprehensive description from all fields
    description = f"Category: {item_details['category']}, Color: {item_details['color']}, "
    description += f"Material: {item_details['material']}, Batch/ID: {item_details['batch_id']}"
    if item_details['additional_notes'] != "N/A":
        description += f", Notes: {item_details['additional_notes']}"
    
    item_details['description'] = description
    
    print("\n✓ Item details recorded successfully!")
    
    return item_details

# ==================== DATA PERSISTENCE ====================

def load_data():
    """Load data from CSV files if they exist"""
    global lost_items, found_items, claims, clients
    global lost_id_counter, found_id_counter, claim_id_counter, client_id_counter
    
    try:
        # Load lost items
        if os.path.exists("lost_items.csv"):
            df = pd.read_csv("lost_items.csv")
            lost_items = df.to_dict('records')
            if lost_items:
                lost_id_counter = max([item['id'] for item in lost_items]) + 1
        
        # Load found items
        if os.path.exists("found_items.csv"):
            df = pd.read_csv("found_items.csv")
            found_items = df.to_dict('records')
            if found_items:
                found_id_counter = max([item['id'] for item in found_items]) + 1
        
        # Load claims
        if os.path.exists("claims.csv"):
            df = pd.read_csv("claims.csv")
            claims = df.to_dict('records')
            if claims:
                claim_id_counter = max([claim['claim_id'] for claim in claims]) + 1
        
        # Load clients
        if os.path.exists("clients.csv"):
            df = pd.read_csv("clients.csv")
            clients = df.to_dict('records')
            if clients:
                client_id_counter = max([client['client_id'] for client in clients]) + 1
                
        print("✓ Data loaded successfully from CSV files!")
    except Exception as e:
        print(f"⚠ Note: Could not load previous data. Starting fresh. ({e})")

def save_data():
    """Save all data to CSV files"""
    try:
        # Save lost items
        if lost_items:
            df_lost = pd.DataFrame(lost_items)
            df_lost.to_csv("lost_items.csv", index=False)
        
        # Save found items
        if found_items:
            df_found = pd.DataFrame(found_items)
            df_found.to_csv("found_items.csv", index=False)
        
        # Save claims
        if claims:
            df_claims = pd.DataFrame(claims)
            df_claims.to_csv("claims.csv", index=False)
        
        # Save clients
        if clients:
            df_clients = pd.DataFrame(clients)
            df_clients.to_csv("clients.csv", index=False)
        
        print("✓ All data saved successfully to CSV files!")
        return True
    except Exception as e:
        print(f"✗ Error saving data: {e}")
        return False




    
# The lines of code below are drafted by Tanmay Khare
# ==================== CLIENT AUTHENTICATION ====================

def client_register():
    """Register a new client"""
    global client_id_counter
    
    print_header("CLIENT REGISTRATION")
    
    print("Create your account to access the Lost & Found Portal\n")
    
    username = input("Choose Username: ").strip()
    
    # Check if username already exists
    for client in clients:
        if client['username'].lower() == username.lower():
            print("\n✗ Username already exists! Please choose a different one.")
            pause()
            return False
    
    password = input("Choose Password: ").strip()
    confirm_password = input("Confirm Password: ").strip()
    
    if password != confirm_password:
        print("\n✗ Passwords do not match!")
        pause()
        return False
    
    if len(password) < 4:
        print("\n✗ Password must be at least 4 characters long!")
        pause()
        return False
    
    name = input("Full Name: ").strip()
    contact = input("Contact Number: ").strip()
    email = input("Email Address: ").strip()
    
    # Create new client record
    new_client = {
        'client_id': client_id_counter,
        'username': username,
        'password_hash': hash_password(password),
        'name': name,
        'contact': contact,
        'email': email,
        'registration_date': get_current_date()
    }
    
    clients.append(new_client)
    client_id_counter += 1
    
    print(f"\n✓ Registration successful! Welcome, {name}!")
    print("You can now login with your credentials.")
    pause()
    return True

def client_login():
    """Client login verification"""
    global current_client
    
    print_header("CLIENT LOGIN")
    
    if not clients:
        print("⚠ No registered clients found.")
        print("Please register first to access the portal.\n")
        pause()
        return False
    
    attempts = 3
    while attempts > 0:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        for client in clients:
            if client['username'].lower() == username.lower():
                if verify_password(password, client['password_hash']):
                    current_client = client
                    print(f"\n✓ Login successful! Welcome back, {client['name']}!")
                    pause()
                    return True
        
        attempts -= 1
        if attempts > 0:
            print(f"\n✗ Invalid credentials! {attempts} attempt(s) remaining.\n")
        else:
            print("\n✗ Too many failed attempts. Returning to main menu.")
            pause()
            return False
    
    return False

def client_logout():
    """Logout current client"""
    global current_client
    current_client = None
    print("\n✓ Logged out successfully!")
    pause()

def require_client_login():
    """Check if client is logged in"""
    if current_client is None:
        print("\n⚠ You must be logged in to access this feature!")
        pause()
        return False
    return True



# The lines of code below are drafted by Samarth Agrawal
# ==================== ADMIN LOGIN ====================

def admin_login():
    """Admin login verification"""
    print_header("ADMIN LOGIN")
    
    attempts = 3
    while attempts > 0:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if username in admins and admins[username] == password:
            print(f"\n✓ Login successful! Welcome, {username}!")
            pause()
            return True
        else:
            attempts -= 1
            if attempts > 0:
                print(f"\n✗ Invalid credentials! {attempts} attempt(s) remaining.\n")
            else:
                print("\n✗ Too many failed attempts. Returning to main menu.")
                pause()
                return False
    
    return False

# ==================== SMART MATCHING ====================

def match_items():
    """Match lost and found items based on keywords, date, and location"""
    print_header("SMART ITEM MATCHING")
    
    if not lost_items or not found_items:
        print("⚠ Insufficient data for matching. Need both lost and found items.")
        pause()
        return
    
    matches = []
    
    for lost in lost_items:
        if lost['status'].lower() == 'closed':
            continue
            
        for found in found_items:
            if found['status'].lower() == 'claimed':
                continue
            
            score = 0
            reasons = []
            
            # Check item name similarity
            lost_keywords = set(lost['item_name'].lower().split())
            found_keywords = set(found['item_name'].lower().split())
            common_keywords = lost_keywords.intersection(found_keywords)
            
            if common_keywords:
                score += len(common_keywords) * 30
                reasons.append(f"Common keywords: {', '.join(common_keywords)}")
            
            # Check category
            if lost.get('category', '').lower() == found.get('category', '').lower():
                score += 25
                reasons.append("Same category")
            
            # Check color
            if lost.get('color', '').lower() == found.get('color', '').lower():
                score += 20
                reasons.append("Same color")
            
            # Check location similarity
            if lost['location'].lower() == found['location'].lower():
                score += 15
                reasons.append("Same location")
            
            # Check date proximity (within 7 days)
            try:
                lost_date = dt.strptime(lost['date_lost'], "%Y-%m-%d")
                found_date = dt.strptime(found['date_found'], "%Y-%m-%d")
                date_diff = abs((found_date - lost_date).days)
                
                if date_diff <= 7:
                    score += 15
                    reasons.append(f"Found within {date_diff} days")
            except:
                pass
            
            # If score is high enough, add to matches
            if score >= 40:
                matches.append({
                    'lost_id': lost['id'],
                    'found_id': found['id'],
                    'lost_item': lost['item_name'],
                    'found_item': found['item_name'],
                    'score': score,
                    'reasons': reasons
                })
    
    if matches:
        matches.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"Found {len(matches)} potential matches:\n")
        for i, match in enumerate(matches, 1):
            print(f"{i}. Match Score: {match['score']}%")
            print(f"   Lost Item #{match['lost_id']}: {match['lost_item']}")
            print(f"   Found Item #{match['found_id']}: {match['found_item']}")
            print(f"   Reasons: {'; '.join(match['reasons'])}")
            print_divider()
    else:
        print("No matches found based on current criteria.")
    
    pause()


# ==================== CHARTS & REPORTS ====================

def generate_charts(chart_type, title, data, labels=None):
    """Generate matplotlib charts"""
    try:
        plt.figure(figsize=(10, 6))
        
        if chart_type == 'bar':
            plt.bar(range(len(data)), data, color='skyblue', edgecolor='navy')
            if labels:
                plt.xticks(range(len(data)), labels, rotation=45, ha='right')
            plt.ylabel('Count')
            
        elif chart_type == 'pie':
            colors_pie = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
            plt.pie(data, labels=labels, autopct='%1.1f%%', colors=colors_pie, startangle=90)
            plt.axis('equal')
            
        elif chart_type == 'line':
            plt.plot(range(len(data)), data, marker='o', linestyle='-', linewidth=2, markersize=8, color='green')
            if labels:
                plt.xticks(range(len(data)), labels, rotation=45, ha='right')
            plt.ylabel('Count')
            plt.grid(True, alpha=0.3)
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"✗ Error generating chart: {e}")



        

# The lines of code below are drafted by Tanmay Khare
def generate_pdf_report():
    """Generate comprehensive PDF report"""
    print_header("GENERATE PDF REPORT")
    
    try:
        filename = f"lost_found_report_{dt.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2e5c8a'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        title = Paragraph("LOST & FOUND PORTAL - SUMMARY REPORT", title_style)
        elements.append(title)
        
        # Date
        date_text = Paragraph(f"<b>Generated:</b> {dt.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        elements.append(date_text)
        elements.append(Spacer(1, 20))
        
        # Summary Statistics
        elements.append(Paragraph("SUMMARY STATISTICS", heading_style))
        
        summary_data = [
            ['Metric', 'Count'],
            ['Total Lost Items', str(len(lost_items))],
            ['Total Found Items', str(len(found_items))],
            ['Total Registered Clients', str(len(clients))],
            ['Open Lost Cases', str(len([x for x in lost_items if x['status'].lower() == 'open']))],
            ['Closed Cases', str(len([x for x in lost_items if x['status'].lower() == 'closed']))],
            ['Pending Claims', str(len([x for x in claims if 'Submitted' in x['status']]))],
            ['Verified Claims', str(len([x for x in claims if 'Verified' in x['status']]))],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(elements)
        print(f"\n✓ PDF Report generated successfully: {filename}")
        
    except Exception as e:
        print(f"✗ Error generating PDF report: {e}")
    
    pause()



# ==================== CLIENT FUNCTIONS ====================

def client_report_lost():
    """Client reports a lost item"""
    global lost_id_counter
    
    if not require_client_login():
        return
    
    print_header("REPORT LOST ITEM")
    
    # Get item details using questionnaire
    item_details = get_item_questionnaire("lost")
    
    # Additional information
    print_divider()
    location = input("\nLocation Where Lost: ").strip()
    date_lost = input("Date Lost (YYYY-MM-DD) or press Enter for today: ").strip()
    
    if not date_lost:
        date_lost = get_current_date()
    elif not validate_date(date_lost):
        print("✗ Invalid date format! Using today's date.")
        date_lost = get_current_date()
    
    # Create lost item record
    item = {
        'id': lost_id_counter,
        'item_name': item_details['item_name'],
        'category': item_details['category'],
        'color': item_details['color'],
        'material': item_details['material'],
        'batch_id': item_details['batch_id'],
        'additional_notes': item_details['additional_notes'],
        'description': item_details['description'],
        'location': location,
        'date_lost': date_lost,
        'status': 'open',
        'reporter_username': current_client['username'],
        'reporter_name': current_client['name'],
        'reporter_contact': current_client['contact']
    }
    
    lost_items.append(item)
    lost_id_counter += 1
    
    print(f"\n✓ Lost item reported successfully! Reference ID: {item['id']}")
    print("You can check the status anytime from your client dashboard.")
    pause()

def client_report_found():
    """Client reports a found item"""
    global found_id_counter
    
    if not require_client_login():
        return
    
    print_header("REPORT FOUND ITEM")
    
    # Get item details using questionnaire
    item_details = get_item_questionnaire("found")
    
    # Additional information
    print_divider()
    location = input("\nLocation Where Found: ").strip()
    date_found = input("Date Found (YYYY-MM-DD) or press Enter for today: ").strip()
    
    if not date_found:
        date_found = get_current_date()
    elif not validate_date(date_found):
        print("✗ Invalid date format! Using today's date.")
        date_found = get_current_date()
    
    # Create found item record
    item = {
        'id': found_id_counter,
        'item_name': item_details['item_name'],
        'category': item_details['category'],
        'color': item_details['color'],
        'material': item_details['material'],
        'batch_id': item_details['batch_id'],
        'additional_notes': item_details['additional_notes'],
        'description': item_details['description'],
        'location': location,
        'date_found': date_found,
        'status': 'available',
        'finder_username': current_client['username'],
        'finder_name': current_client['name'],
        'finder_contact': current_client['contact']
    }
    
    found_items.append(item)
    found_id_counter += 1
    
    print(f"\n✓ Found item reported successfully! Reference ID: {item['id']}")
    print("Thank you for your honesty! The owner will be able to claim it.")
    pause()

def client_view_my_reports():
    """View client's own reported items"""
    if not require_client_login():
        return
    
    print_header("MY REPORTED ITEMS")
    
    username = current_client['username']
    
    # Filter lost items reported by this user
    my_lost = [item for item in lost_items if item.get('reporter_username') == username]
    
    # Filter found items reported by this user
    my_found = [item for item in found_items if item.get('finder_username') == username]
    
    print(f"Items reported by: {current_client['name']}\n")
    
    if my_lost:
        print("--- LOST ITEMS I REPORTED ---")
        for item in my_lost:
            print(f"ID: {item['id']} | {item['item_name']} | {item['category']}")
            print(f"   Location: {item['location']} | Date: {item['date_lost']} | Status: {item['status']}")
            print_divider()
    else:
        print("--- No lost items reported by you ---\n")
    
    if my_found:
        print("\n--- FOUND ITEMS I REPORTED ---")
        for item in my_found:
            print(f"ID: {item['id']} | {item['item_name']} | {item['category']}")
            print(f"   Location: {item['location']} | Date: {item['date_found']} | Status: {item['status']}")
            print_divider()
    else:
        print("--- No found items reported by you ---\n")
    
    pause()







# The lines of code below are drafted by Parth Vats
def client_search_items():
    """Search for items in the database"""
    if not require_client_login():
        return
    
    print_header("SEARCH ITEMS")
    
    print("1. Search by Name")
    print("2. Search by Category")
    print("3. Search by Color")
    print("4. View All Available Items")
    print("5. Back")
    
    choice = input("\nEnter choice: ").strip()
    
    if choice == '1':
        keyword = input("Enter item name keyword: ").strip().lower()
        
        print("\n--- LOST ITEMS ---")
        found_any = False
        for item in lost_items:
            if keyword in item['item_name'].lower() and item['status'].lower() == 'open':
                print(f"ID: {item['id']} | {item['item_name']}|")
                print(f"Date: {item['date_lost']}")
                print_divider()
                found_any = True
        
        print("\n--- FOUND ITEMS ---")
        for item in found_items:
            if keyword in item['item_name'].lower() and item['status'].lower() == 'available':
                print(f"ID: {item['id']} | {item['item_name']} |")
                print(f"Date: {item['date_found']}")
                print_divider()
                found_any = True
        
        if not found_any:
            print("No items found matching your search.")
    
    elif choice == '2':
        print("\nCategories: Electronics, Clothing, Documents, Books, Accessories, Others")
        category = input("Enter category: ").strip().lower()
        
        print("\n--- LOST ITEMS ---")
        found_any = False
        for item in lost_items:
            if item.get('category', '').lower() == category and item['status'].lower() == 'open':
                print(f"ID: {item['id']} | {item['item_name']}")
                print(f"Date: {item['date_lost']}")
                print_divider()
                found_any = True
        
        print("\n--- FOUND ITEMS ---")
        for item in found_items:
            if item.get('category', '').lower() == category and item['status'].lower() == 'available':
                print(f"ID: {item['id']} | {item['item_name']}")
                print(f"Date: {item['date_found']}")
                print_divider()
                found_any = True
        
        if not found_any:
            print("No items found in this category.")
    
    elif choice == '3':
        color = input("Enter color: ").strip().lower()
        
        print("\n--- FOUND ITEMS ---")
        found_any = False
        for item in found_items:
            if item.get('color', '').lower() == color and item['status'].lower() == 'available':
                print(f"ID: {item['id']} | {item['item_name']}")
                print(f"Date: {item['date_found']}")
                print_divider()
                found_any = True
        
        if not found_any:
            print("No items found with that color.")
    
    elif choice == '4':
        print("\n--- ALL AVAILABLE FOUND ITEMS ---")
        available = [item for item in found_items if item['status'].lower() == 'available']
        
        if available:
            for item in available:
                print(f"ID: {item['id']} | {item['item_name']}")
                print(f"Date: {item['date_found']}")
                print_divider()
        else:
            print("No available items at the moment.")
    
    pause()


def client_claim_item():
    """Client claims a found item"""
    global claim_id_counter
    
    if not require_client_login():
        return
    
    print_header("CLAIM AN ITEM")
    
    # Show available found items
    available_items = [item for item in found_items if item['status'].lower() == 'available']
    
    if not available_items:
        print("⚠ No items available for claiming at the moment.")
        pause()
        return
    
    print("Available Items:\n")
    for item in available_items:
        print(f"ID: {item['id']} | {item['item_name']} | {item['category']}")
        print(f"   Date Found: {item['date_found']}")
        print_divider()
    
    found_id = input("\nEnter Found Item ID you want to claim: ").strip()
    
    try:
        found_id = int(found_id)
        
        # Check if item exists and is available
        item_exists = False
        for item in found_items:
            if item['id'] == found_id and item['status'].lower() == 'available':
                item_exists = True
                break
        
        if not item_exists:
            print("\n✗ Item not found or not available!")
            pause()
            return
        
        # Get proof description
        print("\n--- OWNERSHIP VERIFICATION ---")
        proof = input("Describe unique features/details to prove ownership {Name,Category,Color,Material,Lost Place, Lost Date, Unique Identification}: ").strip()
        
        if len(proof) < 10:
            print("\n✗ Please provide more detailed information!")
            pause()
            return
        
        # Create claim
        claim = {
            'claim_id': claim_id_counter,
            'found_item_id': found_id,
            'claimant_username': current_client['username'],
            'claimant_name': current_client['name'],
            'claimant_contact': current_client['contact'],
            'claim_date': get_current_date(),
            'status': 'Claim Request Submitted',
            'proof_description': proof,
            'admin_notes': ''
        }
        
        claims.append(claim)
        claim_id_counter += 1
        
        print(f"\n✓ Claim submitted successfully! Claim ID: {claim['claim_id']}")
        print("Status: Claim Request Submitted")
        print("\nNext Steps:")
        print("- Admin will verify your claim")
        print("- You'll be notified of verification status")
        print("- If verified, collect from SWF Office")
        
    except ValueError:
        print("\n✗ Invalid ID format!")
    
    pause()

def client_check_claim_status():
    """Check status of claims made by logged-in client"""
    if not require_client_login():
        return
    
    print_header("MY CLAIM REQUESTS")
    
    # Filter claims by current user
    my_claims = [claim for claim in claims if claim.get('claimant_username') == current_client['username']]
    
    if not my_claims:
        print("You have not made any claim requests yet.")
        pause()
        return
    
    print(f"Claims by: {current_client['name']}\n")
    
    for claim in my_claims:
        print(f"Claim ID: {claim['claim_id']}")
        print(f"Item ID: {claim['found_item_id']}")
        print(f"Status: {claim['status']}")
        print(f"Claim Date: {claim['claim_date']}")
        
        # Status-specific messages
        if claim['status'] == 'Claim Request Submitted':
            print("   ⏳ Pending admin verification")
        elif claim['status'] == 'Claim Verified':
            print("   ✓ Verified! Please collect from SWF Office")
        elif claim['status'] == 'Collect From SWF Office':
            print("   ✓ Ready for collection at SWF Office")
        elif claim['status'] == 'Claimed':
            print("   ✓ Item successfully claimed and collected")
        elif claim['status'] == 'Claim Rejected':
            print("   ✗ Claim rejected by admin")
            if claim.get('admin_notes'):
                print(f"   Reason: {claim['admin_notes']}")
        elif claim['status'] == 'Not Verified':
            print("   ✗ Could not verify ownership")
            if claim.get('admin_notes'):
                print(f"   Reason: {claim['admin_notes']}")
        
        print_divider()
    
    pause()

# ==================== ADMIN FUNCTIONS ====================

def admin_view_all_lost():
    """View all lost items"""
    print_header("ALL LOST ITEMS")
    
    if not lost_items:
        print("No lost items in database.")
        pause()
        return
    
    for item in lost_items:
        print(f"ID: {item['id']} | {item['item_name']} | {item.get('category', 'N/A')}")
        print(f"   Color: {item.get('color', 'N/A')} | Material: {item.get('material', 'N/A')}")
        print(f"   Location: {item['location']} | Date: {item['date_lost']}")
        print(f"   Status: {item['status']} | Reporter: {item.get('reporter_name', 'N/A')}")
        print_divider()
    
    print(f"\nTotal Lost Items: {len(lost_items)}")
    pause()

def admin_view_all_found():
    """View all found items"""
    print_header("ALL FOUND ITEMS")
    
    if not found_items:
        print("No found items in database.")
        pause()
        return
    
    for item in found_items:
        print(f"ID: {item['id']} | {item['item_name']} | {item.get('category', 'N/A')}")
        print(f"   Color: {item.get('color', 'N/A')} | Material: {item.get('material', 'N/A')}")
        print(f"   Location: {item['location']} | Date: {item['date_found']}")
        print(f"   Status: {item['status']} | Finder: {item.get('finder_name', 'N/A')}")
        print_divider()
    
    print(f"\nTotal Found Items: {len(found_items)}")
    pause()







## The lines of code below are drafted by Arush Agrawal

def admin_view_clients():
    """View all registered clients"""
    print_header("REGISTERED CLIENTS")
    
    if not clients:
        print("No registered clients.")
        pause()
        return
    
    for client in clients:
        print(f"ID: {client['client_id']} | Username: {client['username']}")
        print(f"   Name: {client['name']} | Contact: {client['contact']}")
        print(f"   Email: {client['email']} | Registered: {client.get('registration_date', 'N/A')}")
        print_divider()
    
    print(f"\nTotal Registered Clients: {len(clients)}")
    pause()

def admin_manage_claims():
    """View and manage all claims with status workflow"""
    print_header("MANAGE CLAIMS")
    
    if not claims:
        print("No claims in database.")
        pause()
        return
    
    # Show all claims
    print("ALL CLAIMS:\n")
    for claim in claims:
        print(f"Claim ID: {claim['claim_id']} | Item ID: {claim['found_item_id']}")
        print(f"   Claimant: {claim['claimant_name']} | Contact: {claim['claimant_contact']}")
        print(f"   Status: {claim['status']} | Date: {claim['claim_date']}")
        print(f"   Proof: {claim.get('proof_description', 'N/A')}")
        print_divider()
    
    print("\nCLAIM MANAGEMENT OPTIONS:")
    print("1. Update Claim Status")
    print("2. Back")
    
    choice = input("\nEnter choice: ").strip()
    
    if choice == '1':
        claim_id = input("\nEnter Claim ID to update: ").strip()
        
        try:
            claim_id = int(claim_id)
            claim_found = False
            
            for claim in claims:
                if claim['claim_id'] == claim_id:
                    claim_found = True
                    
                    print(f"\nCurrent Status: {claim['status']}")
                    print("\nUpdate to:")
                    print("1. Claim Verified")
                    print("2. Not Verified")
                    print("3. Collect From SWF Office")
                    print("4. Claimed (Item Collected)")
                    print("5. Claim Rejected")
                    
                    status_choice = input("\nEnter choice (1-5): ").strip()
                    
                    status_map = {
                        '1': 'Claim Verified',
                        '2': 'Not Verified',
                        '3': 'Collect From SWF Office',
                        '4': 'Claimed',
                        '5': 'Claim Rejected'
                    }
                    
                    if status_choice in status_map:
                        old_status = claim['status']
                        claim['status'] = status_map[status_choice]
                        
                        # Get admin notes for rejections
                        if status_choice in ['2', '5']:
                            notes = input("Enter reason for rejection/not verified: ").strip()
                            claim['admin_notes'] = notes
                        
                        # Update found item status if claimed
                        if status_choice == '4':
                            for item in found_items:
                                if item['id'] == claim['found_item_id']:
                                    item['status'] = 'claimed'
                                    break
                        
                        print(f"\n✓ Claim #{claim_id} updated: {old_status} → {claim['status']}")
                    else:
                        print("\n✗ Invalid choice!")
                    
                    break
            
            if not claim_found:
                print(f"\n✗ Claim ID {claim_id} not found.")
        
        except ValueError:
            print("\n✗ Invalid Claim ID!")
    
    pause()

def admin_close_case():
    """Mark a lost item case as closed"""
    print_header("CLOSE LOST ITEM CASE")
    
    # Show open cases
    open_cases = [item for item in lost_items if item['status'].lower() == 'open']
    
    if not open_cases:
        print("No open cases to close.")
        pause()
        return
    
    print("Open Cases:\n")
    for item in open_cases:
        print(f"ID: {item['id']} | {item['item_name']} | {item.get('category', 'N/A')}")
        print(f"   Reporter: {item.get('reporter_name', 'N/A')} | Date: {item['date_lost']}")
        print_divider()
    
    item_id = input("\nEnter Lost Item ID to close: ").strip()
    
    try:
        item_id = int(item_id)
        for item in lost_items:
            if item['id'] == item_id:
                item['status'] = 'closed'
                print(f"\n✓ Case #{item_id} closed successfully!")
                pause()
                return
        
        print(f"\n✗ Item #{item_id} not found.")
    except ValueError:
        print("\n✗ Invalid ID format!")
    
    pause()

def admin_analytics():
    """Generate analytics and charts"""
    print_header("ANALYTICS & REPORTS")
    
    print("1. Items Lost Per Category")
    print("2. Items Found Per Category")
    print("3. Lost vs Found Comparison")
    print("4. Claim Status Distribution")
    print("5. Back")
    
    choice = input("\nEnter choice: ").strip()
    
    if choice == '1':
        if not lost_items:
            print("\n⚠ No lost items data available.")
            pause()
            return
        
        df = pd.DataFrame(lost_items)
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            print("\nItems Lost Per Category:")
            print(category_counts)
            
            generate_charts('bar', 'Items Lost Per Category', 
                          category_counts.values.tolist(), 
                          category_counts.index.tolist())
        else:
            print("\n⚠ Category information not available.")
    
    elif choice == '2':
        if not found_items:
            print("\n⚠ No found items data available.")
            pause()
            return
        
        df = pd.DataFrame(found_items)
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            print("\nItems Found Per Category:")
            print(category_counts)
            
            generate_charts('bar', 'Items Found Per Category', 
                          category_counts.values.tolist(), 
                          category_counts.index.tolist())
        else:
            print("\n⚠ Category information not available.")
    
    elif choice == '3':
        total_lost = len(lost_items)
        total_found = len(found_items)
        
        if total_lost == 0 and total_found == 0:
            print("\n⚠ No data available.")
            pause()
            return
        
        print(f"\nTotal Lost Items: {total_lost}")
        print(f"Total Found Items: {total_found}")
        
        generate_charts('pie', 'Lost vs Found Items Comparison', 
                      [total_lost, total_found], 
                      ['Lost Items', 'Found Items'])
    
    elif choice == '4':
        if not claims:
            print("\n⚠ No claims data available.")
            pause()
            return
        
        df = pd.DataFrame(claims)
        status_counts = df['status'].value_counts()
        
        print("\nClaim Status Distribution:")
        print(status_counts)
        
        generate_charts('pie', 'Claim Status Distribution', 
                      status_counts.values.tolist(), 
                      status_counts.index.tolist())
    
    pause()

def admin_dashboard():
    """Main admin dashboard"""
    while True:
        clear_screen()
        print_header("ADMIN DASHBOARD")
        
        print("1.  View All Lost Items")
        print("2.  View All Found Items")
        print("3.  View Registered Clients")
        print("4.  Manage Claims")
        print("5.  Close Lost Item Case")
        print("6.  Smart Item Matching")
        print("7.  Analytics & Charts")
        print("8.  Save All Data")
        print("9.  Generate PDF Report")
        print("10. Logout")
        
        choice = input("\nEnter choice (1-10): ").strip()
        
        if choice == '1':
            admin_view_all_lost()
        elif choice == '2':
            admin_view_all_found()
        elif choice == '3':
            admin_view_clients()
        elif choice == '4':
            admin_manage_claims()
        elif choice == '5':
            admin_close_case()
        elif choice == '6':
            match_items()
        elif choice == '7':
            admin_analytics()
        elif choice == '8':
            save_data()
            pause()
        elif choice == '9':
            generate_pdf_report()
        elif choice == '10':
            print("\n✓ Logged out successfully!")
            pause()
            break
        else:
            print("\n✗ Invalid choice! Please try again.")
            pause()

# ==================== CLIENT PORTAL ====================

def client_portal():
    """Main client portal"""
    global current_client
    
    while True:
        clear_screen()
        
        if current_client is None:
            # Not logged in - show login/register menu
            print_header("CLIENT PORTAL")
            
            print("1. Client Login")
            print("2. Client Registration")
            print("3. Back to Main Menu")
            
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == '1':
                if client_login():
                    continue  # Reload menu as logged in user
            elif choice == '2':
                client_register()
            elif choice == '3':
                break
            else:
                print("\n✗ Invalid choice!")
                pause()
        
        else:
            # Logged in - show client functions
            print_header(f"CLIENT PORTAL - Welcome, {current_client['name']}!")
            
            print("1. Report Lost Item")
            print("2. Report Found Item")
            print("3. My Reported Items")
            print("4. Search Items")
            print("5. Claim an Item")
            print("6. Check My Claim Status")
            print("7. Logout")
            
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == '1':
                client_report_lost()
            elif choice == '2':
                client_report_found()
            elif choice == '3':
                client_view_my_reports()
            elif choice == '4':
                client_search_items()
            elif choice == '5':
                client_claim_item()
            elif choice == '6':
                client_check_claim_status()
            elif choice == '7':
                client_logout()
            else:
                print("\n✗ Invalid choice!")
                pause()
# # The lines of code below are drafted by Samarth Agrawal
# ==================== MAIN PROGRAM ====================

def main():
    """Main program entry point"""
    # Load existing data
    load_data()
    
    while True:
        clear_screen()
        print_header("SMART LOST & FOUND PORTAL - VIT")
        
        print("Developed By: Team TITANS")
        print("Version 3.2\n")
        print_divider()
        
        print("\n1) Admin Login")
        print("2) Client Portal")
        print("3) Exit Program")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            if admin_login():
                admin_dashboard()
        elif choice == '2':
            client_portal()
        elif choice == '3':
            # Save data before exit
            print("\nSaving data...")
            save_data()
            print("\n" + "="*60)
            print("Thank you for using SMART LOST & FOUND PORTAL".center(60))
            print("Developed By Team TITANS - ©2025".center(60))
            print("="*60 + "\n")
            break
        else:
            print("\n✗ Invalid choice! Please try again.")
            pause()

# ==================== PROGRAM START ====================

if __name__ == "__main__":
    main()
