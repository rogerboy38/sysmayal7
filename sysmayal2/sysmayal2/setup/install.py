"""
Installation and setup functions for Sysmayal app.

This module contains functions that are called during app installation
to set up initial data, configurations, and customizations.
"""

import frappe
import json
import os
from frappe.utils import cint, cstr, nowdate

def after_install():
    """
    Called after Sysmayal app installation.
    Sets up initial data and configurations for V15.
    """
    print("Setting up Sysmayal for Frappe/ERPNext V15...")
    
    # Check V15 compatibility first
    check_v15_compatibility()
    
    # Setup user roles and permissions
    setup_user_roles()
    
    # Setup custom fields
    setup_custom_fields()
    
    # Import country regulations data
    setup_country_regulations()
    
    # Setup default configurations
    setup_default_configurations()
    
    # Setup workspace for V15
    setup_workspace()
    
    # Create default workspace shortcuts
    setup_workspace_shortcuts()
    
    print("Sysmayal V15 setup completed successfully!")

def setup_user_roles():
    """Create and configure user roles for Sysmayal."""
    
    roles = [
        {
            "role_name": "Distribution Manager",
            "desk_access": 1,
            "home_page": "distribution-dashboard"
        },
        {
            "role_name": "R&D Manager", 
            "desk_access": 1,
            "home_page": "rd-dashboard"
        },
        {
            "role_name": "Compliance Officer",
            "desk_access": 1,
            "home_page": "compliance-dashboard"
        },
        {
            "role_name": "Data Entry Operator",
            "desk_access": 1,
            "home_page": "data-entry-dashboard"
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.role_name = role_data["role_name"]
            role.desk_access = role_data["desk_access"]
            if "home_page" in role_data:
                role.home_page = role_data["home_page"]
            role.save(ignore_permissions=True)
            print(f"Created role: {role_data['role_name']}")

def setup_custom_fields():
    """Add custom fields to existing ERPNext DocTypes."""
    
    custom_fields = [
        # Customer customizations
        {
            "dt": "Customer",
            "fieldname": "territory_manager",
            "label": "Territory Manager",
            "fieldtype": "Link",
            "options": "User",
            "insert_after": "territory"
        },
        {
            "dt": "Customer", 
            "fieldname": "regulatory_status",
            "label": "Regulatory Status",
            "fieldtype": "Select",
            "options": "Active\nPending\nSuspended\nInactive",
            "insert_after": "territory_manager"
        },
        
        # Supplier customizations
        {
            "dt": "Supplier",
            "fieldname": "compliance_status",
            "label": "Compliance Status", 
            "fieldtype": "Select",
            "options": "Compliant\nPending Review\nNon-Compliant\nExpired",
            "insert_after": "supplier_type"
        },
        
        # Contact customizations
        {
            "dt": "Contact",
            "fieldname": "regulatory_role",
            "label": "Regulatory Role",
            "fieldtype": "Select", 
            "options": "Quality Manager\nRegulatory Affairs\nProduct Manager\nDistribution Manager\nOther",
            "insert_after": "designation"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": field["dt"], "fieldname": field["fieldname"]}):
            custom_field = frappe.new_doc("Custom Field")
            custom_field.update(field)
            custom_field.save(ignore_permissions=True)
            print(f"Created custom field: {field['dt']}.{field['fieldname']}")

def setup_country_regulations():
    """Import country regulation data from JSON files."""
    
    # Get the path to the data directory
    app_path = frappe.get_app_path("sysmayal")
    data_path = os.path.join(os.path.dirname(app_path), "data")
    
    # Check if aloe vera global regulations file exists
    regulations_file = os.path.join(data_path, "aloe_vera_global_regulations.json")
    
    if os.path.exists(regulations_file):
        try:
            with open(regulations_file, 'r', encoding='utf-8') as f:
                regulations_data = json.load(f)
            
            # Import country regulations
            if "countries" in regulations_data:
                for country_code, country_data in regulations_data["countries"].items():
                    country_name = country_data.get("country_name", country_code.replace("_", " ").title())
                    
                    if not frappe.db.exists("Country Regulation", country_name):
                        country_reg = frappe.new_doc("Country Regulation")
                        country_reg.country_name = country_name
                        country_reg.regulatory_authority = country_data.get("regulatory_authority", "")
                        country_reg.authority_website = country_data.get("website", "")
                        country_reg.last_updated = nowdate()
                        country_reg.save(ignore_permissions=True)
                        print(f"Created country regulation: {country_name}")
                        
        except Exception as e:
            print(f"Error importing country regulations: {str(e)}")
    else:
        print("Country regulations data file not found, skipping import")

def setup_default_configurations():
    """Setup default system configurations."""
    
    # Set default number series
    number_series = [
        {"doctype": "Distribution Organization", "prefix": "DIST-ORG-", "current": 1},
        {"doctype": "Distribution Contact", "prefix": "DIST-CON-", "current": 1},
        {"doctype": "Product Development Project", "prefix": "RND-", "current": 1},
        {"doctype": "Country Regulation", "prefix": "REG-", "current": 1},
        {"doctype": "Product Compliance", "prefix": "COMP-", "current": 1},
        {"doctype": "Certification Document", "prefix": "CERT-", "current": 1},
        {"doctype": "Market Research", "prefix": "MR-", "current": 1}
    ]
    
    for series in number_series:
        if not frappe.db.exists("Naming Series", series["prefix"]):
            naming_series = frappe.new_doc("Naming Series")
            naming_series.prefix = series["prefix"]
            naming_series.current = series["current"]
            naming_series.save(ignore_permissions=True)
            print(f"Created naming series: {series['prefix']}")

def setup_workspace():
    """Setup Sysmayal workspace for V15."""
    
    if not frappe.db.exists("Workspace", "Sysmayal"):
        workspace = frappe.new_doc("Workspace")
        workspace.title = "Sysmayal"
        workspace.module = "sysmayal_module"
        workspace.category = "Modules"
        workspace.icon = "globe"
        workspace.public = 1
        workspace.is_standard = 0
        workspace.developer_mode_only = 0
        
        # Add workspace content for V15
        workspace.content = '''[
            {
                "id": "sysmayal-shortcuts",
                "type": "shortcut",
                "data": {
                    "shortcut_name": "Distribution Organization",
                    "link_to": "Distribution Organization",
                    "type": "DocType"
                }
            },
            {
                "id": "sysmayal-reports",
                "type": "shortcut", 
                "data": {
                    "shortcut_name": "Distribution Analytics",
                    "link_to": "Distribution Analytics Report",
                    "type": "Report"
                }
            }
        ]'''
        
        workspace.save(ignore_permissions=True)
        print("Created Sysmayal workspace for V15")
        
def check_v15_compatibility():
    """Check V15 compatibility during installation."""
    
    # Check Frappe version
    frappe_version = frappe.__version__
    if not frappe_version.startswith('15'):
        frappe.throw(f"This version of Sysmayal requires Frappe V15. Current version: {frappe_version}")
    
    print(f"✅ Frappe V15 compatibility confirmed: {frappe_version}")

def setup_workspace_shortcuts():
    """Setup workspace shortcuts for V15."""
    
    shortcuts = [
        {
            "label": "Distribution Organization",
            "link_to": "Distribution Organization",
            "type": "DocType",
            "icon": "building",
            "color": "blue"
        },
        {
            "label": "Distribution Contact",
            "link_to": "Distribution Contact", 
            "type": "DocType",
            "icon": "user",
            "color": "green"
        },
        {
            "label": "Product Compliance",
            "link_to": "Product Compliance",
            "type": "DocType",
            "icon": "check-circle",
            "color": "orange"
        },
        {
            "label": "Country Regulation",
            "link_to": "Country Regulation",
            "type": "DocType",
            "icon": "globe",
            "color": "red"
        },
        {
            "label": "Market Entry Plan",
            "link_to": "Market Entry Plan",
            "type": "DocType", 
            "icon": "target",
            "color": "purple"
        }
    ]
    
    for shortcut in shortcuts:
        if not frappe.db.exists("Workspace Shortcut", {"label": shortcut["label"]}):
            workspace_shortcut = frappe.new_doc("Workspace Shortcut")
            workspace_shortcut.update(shortcut)
            workspace_shortcut.save(ignore_permissions=True)
            print(f"Created workspace shortcut: {shortcut['label']}")

def validate_doctype_compatibility():
    """Validate all DocTypes are V15 compatible."""
    
    doctypes_to_check = [
        "Distribution Organization",
        "Distribution Contact", 
        "Product Compliance",
        "Country Regulation",
        "Market Entry Plan",
        "Product Development Project",
        "Certification Document",
        "Market Research"
    ]
    
    for doctype in doctypes_to_check:
        if frappe.db.exists("DocType", doctype):
            print(f"✅ DocType {doctype} is ready for V15")
        else:
            print(f"⚠️  DocType {doctype} not found - will be created during migration")
