"""
Distribution Analytics Report

This report provides comprehensive analytics on distribution network
including organization performance, geographic coverage, and growth trends.
"""

import frappe
from frappe import _
from frappe.utils import nowdate, add_months

def execute(filters=None):
    """Execute the distribution analytics report."""
    
    columns = get_columns()
    data = get_data(filters)
    chart_data = get_chart_data(data)
    
    return columns, data, None, chart_data

def get_columns():
    """Define report columns."""
    
    return [
        {
            "fieldname": "organization_name",
            "label": _("Organization"),
            "fieldtype": "Link",
            "options": "Distribution Organization",
            "width": 200
        },
        {
            "fieldname": "organization_type",
            "label": _("Type"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "country",
            "label": _("Country"),
            "fieldtype": "Link",
            "options": "Country",
            "width": 120
        },
        {
            "fieldname": "territory",
            "label": _("Territory"),
            "fieldtype": "Link",
            "options": "Territory",
            "width": 120
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "contact_count",
            "label": _("Contacts"),
            "fieldtype": "Int",
            "width": 80
        },
        {
            "fieldname": "regulatory_status",
            "label": _("Regulatory Status"),
            "fieldtype": "Data",
            "width": 130
        },
        {
            "fieldname": "annual_revenue",
            "label": _("Annual Revenue"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "employee_count",
            "label": _("Employees"),
            "fieldtype": "Int",
            "width": 90
        },
        {
            "fieldname": "established_year",
            "label": _("Established"),
            "fieldtype": "Int",
            "width": 90
        },
        {
            "fieldname": "agreement_expiry",
            "label": _("Agreement Expiry"),
            "fieldtype": "Date",
            "width": 120
        },
        {
            "fieldname": "days_to_expiry",
            "label": _("Days to Expiry"),
            "fieldtype": "Int",
            "width": 110
        },
        {
            "fieldname": "last_audit_date",
            "label": _("Last Audit"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "next_audit_due",
            "label": _("Next Audit Due"),
            "fieldtype": "Date",
            "width": 110
        },
        {
            "fieldname": "business_focus",
            "label": _("Business Focus"),
            "fieldtype": "Data",
            "width": 150
        }
    ]

def get_data(filters):
    """Get report data based on filters."""
    
    conditions = get_conditions(filters)
    
    query = f"""
        SELECT 
            org.name,
            org.organization_name,
            org.organization_type,
            org.country,
            org.territory,
            org.status,
            org.regulatory_status,
            org.annual_revenue,
            org.employee_count,
            org.established_year,
            org.agreement_expiry,
            org.last_audit_date,
            org.next_audit_due,
            org.business_focus,
            (SELECT COUNT(*) 
             FROM `tabDistribution Contact` dc 
             WHERE dc.organization = org.name 
             AND dc.status = 'Active') as contact_count,
            CASE 
                WHEN org.agreement_expiry IS NOT NULL 
                THEN DATEDIFF(org.agreement_expiry, CURDATE())
                ELSE NULL 
            END as days_to_expiry
        FROM `tabDistribution Organization` org
        WHERE org.docstatus < 2
        {conditions}
        ORDER BY 
            org.country,
            org.organization_type,
            org.organization_name
    """
    
    return frappe.db.sql(query, as_dict=True)

def get_conditions(filters):
    """Build SQL conditions based on filters."""
    
    conditions = ""
    
    if filters:
        if filters.get("country"):
            conditions += f" AND org.country = '{filters['country']}'"
            
        if filters.get("organization_type"):
            conditions += f" AND org.organization_type = '{filters['organization_type']}'"
            
        if filters.get("status"):
            conditions += f" AND org.status = '{filters['status']}'"
            
        if filters.get("territory"):
            conditions += f" AND org.territory = '{filters['territory']}'"
            
        if filters.get("regulatory_status"):
            conditions += f" AND org.regulatory_status = '{filters['regulatory_status']}'"
            
        if filters.get("min_revenue"):
            conditions += f" AND org.annual_revenue >= {filters['min_revenue']}"
            
        if filters.get("max_revenue"):
            conditions += f" AND org.annual_revenue <= {filters['max_revenue']}"
            
    return conditions

def get_chart_data(data):
    """Generate chart data for the report."""
    
    # Organization type distribution
    type_counts = {}
    country_counts = {}
    status_counts = {}
    revenue_by_type = {}
    
    for row in data:
        # Type distribution
        org_type = row.get('organization_type', 'Unknown')
        type_counts[org_type] = type_counts.get(org_type, 0) + 1
        
        # Country distribution
        country = row.get('country', 'Unknown')
        country_counts[country] = country_counts.get(country, 0) + 1
        
        # Status distribution
        status = row.get('status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Revenue by type
        if org_type not in revenue_by_type:
            revenue_by_type[org_type] = 0
        if row.get('annual_revenue'):
            revenue_by_type[org_type] += row['annual_revenue']
    
    chart_data = {
        "data": {
            "labels": list(type_counts.keys()),
            "datasets": [{
                "name": "Organizations by Type",
                "values": list(type_counts.values())
            }]
        },
        "type": "bar",
        "height": 300,
        "colors": ["#28a745", "#17a2b8", "#ffc107", "#dc3545", "#6f42c1"]
    }
    
    return chart_data

@frappe.whitelist()
def get_distribution_summary(filters=None):
    """Get distribution network summary statistics."""
    
    conditions = get_conditions(filters) if filters else ""
    
    # Basic counts
    summary_query = f"""
        SELECT 
            COUNT(*) as total_organizations,
            COUNT(CASE WHEN status = 'Active' THEN 1 END) as active_organizations,
            COUNT(CASE WHEN organization_type = 'Distributor' THEN 1 END) as distributors,
            COUNT(CASE WHEN organization_type = 'Retailer' THEN 1 END) as retailers,
            COUNT(CASE WHEN organization_type = 'Supplier' THEN 1 END) as suppliers,
            COUNT(CASE WHEN organization_type = 'Manufacturer' THEN 1 END) as manufacturers,
            COUNT(DISTINCT country) as countries_covered,
            COUNT(DISTINCT territory) as territories_covered,
            AVG(annual_revenue) as avg_revenue,
            SUM(annual_revenue) as total_revenue,
            AVG(employee_count) as avg_employees,
            SUM(employee_count) as total_employees
        FROM `tabDistribution Organization`
        WHERE docstatus < 2
        {conditions}
    """
    
    summary = frappe.db.sql(summary_query, as_dict=True)[0]
    
    # Geographic distribution
    geo_query = f"""
        SELECT 
            country,
            COUNT(*) as org_count,
            AVG(annual_revenue) as avg_revenue,
            COUNT(CASE WHEN status = 'Active' THEN 1 END) as active_count
        FROM `tabDistribution Organization`
        WHERE docstatus < 2
        {conditions}
        GROUP BY country
        ORDER BY org_count DESC
    """
    
    geographic_data = frappe.db.sql(geo_query, as_dict=True)
    
    # Compliance distribution
    compliance_query = f"""
        SELECT 
            regulatory_status,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM `tabDistribution Organization` WHERE docstatus < 2 {conditions}), 1) as percentage
        FROM `tabDistribution Organization`
        WHERE docstatus < 2
        {conditions}
        GROUP BY regulatory_status
        ORDER BY count DESC
    """
    
    compliance_data = frappe.db.sql(compliance_query, as_dict=True)
    
    # Expiring agreements
    expiring_query = f"""
        SELECT 
            organization_name,
            agreement_expiry,
            DATEDIFF(agreement_expiry, CURDATE()) as days_to_expiry
        FROM `tabDistribution Organization`
        WHERE docstatus < 2
        AND agreement_expiry IS NOT NULL
        AND agreement_expiry BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 90 DAY)
        {conditions}
        ORDER BY agreement_expiry
    """
    
    expiring_agreements = frappe.db.sql(expiring_query, as_dict=True)
    
    return {
        "summary": summary,
        "geographic_distribution": geographic_data,
        "compliance_distribution": compliance_data,
        "expiring_agreements": expiring_agreements
    }

@frappe.whitelist()
def get_performance_metrics(filters=None):
    """Get performance metrics for distribution network."""
    
    conditions = get_conditions(filters) if filters else ""
    
    # Performance by type
    performance_query = f"""
        SELECT 
            organization_type,
            COUNT(*) as count,
            AVG(annual_revenue) as avg_revenue,
            AVG(employee_count) as avg_employees,
            COUNT(CASE WHEN regulatory_status = 'Compliant' THEN 1 END) as compliant_count,
            ROUND(COUNT(CASE WHEN regulatory_status = 'Compliant' THEN 1 END) * 100.0 / COUNT(*), 1) as compliance_rate
        FROM `tabDistribution Organization`
        WHERE docstatus < 2
        {conditions}
        GROUP BY organization_type
        ORDER BY count DESC
    """
    
    performance_data = frappe.db.sql(performance_query, as_dict=True)
    
    # Growth analysis (based on established year)
    growth_query = f"""
        SELECT 
            CASE 
                WHEN established_year >= YEAR(CURDATE()) - 2 THEN 'New (0-2 years)'
                WHEN established_year >= YEAR(CURDATE()) - 5 THEN 'Young (3-5 years)'
                WHEN established_year >= YEAR(CURDATE()) - 10 THEN 'Mature (6-10 years)'
                ELSE 'Established (10+ years)'
            END as age_group,
            COUNT(*) as count,
            AVG(annual_revenue) as avg_revenue
        FROM `tabDistribution Organization`
        WHERE docstatus < 2
        AND established_year IS NOT NULL
        {conditions}
        GROUP BY age_group
        ORDER BY 
            CASE age_group
                WHEN 'New (0-2 years)' THEN 1
                WHEN 'Young (3-5 years)' THEN 2
                WHEN 'Mature (6-10 years)' THEN 3
                ELSE 4
            END
    """
    
    growth_data = frappe.db.sql(growth_query, as_dict=True)
    
    return {
        "performance_by_type": performance_data,
        "growth_analysis": growth_data
    }

@frappe.whitelist()
def get_contact_analytics(filters=None):
    """Get contact analytics for distribution network."""
    
    org_conditions = get_conditions(filters) if filters else ""
    
    # Contact distribution by role
    contact_query = f"""
        SELECT 
            dc.regulatory_role,
            COUNT(*) as count,
            COUNT(CASE WHEN dc.status = 'Active' THEN 1 END) as active_count,
            COUNT(DISTINCT dc.organization) as organizations_covered
        FROM `tabDistribution Contact` dc
        JOIN `tabDistribution Organization` org ON dc.organization = org.name
        WHERE dc.docstatus < 2
        AND org.docstatus < 2
        {org_conditions.replace('org.', 'org.')}
        GROUP BY dc.regulatory_role
        ORDER BY count DESC
    """
    
    contact_data = frappe.db.sql(contact_query, as_dict=True)
    
    # Communication preferences
    comm_query = f"""
        SELECT 
            dc.communication_preference,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM `tabDistribution Contact` WHERE docstatus < 2), 1) as percentage
        FROM `tabDistribution Contact` dc
        JOIN `tabDistribution Organization` org ON dc.organization = org.name
        WHERE dc.docstatus < 2
        AND org.docstatus < 2
        {org_conditions.replace('org.', 'org.')}
        GROUP BY dc.communication_preference
        ORDER BY count DESC
    """
    
    communication_data = frappe.db.sql(comm_query, as_dict=True)
    
    return {
        "contact_by_role": contact_data,
        "communication_preferences": communication_data
    }
