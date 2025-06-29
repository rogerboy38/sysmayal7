"""
R&D Project Status Report

This report provides comprehensive overview of research and development
projects including progress tracking, resource allocation, and timeline analysis.
"""

import frappe
from frappe import _
from frappe.utils import date_diff, nowdate

def execute(filters=None):
    """Execute the R&D project status report."""
    
    columns = get_columns()
    data = get_data(filters)
    chart_data = get_chart_data(data)
    
    return columns, data, None, chart_data

def get_columns():
    """Define report columns."""
    
    return [
        {
            "fieldname": "project_name",
            "label": _("Project Name"),
            "fieldtype": "Link",
            "options": "Product Development Project",
            "width": 200
        },
        {
            "fieldname": "project_type",
            "label": _("Project Type"),
            "fieldtype": "Data",
            "width": 140
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "priority",
            "label": _("Priority"),
            "fieldtype": "Data",
            "width": 80
        },
        {
            "fieldname": "completion_percentage",
            "label": _("Progress"),
            "fieldtype": "Percent",
            "width": 100
        },
        {
            "fieldname": "current_phase",
            "label": _("Current Phase"),
            "fieldtype": "Data",
            "width": 130
        },
        {
            "fieldname": "start_date",
            "label": _("Start Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "expected_completion",
            "label": _("Expected Completion"),
            "fieldtype": "Date",
            "width": 130
        },
        {
            "fieldname": "days_remaining",
            "label": _("Days Remaining"),
            "fieldtype": "Int",
            "width": 110
        },
        {
            "fieldname": "product_category",
            "label": _("Product Category"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "target_markets",
            "label": _("Target Markets"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "estimated_investment",
            "label": _("Investment"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "project_manager",
            "label": _("Project Manager"),
            "fieldtype": "Link",
            "options": "User",
            "width": 140
        },
        {
            "fieldname": "r_and_d_lead",
            "label": _("R&D Lead"),
            "fieldtype": "Link",
            "options": "User",
            "width": 120
        },
        {
            "fieldname": "regulatory_lead",
            "label": _("Regulatory Lead"),
            "fieldtype": "Link",
            "options": "User",
            "width": 130
        },
        {
            "fieldname": "compliance_status",
            "label": _("Compliance Status"),
            "fieldtype": "Data",
            "width": 130
        },
        {
            "fieldname": "next_milestone",
            "label": _("Next Milestone"),
            "fieldtype": "Data",
            "width": 150
        }
    ]

def get_data(filters):
    """Get report data based on filters."""
    
    conditions = get_conditions(filters)
    
    query = f"""
        SELECT 
            proj.name,
            proj.project_name,
            proj.project_type,
            proj.status,
            proj.priority,
            proj.completion_percentage,
            proj.current_phase,
            proj.start_date,
            proj.expected_completion,
            proj.product_category,
            proj.target_markets,
            proj.estimated_investment,
            proj.project_manager,
            proj.r_and_d_lead,
            proj.regulatory_lead,
            proj.compliance_status,
            proj.next_milestone,
            CASE 
                WHEN proj.expected_completion IS NOT NULL 
                THEN DATEDIFF(proj.expected_completion, CURDATE())
                ELSE NULL 
            END as days_remaining
        FROM `tabProduct Development Project` proj
        WHERE proj.docstatus < 2
        {conditions}
        ORDER BY 
            CASE proj.priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
                ELSE 4
            END,
            CASE proj.status
                WHEN 'In Progress' THEN 1
                WHEN 'Testing' THEN 2
                WHEN 'Regulatory Review' THEN 3
                WHEN 'Planning' THEN 4
                WHEN 'Completed' THEN 5
                ELSE 6
            END,
            proj.expected_completion
    """
    
    return frappe.db.sql(query, as_dict=True)

def get_conditions(filters):
    """Build SQL conditions based on filters."""
    
    conditions = ""
    
    if filters:
        if filters.get("status"):
            conditions += f" AND proj.status = '{filters['status']}'"
            
        if filters.get("priority"):
            conditions += f" AND proj.priority = '{filters['priority']}'"
            
        if filters.get("project_type"):
            conditions += f" AND proj.project_type = '{filters['project_type']}'"
            
        if filters.get("product_category"):
            conditions += f" AND proj.product_category = '{filters['product_category']}'"
            
        if filters.get("project_manager"):
            conditions += f" AND proj.project_manager = '{filters['project_manager']}'"
            
        if filters.get("r_and_d_lead"):
            conditions += f" AND proj.r_and_d_lead = '{filters['r_and_d_lead']}'"
            
        if filters.get("compliance_status"):
            conditions += f" AND proj.compliance_status = '{filters['compliance_status']}'"
            
        if filters.get("from_date"):
            conditions += f" AND proj.start_date >= '{filters['from_date']}'"
            
        if filters.get("to_date"):
            conditions += f" AND proj.expected_completion <= '{filters['to_date']}'"
            
        if filters.get("min_investment"):
            conditions += f" AND proj.estimated_investment >= {filters['min_investment']}"
            
        if filters.get("max_investment"):
            conditions += f" AND proj.estimated_investment <= {filters['max_investment']}"
            
    return conditions

def get_chart_data(data):
    """Generate chart data for the report."""
    
    # Status distribution
    status_counts = {}
    priority_counts = {}
    category_counts = {}
    phase_counts = {}
    
    for row in data:
        # Status distribution
        status = row.get('status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Priority distribution
        priority = row.get('priority', 'Unknown')
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Category distribution
        category = row.get('product_category', 'Unknown')
        category_counts[category] = category_counts.get(category, 0) + 1
        
        # Phase distribution
        phase = row.get('current_phase', 'Unknown')
        phase_counts[phase] = phase_counts.get(phase, 0) + 1
    
    chart_data = {
        "data": {
            "labels": list(status_counts.keys()),
            "datasets": [{
                "name": "Projects by Status",
                "values": list(status_counts.values())
            }]
        },
        "type": "pie",
        "height": 300,
        "colors": ["#28a745", "#17a2b8", "#ffc107", "#dc3545", "#6f42c1", "#fd7e14"]
    }
    
    return chart_data

@frappe.whitelist()
def get_project_portfolio_summary(filters=None):
    """Get project portfolio summary statistics."""
    
    conditions = get_conditions(filters) if filters else ""
    
    # Basic project metrics
    summary_query = f"""
        SELECT 
            COUNT(*) as total_projects,
            COUNT(CASE WHEN status IN ('In Progress', 'Testing', 'Regulatory Review') THEN 1 END) as active_projects,
            COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_projects,
            COUNT(CASE WHEN status = 'On Hold' THEN 1 END) as on_hold_projects,
            COUNT(CASE WHEN status = 'Cancelled' THEN 1 END) as cancelled_projects,
            COUNT(CASE WHEN priority = 'High' THEN 1 END) as high_priority,
            COUNT(CASE WHEN priority = 'Medium' THEN 1 END) as medium_priority,
            COUNT(CASE WHEN priority = 'Low' THEN 1 END) as low_priority,
            AVG(completion_percentage) as avg_completion,
            SUM(estimated_investment) as total_investment,
            AVG(estimated_investment) as avg_investment
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        {conditions}
    """
    
    summary = frappe.db.sql(summary_query, as_dict=True)[0]
    
    # Timeline analysis
    timeline_query = f"""
        SELECT 
            CASE 
                WHEN expected_completion < CURDATE() AND status NOT IN ('Completed', 'Cancelled') THEN 'Overdue'
                WHEN expected_completion BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN 'Due Soon'
                WHEN expected_completion BETWEEN DATE_ADD(CURDATE(), INTERVAL 31 DAY) AND DATE_ADD(CURDATE(), INTERVAL 90 DAY) THEN 'Due This Quarter'
                ELSE 'Future'
            END as timeline_category,
            COUNT(*) as count
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        AND expected_completion IS NOT NULL
        AND status NOT IN ('Completed', 'Cancelled')
        {conditions}
        GROUP BY timeline_category
    """
    
    timeline_data = frappe.db.sql(timeline_query, as_dict=True)
    
    # Product category analysis
    category_query = f"""
        SELECT 
            product_category,
            COUNT(*) as project_count,
            AVG(completion_percentage) as avg_progress,
            SUM(estimated_investment) as total_investment,
            COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_count
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        AND product_category IS NOT NULL
        {conditions}
        GROUP BY product_category
        ORDER BY project_count DESC
    """
    
    category_data = frappe.db.sql(category_query, as_dict=True)
    
    # Resource allocation
    resource_query = f"""
        SELECT 
            project_manager,
            COUNT(*) as managed_projects,
            AVG(completion_percentage) as avg_progress,
            COUNT(CASE WHEN status IN ('In Progress', 'Testing', 'Regulatory Review') THEN 1 END) as active_projects
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        AND project_manager IS NOT NULL
        {conditions}
        GROUP BY project_manager
        ORDER BY managed_projects DESC
    """
    
    resource_data = frappe.db.sql(resource_query, as_dict=True)
    
    return {
        "summary": summary,
        "timeline_analysis": timeline_data,
        "category_analysis": category_data,
        "resource_allocation": resource_data
    }

@frappe.whitelist()
def get_project_performance_metrics(filters=None):
    """Get detailed project performance metrics."""
    
    conditions = get_conditions(filters) if filters else ""
    
    # Completion rate by status
    completion_query = f"""
        SELECT 
            status,
            COUNT(*) as project_count,
            AVG(completion_percentage) as avg_completion,
            MIN(completion_percentage) as min_completion,
            MAX(completion_percentage) as max_completion
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        {conditions}
        GROUP BY status
        ORDER BY avg_completion DESC
    """
    
    completion_data = frappe.db.sql(completion_query, as_dict=True)
    
    # Investment vs progress analysis
    investment_query = f"""
        SELECT 
            CASE 
                WHEN estimated_investment < 100000 THEN 'Small (<$100K)'
                WHEN estimated_investment < 500000 THEN 'Medium ($100K-$500K)'
                WHEN estimated_investment < 1000000 THEN 'Large ($500K-$1M)'
                ELSE 'Major (>$1M)'
            END as investment_category,
            COUNT(*) as project_count,
            AVG(completion_percentage) as avg_progress,
            AVG(DATEDIFF(expected_completion, start_date)) as avg_duration_days
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        AND estimated_investment IS NOT NULL
        AND start_date IS NOT NULL
        AND expected_completion IS NOT NULL
        {conditions}
        GROUP BY investment_category
        ORDER BY 
            CASE investment_category
                WHEN 'Small (<$100K)' THEN 1
                WHEN 'Medium ($100K-$500K)' THEN 2
                WHEN 'Large ($500K-$1M)' THEN 3
                ELSE 4
            END
    """
    
    investment_data = frappe.db.sql(investment_query, as_dict=True)
    
    # Compliance status analysis
    compliance_query = f"""
        SELECT 
            compliance_status,
            COUNT(*) as project_count,
            AVG(completion_percentage) as avg_progress,
            COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_count
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        AND compliance_status IS NOT NULL
        {conditions}
        GROUP BY compliance_status
        ORDER BY project_count DESC
    """
    
    compliance_data = frappe.db.sql(compliance_query, as_dict=True)
    
    return {
        "completion_by_status": completion_data,
        "investment_analysis": investment_data,
        "compliance_analysis": compliance_data
    }

@frappe.whitelist()
def get_project_risks_and_issues(filters=None):
    """Identify project risks and issues."""
    
    conditions = get_conditions(filters) if filters else ""
    
    # Overdue projects
    overdue_query = f"""
        SELECT 
            project_name,
            status,
            expected_completion,
            completion_percentage,
            DATEDIFF(CURDATE(), expected_completion) as days_overdue
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        AND expected_completion < CURDATE()
        AND status NOT IN ('Completed', 'Cancelled')
        {conditions}
        ORDER BY days_overdue DESC
    """
    
    overdue_projects = frappe.db.sql(overdue_query, as_dict=True)
    
    # Stalled projects (low progress for extended period)
    stalled_query = f"""
        SELECT 
            project_name,
            status,
            completion_percentage,
            start_date,
            DATEDIFF(CURDATE(), start_date) as days_since_start
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        AND start_date IS NOT NULL
        AND DATEDIFF(CURDATE(), start_date) > 180
        AND completion_percentage < 25
        AND status NOT IN ('Completed', 'Cancelled', 'On Hold')
        {conditions}
        ORDER BY days_since_start DESC
    """
    
    stalled_projects = frappe.db.sql(stalled_query, as_dict=True)
    
    # High investment, low progress projects
    risk_query = f"""
        SELECT 
            project_name,
            estimated_investment,
            completion_percentage,
            status,
            start_date
        FROM `tabProduct Development Project`
        WHERE docstatus < 2
        AND estimated_investment > 500000
        AND completion_percentage < 50
        AND status NOT IN ('Completed', 'Cancelled')
        {conditions}
        ORDER BY estimated_investment DESC
    """
    
    high_risk_projects = frappe.db.sql(risk_query, as_dict=True)
    
    return {
        "overdue_projects": overdue_projects,
        "stalled_projects": stalled_projects,
        "high_risk_projects": high_risk_projects
    }
