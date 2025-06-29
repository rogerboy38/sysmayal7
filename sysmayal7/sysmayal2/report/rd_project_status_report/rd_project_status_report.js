/**
 * R&D Project Status Report - Client Side Configuration
 */

frappe.query_reports["R&D Project Status Report"] = {
    "filters": [
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nPlanning\nIn Progress\nTesting\nRegulatory Review\nCompleted\nOn Hold\nCancelled",
            "width": "100px"
        },
        {
            "fieldname": "priority",
            "label": __("Priority"),
            "fieldtype": "Select",
            "options": "\nHigh\nMedium\nLow",
            "width": "100px"
        },
        {
            "fieldname": "project_type",
            "label": __("Project Type"),
            "fieldtype": "Select",
            "options": "\nNew Product Development\nProduct Improvement\nFormulation Research\nMarket Expansion\nRegulatory Compliance\nOther",
            "width": "140px"
        },
        {
            "fieldname": "product_category",
            "label": __("Product Category"),
            "fieldtype": "Select",
            "options": "\nAloe Juice\nAloe Powder\nCosmetic Formulation\nPharmaceutical\nDietary Supplement\nOther",
            "width": "120px"
        },
        {
            "fieldname": "project_manager",
            "label": __("Project Manager"),
            "fieldtype": "Link",
            "options": "User",
            "width": "120px"
        },
        {
            "fieldname": "r_and_d_lead",
            "label": __("R&D Lead"),
            "fieldtype": "Link",
            "options": "User",
            "width": "120px"
        },
        {
            "fieldname": "compliance_status",
            "label": __("Compliance Status"),
            "fieldtype": "Select",
            "options": "\nNot Started\nIn Progress\nPending Review\nCompliant\nNon-Compliant",
            "width": "120px"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "width": "100px"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "width": "100px"
        },
        {
            "fieldname": "min_investment",
            "label": __("Min Investment"),
            "fieldtype": "Currency",
            "width": "120px"
        },
        {
            "fieldname": "max_investment",
            "label": __("Max Investment"),
            "fieldtype": "Currency",
            "width": "120px"
        }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // Color coding for status
        if (column.fieldname == "status") {
            if (value == "Completed") {
                value = `<span style="color: #28a745; font-weight: bold;">${value}</span>`;
            } else if (value == "In Progress" || value == "Testing") {
                value = `<span style="color: #17a2b8; font-weight: bold;">${value}</span>`;
            } else if (value == "On Hold" || value == "Cancelled") {
                value = `<span style="color: #dc3545; font-weight: bold;">${value}</span>`;
            } else if (value == "Regulatory Review") {
                value = `<span style="color: #ffc107; font-weight: bold;">${value}</span>`;
            }
        }

        // Color coding for priority
        if (column.fieldname == "priority") {
            if (value == "High") {
                value = `<span style="color: #dc3545; font-weight: bold;">${value}</span>`;
            } else if (value == "Medium") {
                value = `<span style="color: #ffc107; font-weight: bold;">${value}</span>`;
            } else if (value == "Low") {
                value = `<span style="color: #28a745;">${value}</span>`;
            }
        }

        // Progress bar for completion percentage
        if (column.fieldname == "completion_percentage") {
            if (data && data.completion_percentage !== null) {
                const percentage = data.completion_percentage;
                let color = "#28a745"; // Green for high progress
                
                if (percentage < 25) {
                    color = "#dc3545"; // Red for low progress
                } else if (percentage < 50) {
                    color = "#fd7e14"; // Orange for low-medium progress
                } else if (percentage < 75) {
                    color = "#ffc107"; // Yellow for medium-high progress
                }
                
                value = `
                    <div style="display: flex; align-items: center;">
                        <div style="
                            width: 80px; 
                            height: 12px; 
                            background: #f5f5f5; 
                            border-radius: 6px; 
                            margin-right: 8px; 
                            overflow: hidden;
                            border: 1px solid #ddd;
                        ">
                            <div style="
                                width: ${percentage}%; 
                                height: 100%; 
                                background: ${color}; 
                                transition: width 0.3s ease;
                            "></div>
                        </div>
                        <span style="font-weight: bold;">${percentage}%</span>
                    </div>
                `;
            }
        }

        // Highlight timeline issues
        if (column.fieldname == "days_remaining") {
            if (data && data.days_remaining !== null) {
                if (data.days_remaining < 0) {
                    value = `<span style="color: #dc3545; font-weight: bold;">${Math.abs(data.days_remaining)} days overdue</span>`;
                } else if (data.days_remaining <= 30) {
                    value = `<span style="color: #fd7e14; font-weight: bold;">${value}</span>`;
                } else if (data.days_remaining <= 90) {
                    value = `<span style="color: #ffc107;">${value}</span>`;
                }
            }
        }

        // Color coding for compliance status
        if (column.fieldname == "compliance_status") {
            if (value == "Compliant") {
                value = `<span style="color: #28a745; font-weight: bold;">${value}</span>`;
            } else if (value == "Non-Compliant") {
                value = `<span style="color: #dc3545; font-weight: bold;">${value}</span>`;
            } else if (value == "In Progress" || value == "Pending Review") {
                value = `<span style="color: #ffc107; font-weight: bold;">${value}</span>`;
            }
        }

        // Investment amount formatting with indicators
        if (column.fieldname == "estimated_investment") {
            if (data && data.estimated_investment) {
                const investment = data.estimated_investment;
                let indicator = "";
                
                if (investment >= 1000000) { // $1M+
                    indicator = ' <span style="color: #dc3545;">●●●</span>';
                } else if (investment >= 500000) { // $500K+
                    indicator = ' <span style="color: #ffc107;">●●</span>';
                } else if (investment >= 100000) { // $100K+
                    indicator = ' <span style="color: #17a2b8;">●</span>';
                }
                
                value = value + indicator;
            }
        }

        return value;
    },

    "onload": function(report) {
        // Add custom buttons
        report.page.add_inner_button(__("Portfolio Summary"), function() {
            show_portfolio_summary(report);
        });

        report.page.add_inner_button(__("Performance Metrics"), function() {
            show_performance_metrics(report);
        });

        report.page.add_inner_button(__("Risk Analysis"), function() {
            show_risk_analysis(report);
        });

        report.page.add_inner_button(__("Export Portfolio"), function() {
            export_project_portfolio(report);
        });
    }
};

function show_portfolio_summary(report) {
    const filters = report.get_values();
    
    frappe.call({
        method: "sysmayal.sysmayal_module.report.rd_project_status_report.rd_project_status_report.get_project_portfolio_summary",
        args: { filters: filters },
        callback: function(r) {
            if (r.message) {
                display_portfolio_summary_dialog(r.message);
            }
        }
    });
}

function show_performance_metrics(report) {
    const filters = report.get_values();
    
    frappe.call({
        method: "sysmayal.sysmayal_module.report.rd_project_status_report.rd_project_status_report.get_project_performance_metrics",
        args: { filters: filters },
        callback: function(r) {
            if (r.message) {
                display_performance_metrics_dialog(r.message);
            }
        }
    });
}

function show_risk_analysis(report) {
    const filters = report.get_values();
    
    frappe.call({
        method: "sysmayal.sysmayal_module.report.rd_project_status_report.rd_project_status_report.get_project_risks_and_issues",
        args: { filters: filters },
        callback: function(r) {
            if (r.message) {
                display_risk_analysis_dialog(r.message);
            }
        }
    });
}

function display_portfolio_summary_dialog(data) {
    const summary = data.summary;
    const timeline = data.timeline_analysis;
    const categories = data.category_analysis;
    const resources = data.resource_allocation;

    let html = `
        <div class="row">
            <div class="col-md-6">
                <h5>Project Portfolio Overview</h5>
                <table class="table table-bordered">
                    <tr><td>Total Projects</td><td><strong>${summary.total_projects}</strong></td></tr>
                    <tr><td>Active Projects</td><td><strong>${summary.active_projects}</strong></td></tr>
                    <tr><td>Completed Projects</td><td><strong>${summary.completed_projects}</strong></td></tr>
                    <tr><td>On Hold</td><td><strong>${summary.on_hold_projects}</strong></td></tr>
                    <tr><td>Cancelled</td><td><strong>${summary.cancelled_projects}</strong></td></tr>
                    <tr><td>Average Completion</td><td><strong>${Math.round(summary.avg_completion || 0)}%</strong></td></tr>
                </table>
                
                <h6>Priority Distribution</h6>
                <table class="table table-bordered">
                    <tr><td>High Priority</td><td>${summary.high_priority}</td></tr>
                    <tr><td>Medium Priority</td><td>${summary.medium_priority}</td></tr>
                    <tr><td>Low Priority</td><td>${summary.low_priority}</td></tr>
                </table>
            </div>
            
            <div class="col-md-6">
                <h5>Financial Overview</h5>
                <table class="table table-bordered">
                    <tr><td>Total Investment</td><td><strong>${format_currency(summary.total_investment)}</strong></td></tr>
                    <tr><td>Average Investment</td><td><strong>${format_currency(summary.avg_investment)}</strong></td></tr>
                </table>
                
                <h6>Timeline Analysis</h6>
                <table class="table table-bordered">
    `;
    
    timeline.forEach(item => {
        const color = item.timeline_category === 'Overdue' ? 'text-danger' : 
                     item.timeline_category === 'Due Soon' ? 'text-warning' : '';
        html += `<tr><td class="${color}">${item.timeline_category}</td><td class="${color}">${item.count}</td></tr>`;
    });
    
    html += `
                </table>
            </div>
        </div>
    `;
    
    if (categories.length > 0) {
        html += `
            <div class="row">
                <div class="col-md-12">
                    <h5>Project Categories</h5>
                    <table class="table table-bordered">
                        <thead>
                            <tr><th>Category</th><th>Projects</th><th>Avg Progress</th><th>Investment</th><th>Completed</th></tr>
                        </thead>
                        <tbody>
        `;
        
        categories.forEach(cat => {
            html += `
                <tr>
                    <td>${cat.product_category}</td>
                    <td>${cat.project_count}</td>
                    <td>${Math.round(cat.avg_progress || 0)}%</td>
                    <td>${format_currency(cat.total_investment)}</td>
                    <td>${cat.completed_count}</td>
                </tr>
            `;
        });
        
        html += `
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    frappe.msgprint({
        title: __("R&D Portfolio Summary"),
        message: html,
        wide: true
    });
}

function display_performance_metrics_dialog(data) {
    const completion = data.completion_by_status;
    const investment = data.investment_analysis;
    const compliance = data.compliance_analysis;

    let html = `
        <div class="row">
            <div class="col-md-6">
                <h5>Completion Rate by Status</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Status</th><th>Projects</th><th>Avg Completion</th><th>Range</th></tr>
                    </thead>
                    <tbody>
    `;
    
    completion.forEach(comp => {
        html += `
            <tr>
                <td>${comp.status}</td>
                <td>${comp.project_count}</td>
                <td>${Math.round(comp.avg_completion || 0)}%</td>
                <td>${Math.round(comp.min_completion || 0)}% - ${Math.round(comp.max_completion || 0)}%</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
            </div>
            
            <div class="col-md-6">
                <h5>Investment Analysis</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Investment Size</th><th>Projects</th><th>Avg Progress</th><th>Avg Duration</th></tr>
                    </thead>
                    <tbody>
    `;
    
    investment.forEach(inv => {
        html += `
            <tr>
                <td>${inv.investment_category}</td>
                <td>${inv.project_count}</td>
                <td>${Math.round(inv.avg_progress || 0)}%</td>
                <td>${Math.round(inv.avg_duration_days || 0)} days</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
                
                <h6>Compliance Status</h6>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Status</th><th>Projects</th><th>Avg Progress</th></tr>
                    </thead>
                    <tbody>
    `;
    
    compliance.forEach(comp => {
        html += `<tr><td>${comp.compliance_status}</td><td>${comp.project_count}</td><td>${Math.round(comp.avg_progress || 0)}%</td></tr>`;
    });
    
    html += `
                    </tbody>
                </table>
            </div>
        </div>
    `;

    frappe.msgprint({
        title: __("Performance Metrics"),
        message: html,
        wide: true
    });
}

function display_risk_analysis_dialog(data) {
    const overdue = data.overdue_projects;
    const stalled = data.stalled_projects;
    const high_risk = data.high_risk_projects;

    let html = '<div class="row">';
    
    if (overdue.length > 0) {
        html += `
            <div class="col-md-12">
                <h5 style="color: #dc3545;">Overdue Projects</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Project</th><th>Status</th><th>Expected Completion</th><th>Progress</th><th>Days Overdue</th></tr>
                    </thead>
                    <tbody>
        `;
        
        overdue.forEach(proj => {
            html += `
                <tr>
                    <td>${proj.project_name}</td>
                    <td>${proj.status}</td>
                    <td>${proj.expected_completion}</td>
                    <td>${proj.completion_percentage || 0}%</td>
                    <td class="text-danger"><strong>${proj.days_overdue}</strong></td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div>';
    }
    
    if (stalled.length > 0) {
        html += `
            <div class="col-md-12">
                <h5 style="color: #ffc107;">Stalled Projects</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Project</th><th>Status</th><th>Start Date</th><th>Progress</th><th>Days Since Start</th></tr>
                    </thead>
                    <tbody>
        `;
        
        stalled.forEach(proj => {
            html += `
                <tr>
                    <td>${proj.project_name}</td>
                    <td>${proj.status}</td>
                    <td>${proj.start_date}</td>
                    <td>${proj.completion_percentage || 0}%</td>
                    <td class="text-warning"><strong>${proj.days_since_start}</strong></td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div>';
    }
    
    if (high_risk.length > 0) {
        html += `
            <div class="col-md-12">
                <h5 style="color: #fd7e14;">High Risk Projects</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Project</th><th>Investment</th><th>Progress</th><th>Status</th></tr>
                    </thead>
                    <tbody>
        `;
        
        high_risk.forEach(proj => {
            html += `
                <tr>
                    <td>${proj.project_name}</td>
                    <td>${format_currency(proj.estimated_investment)}</td>
                    <td>${proj.completion_percentage || 0}%</td>
                    <td>${proj.status}</td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div>';
    }
    
    html += '</div>';
    
    if (overdue.length === 0 && stalled.length === 0 && high_risk.length === 0) {
        html = '<div class="text-center text-success"><h5>No significant risks identified in current project portfolio</h5></div>';
    }

    frappe.msgprint({
        title: __("Risk Analysis"),
        message: html,
        wide: true
    });
}

function export_project_portfolio(report) {
    const data = report.data;
    if (!data || data.length === 0) {
        frappe.msgprint(__("No data to export"));
        return;
    }

    frappe.msgprint(__("Exporting project portfolio analysis..."));
    
    // In a real implementation, this would generate a comprehensive Excel report
    // with multiple sheets including project details, timeline analysis, and charts
}

function format_currency(amount) {
    if (!amount) return '$0';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    }).format(amount);
}
