"""
Compliance Status Report

This report provides comprehensive overview of product compliance status
across different countries and regulatory frameworks.
"""

import frappe
from frappe import _
from frappe.utils import date_diff, nowdate

def execute(filters=None):
    """Execute the compliance status report."""
    
    columns = get_columns()
    data = get_data(filters)
    chart_data = get_chart_data(data)
    
    return columns, data, None, chart_data

def get_columns():
    """Define report columns."""
    
    return [
        {
            "fieldname": "product_name",
            "label": _("Product Name"),
            "fieldtype": "Link",
            "options": "Product Compliance",
            "width": 200
        },
        {
            "fieldname": "product_code",
            "label": _("Product Code"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "country",
            "label": _("Country"),
            "fieldtype": "Link", 
            "options": "Country",
            "width": 120
        },
        {
            "fieldname": "compliance_status",
            "label": _("Compliance Status"),
            "fieldtype": "Data",
            "width": 130
        },
        {
            "fieldname": "compliance_percentage",
            "label": _("Compliance %"),
            "fieldtype": "Percent",
            "width": 100
        },
        {
            "fieldname": "risk_level",
            "label": _("Risk Level"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "approval_status", 
            "label": _("Approval Status"),
            "fieldtype": "Data",
            "width": 130
        },
        {
            "fieldname": "testing_status",
            "label": _("Testing Status"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "next_review_date",
            "label": _("Next Review"),
            "fieldtype": "Date",
            "width": 110
        },
        {
            "fieldname": "days_to_review",
            "label": _("Days to Review"),
            "fieldtype": "Int",
            "width": 110
        },
        {
            "fieldname": "expiry_date",
            "label": _("Expiry Date"),
            "fieldtype": "Date",
            "width": 110
        },
        {
            "fieldname": "days_to_expiry",
            "label": _("Days to Expiry"),
            "fieldtype": "Int",
            "width": 110
        },
        {
            "fieldname": "responsible_person",
            "label": _("Responsible Person"),
            "fieldtype": "Link",
            "options": "User",
            "width": 150
        },
        {
            "fieldname": "manufacturer",
            "label": _("Manufacturer"),
            "fieldtype": "Link",
            "options": "Distribution Organization",
            "width": 150
        }
    ]

def get_data(filters):
    """Get report data based on filters."""
    
    conditions = get_conditions(filters)
    
    query = f"""
        SELECT 
            pc.name,
            pc.product_name,
            pc.product_code,
            pc.country,
            pc.compliance_status,
            pc.compliance_percentage,
            pc.risk_level,
            pc.approval_status,
            pc.testing_status,
            pc.next_review_date,
            pc.expiry_date,
            pc.responsible_person,
            pc.manufacturer,
            CASE 
                WHEN pc.next_review_date IS NOT NULL 
                THEN DATEDIFF(pc.next_review_date, CURDATE())
                ELSE NULL 
            END as days_to_review,
            CASE 
                WHEN pc.expiry_date IS NOT NULL 
                THEN DATEDIFF(pc.expiry_date, CURDATE())
                ELSE NULL 
            END as days_to_expiry
        FROM `tabProduct Compliance` pc
        WHERE pc.docstatus < 2
        {conditions}
        ORDER BY 
            pc.country,
            CASE pc.compliance_status
                WHEN 'Non-Compliant' THEN 1
                WHEN 'Expired' THEN 2
                WHEN 'Pending Review' THEN 3
                WHEN 'Partially Compliant' THEN 4
                WHEN 'Compliant' THEN 5
                ELSE 6
            END,
            pc.product_name
    """
    
    return frappe.db.sql(query, as_dict=True)

def get_conditions(filters):
    """Build SQL conditions based on filters."""
    
    conditions = ""
    
    if filters:
        if filters.get("country"):
            conditions += f" AND pc.country = '{filters['country']}'"
            
        if filters.get("compliance_status"):
            conditions += f" AND pc.compliance_status = '{filters['compliance_status']}'"
            
        if filters.get("risk_level"):
            conditions += f" AND pc.risk_level = '{filters['risk_level']}'"
            
        if filters.get("manufacturer"):
            conditions += f" AND pc.manufacturer = '{filters['manufacturer']}'"
            
        if filters.get("responsible_person"):
            conditions += f" AND pc.responsible_person = '{filters['responsible_person']}'"
            
        if filters.get("from_date"):
            conditions += f" AND pc.last_review_date >= '{filters['from_date']}'"
            
        if filters.get("to_date"):
            conditions += f" AND pc.next_review_date <= '{filters['to_date']}'"
            
    return conditions

def get_chart_data(data):
    """Generate chart data for the report."""
    
    # Compliance status distribution
    status_counts = {}
    risk_counts = {}
    country_compliance = {}
    
    for row in data:
        # Status distribution
        status = row.get('compliance_status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Risk distribution
        risk = row.get('risk_level', 'Unknown')
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        # Country compliance
        country = row.get('country', 'Unknown')
        if country not in country_compliance:
            country_compliance[country] = {'total': 0, 'compliant': 0}
        country_compliance[country]['total'] += 1
        if status == 'Compliant':
            country_compliance[country]['compliant'] += 1
    
    # Calculate compliance rates by country
    country_rates = {}
    for country, data in country_compliance.items():
        rate = (data['compliant'] / data['total'] * 100) if data['total'] > 0 else 0
        country_rates[country] = round(rate, 1)
    
    chart_data = {
        "data": {
            "labels": list(status_counts.keys()),
            "datasets": [{
                "name": "Compliance Status Distribution",
                "values": list(status_counts.values())
            }]
        },
        "type": "donut",
        "height": 300,
        "colors": ["#28a745", "#ffc107", "#dc3545", "#6c757d", "#17a2b8"]
    }
    
    return chart_data

def get_report_summary(data):
    """Generate report summary statistics."""
    
    if not data:
        return {}
    
    total_products = len(data)
    compliant_products = len([d for d in data if d.get('compliance_status') == 'Compliant'])
    non_compliant = len([d for d in data if d.get('compliance_status') == 'Non-Compliant'])
    expired = len([d for d in data if d.get('compliance_status') == 'Expired'])
    
    # Products expiring soon (within 30 days)
    expiring_soon = len([d for d in data if d.get('days_to_expiry') and d['days_to_expiry'] <= 30 and d['days_to_expiry'] > 0])
    
    # Reviews due soon (within 7 days)
    reviews_due = len([d for d in data if d.get('days_to_review') and d['days_to_review'] <= 7 and d['days_to_review'] > 0])
    
    compliance_rate = (compliant_products / total_products * 100) if total_products > 0 else 0
    
    return {
        "total_products": total_products,
        "compliant_products": compliant_products,
        "compliance_rate": round(compliance_rate, 1),
        "non_compliant": non_compliant,
        "expired": expired,
        "expiring_soon": expiring_soon,
        "reviews_due": reviews_due
    }

@frappe.whitelist()
def get_compliance_filters():
    """Get available filter options for the report."""
    
    countries = frappe.get_all("Country", fields=["name"], order_by="name")
    manufacturers = frappe.get_all("Distribution Organization", 
                                 filters={"organization_type": ["in", ["Manufacturer", "Supplier"]]},
                                 fields=["name", "organization_name"], 
                                 order_by="organization_name")
    users = frappe.get_all("User", 
                          filters={"enabled": 1, "user_type": "System User"},
                          fields=["name", "full_name"],
                          order_by="full_name")
    
    return {
        "countries": [d.name for d in countries],
        "manufacturers": [{"value": d.name, "label": d.organization_name} for d in manufacturers],
        "users": [{"value": d.name, "label": d.full_name} for d in users],
        "compliance_statuses": ["Compliant", "Pending Review", "Non-Compliant", "Partially Compliant", "Expired", "Not Applicable"],
        "risk_levels": ["Low", "Medium", "High", "Critical"]
    }
