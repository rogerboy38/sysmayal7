"""
Frappe Hooks for Sysmayal App

This file contains all the hooks and configuration for integrating
the Sysmayal app with the Frappe framework.
from . import __version__ as app_version
"""


# module_name = "sysmayal_module"
app_name = "sysmayal"
app_title = "sysmayal"
app_publisher = "Sysmayal Development Team"
app_description = "Global Distribution & R&D Management for Aloe Vera Products"
app_icon = "octicon octicon-globe"
app_color = "green"
app_email = "dev@sysmayal.com"
app_license = "MIT"

# Required Frappe apps for V15 compatibility
required_apps = ["frappe", "erpnext"]

# Minimum required versions for compatibility
min_frappe_version = "15.0.0"
min_erpnext_version = "15.0.0"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sysmayal/css/sysmayal.css"
# app_include_js = "/assets/sysmayal/js/sysmayal.js"

# include js, css files in header of web template
# web_include_css = "/assets/sysmayal/css/sysmayal.css"
# web_include_js = "/assets/sysmayal/js/sysmayal.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sysmayal/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "sysmayal.install.before_install"
after_install = "sysmayal.setup.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sysmayal.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sysmayal.tasks.all"
# 	],
# 	"daily": [
# 		"sysmayal.tasks.daily"
# 	],
# 	"hourly": [
# 		"sysmayal.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sysmayal.tasks.weekly"
# 	]
# 	"monthly": [
# 		"sysmayal.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "sysmayal.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sysmayal.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sysmayal.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "Distribution Contact",
        "filter_by": "email",
        "redact_fields": ["first_name", "last_name", "phone", "mobile_no"],
        "rename": None,
        "partial": True,
    },
    {
        "doctype": "Distribution Organization", 
        "filter_by": "email_id",
        "redact_fields": ["organization_name", "phone", "contact_person"],
        "rename": None,
        "partial": True,
    },
    {
        "doctype": "Product Compliance",
        "filter_by": "contact_email",
        "redact_fields": ["responsible_person"],
        "rename": None,
        "partial": True,
    },
    {
        "doctype": "Certification Document",
        "filter_by": "contact_email",
        "redact_fields": ["primary_contact", "secondary_contact", "auditor_name", "auditor_email"],
        "rename": None,
        "partial": True,
    },
    # Note: Redaction for linked fields (like users/organizations) in Market Entry Plan might require custom handling.
     {
        "doctype": "Market Entry Plan",
        "filter_by": "project_manager", 
        "redact_fields": ["market_lead", "regulatory_lead", "local_partner"], 
        "rename": None,
        "partial": True,
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sysmayal_module.auth.validate"
# ]

# Translation
# --------------------------------

# Make property setters available in the translation file
# include_in_translator_file = ["doctype", "page", "report", "dashboard", "portal_menu"]


# Website routing
# ---------------

# website_route_rules = [
# 	{"from_route": "/sysmayal/<path:app_path>", "to_route": "sysmayal"},
# ]

# Fixtures
# --------
# Provide initial data to be loaded during installation

fixtures = [
    {
        "dt": "Country Regulation", 
        "filters": [
            ["docstatus", "<", 2]
        ]
    },
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", [
                "Customer-territory_manager",
                "Customer-regulatory_status",
                "Supplier-compliance_status",
                "Contact-regulatory_role"
            ]]
        ]
    },
    {
        "dt": "Property Setter",
        "filters": [
            ["doc_type", "in", ["Customer", "Supplier", "Contact"]]
        ]
    },
    {
        "dt": "Workflow",
        "filters": [
            ["name", "in", [
                "R&D Project Approval",
                "Product Compliance Review", 
                "Market Entry Plan Approval"
            ]]
        ]
    },
    {
        "dt": "Workflow State",
        "filters": [
            ["workflow_name", "in", [
                "R&D Project Approval",
                "Product Compliance Review",
                "Market Entry Plan Approval"
            ]]
        ]
    },
    {
        "dt": "Workflow Action Master",
        "filters": [
            ["workflow_name", "in", [
                "R&D Project Approval",
                "Product Compliance Review",
                "Market Entry Plan Approval"
            ]]
        ]
    }
]

# Configuration for Module Def
# -----------------------------
# restrict modules based on user permissions

# has_website_permission = {
# 	"Sales Order": "sysmayal.permissions.has_website_permission"
# }

# DocType specific
# ----------------

# Scheduled tasks for compliance monitoring
scheduler_events = {
    "daily": [
        "sysmayal_module.tasks.check_certification_expiry",
        "sysmayal_module.tasks.update_compliance_status"
    ],
    "weekly": [
        "sysmayal_module.tasks.generate_compliance_reports"
    ],
    "monthly": [
        "sysmayal_module.tasks.archive_old_documents"
    ]
}

# Email integration
# -----------------

# standard_email_footer = """<div style="padding: 7px; text-align: right; color: #888"><small>Sent via Sysmayal</small></div>"""

# Error notifications
# -------------------
# Send error notifications to administrators for critical issues

# on_session_creation = [
# 	"sysmayal.utils.clear_notifications"
# ]

# Boot session
# ------------
# Provide session data for client-side operations

# boot_session = "sysmayal.boot.boot_session"
