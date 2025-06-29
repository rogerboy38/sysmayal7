/**
 * Distribution Analytics Report - Client Side Configuration
 */

frappe.query_reports["Distribution Analytics Report"] = {
    "filters": [
        {
            "fieldname": "country",
            "label": __("Country"),
            "fieldtype": "Link",
            "options": "Country",
            "width": "100px"
        },
        {
            "fieldname": "organization_type",
            "label": __("Organization Type"),
            "fieldtype": "Select",
            "options": "\nDistributor\nRetailer\nSupplier\nManufacturer\nWholesaler\nAgent\nConsultant\nOther",
            "width": "120px"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nActive\nInactive\nPending\nSuspended\nTerminated",
            "width": "100px"
        },
        {
            "fieldname": "territory",
            "label": __("Territory"),
            "fieldtype": "Link",
            "options": "Territory",
            "width": "100px"
        },
        {
            "fieldname": "regulatory_status",
            "label": __("Regulatory Status"),
            "fieldtype": "Select",
            "options": "\nCompliant\nPending Review\nNon-Compliant\nExpired\nNot Applicable",
            "width": "120px"
        },
        {
            "fieldname": "min_revenue",
            "label": __("Min Revenue"),
            "fieldtype": "Currency",
            "width": "100px"
        },
        {
            "fieldname": "max_revenue",
            "label": __("Max Revenue"),
            "fieldtype": "Currency",
            "width": "100px"
        }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // Color coding for status
        if (column.fieldname == "status") {
            if (value == "Active") {
                value = `<span style="color: #28a745; font-weight: bold;">${value}</span>`;
            } else if (value == "Inactive" || value == "Terminated") {
                value = `<span style="color: #dc3545; font-weight: bold;">${value}</span>`;
            } else if (value == "Pending" || value == "Suspended") {
                value = `<span style="color: #ffc107; font-weight: bold;">${value}</span>`;
            }
        }

        // Color coding for regulatory status
        if (column.fieldname == "regulatory_status") {
            if (value == "Compliant") {
                value = `<span style="color: #28a745; font-weight: bold;">${value}</span>`;
            } else if (value == "Non-Compliant" || value == "Expired") {
                value = `<span style="color: #dc3545; font-weight: bold;">${value}</span>`;
            } else if (value == "Pending Review") {
                value = `<span style="color: #ffc107; font-weight: bold;">${value}</span>`;
            }
        }

        // Highlight expiring agreements
        if (column.fieldname == "days_to_expiry") {
            if (data && data.days_to_expiry !== null) {
                if (data.days_to_expiry < 0) {
                    value = `<span style="color: #dc3545; font-weight: bold;">${value} (Expired)</span>`;
                } else if (data.days_to_expiry <= 30) {
                    value = `<span style="color: #fd7e14; font-weight: bold;">${value}</span>`;
                } else if (data.days_to_expiry <= 90) {
                    value = `<span style="color: #ffc107;">${value}</span>`;
                }
            }
        }

        // Format revenue with indicators
        if (column.fieldname == "annual_revenue") {
            if (data && data.annual_revenue) {
                const revenue = data.annual_revenue;
                let indicator = "";
                
                if (revenue >= 10000000) { // $10M+
                    indicator = ' <span style="color: #28a745;">●</span>';
                } else if (revenue >= 1000000) { // $1M+
                    indicator = ' <span style="color: #ffc107;">●</span>';
                } else if (revenue >= 100000) { // $100K+
                    indicator = ' <span style="color: #17a2b8;">●</span>';
                }
                
                value = value + indicator;
            }
        }

        // Contact count with visual indicator
        if (column.fieldname == "contact_count") {
            if (data && data.contact_count !== null) {
                const count = data.contact_count;
                let color = "#6c757d";
                
                if (count >= 10) {
                    color = "#28a745";
                } else if (count >= 5) {
                    color = "#ffc107";
                } else if (count >= 1) {
                    color = "#17a2b8";
                } else {
                    color = "#dc3545";
                }
                
                value = `<span style="color: ${color}; font-weight: bold;">${count}</span>`;
            }
        }

        return value;
    },

    "onload": function(report) {
        // Add custom buttons
        report.page.add_inner_button(__("Distribution Summary"), function() {
            show_distribution_summary(report);
        });

        report.page.add_inner_button(__("Performance Metrics"), function() {
            show_performance_metrics(report);
        });

        report.page.add_inner_button(__("Contact Analytics"), function() {
            show_contact_analytics(report);
        });

        report.page.add_inner_button(__("Export Analysis"), function() {
            export_distribution_analysis(report);
        });
    }
};

function show_distribution_summary(report) {
    const filters = report.get_values();
    
    frappe.call({
        method: "sysmayal.sysmayal_module.report.distribution_analytics_report.distribution_analytics_report.get_distribution_summary",
        args: { filters: filters },
        callback: function(r) {
            if (r.message) {
                display_summary_dialog(r.message);
            }
        }
    });
}

function show_performance_metrics(report) {
    const filters = report.get_values();
    
    frappe.call({
        method: "sysmayal.sysmayal_module.report.distribution_analytics_report.distribution_analytics_report.get_performance_metrics",
        args: { filters: filters },
        callback: function(r) {
            if (r.message) {
                display_performance_dialog(r.message);
            }
        }
    });
}

function show_contact_analytics(report) {
    const filters = report.get_values();
    
    frappe.call({
        method: "sysmayal.sysmayal_module.report.distribution_analytics_report.distribution_analytics_report.get_contact_analytics",
        args: { filters: filters },
        callback: function(r) {
            if (r.message) {
                display_contact_analytics_dialog(r.message);
            }
        }
    });
}

function display_summary_dialog(data) {
    const summary = data.summary;
    const geographic = data.geographic_distribution;
    const compliance = data.compliance_distribution;
    const expiring = data.expiring_agreements;

    let html = `
        <div class="row">
            <div class="col-md-6">
                <h5>Network Overview</h5>
                <table class="table table-bordered">
                    <tr><td>Total Organizations</td><td><strong>${summary.total_organizations}</strong></td></tr>
                    <tr><td>Active Organizations</td><td><strong>${summary.active_organizations}</strong></td></tr>
                    <tr><td>Countries Covered</td><td><strong>${summary.countries_covered}</strong></td></tr>
                    <tr><td>Territories Covered</td><td><strong>${summary.territories_covered}</strong></td></tr>
                </table>
                
                <h6>Organization Types</h6>
                <table class="table table-bordered">
                    <tr><td>Distributors</td><td>${summary.distributors}</td></tr>
                    <tr><td>Retailers</td><td>${summary.retailers}</td></tr>
                    <tr><td>Suppliers</td><td>${summary.suppliers}</td></tr>
                    <tr><td>Manufacturers</td><td>${summary.manufacturers}</td></tr>
                </table>
            </div>
            
            <div class="col-md-6">
                <h5>Financial Overview</h5>
                <table class="table table-bordered">
                    <tr><td>Total Revenue</td><td><strong>${format_currency(summary.total_revenue)}</strong></td></tr>
                    <tr><td>Average Revenue</td><td><strong>${format_currency(summary.avg_revenue)}</strong></td></tr>
                    <tr><td>Total Employees</td><td><strong>${summary.total_employees || 0}</strong></td></tr>
                    <tr><td>Average Employees</td><td><strong>${Math.round(summary.avg_employees || 0)}</strong></td></tr>
                </table>
                
                <h6>Compliance Status</h6>
                <table class="table table-bordered">
    `;
    
    compliance.forEach(comp => {
        html += `<tr><td>${comp.regulatory_status || 'Not Set'}</td><td>${comp.count} (${comp.percentage}%)</td></tr>`;
    });
    
    html += `
                </table>
            </div>
        </div>
    `;
    
    if (expiring.length > 0) {
        html += `
            <div class="row">
                <div class="col-md-12">
                    <h5>Expiring Agreements (Next 90 Days)</h5>
                    <table class="table table-bordered">
                        <thead>
                            <tr><th>Organization</th><th>Expiry Date</th><th>Days Left</th></tr>
                        </thead>
                        <tbody>
        `;
        
        expiring.forEach(exp => {
            const color = exp.days_to_expiry <= 30 ? 'text-danger' : 'text-warning';
            html += `<tr><td>${exp.organization_name}</td><td>${exp.agreement_expiry}</td><td class="${color}">${exp.days_to_expiry}</td></tr>`;
        });
        
        html += `
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }

    frappe.msgprint({
        title: __("Distribution Network Summary"),
        message: html,
        wide: true
    });
}

function display_performance_dialog(data) {
    const performance = data.performance_by_type;
    const growth = data.growth_analysis;

    let html = `
        <div class="row">
            <div class="col-md-12">
                <h5>Performance by Organization Type</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Count</th>
                            <th>Avg Revenue</th>
                            <th>Avg Employees</th>
                            <th>Compliance Rate</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    performance.forEach(perf => {
        html += `
            <tr>
                <td>${perf.organization_type}</td>
                <td>${perf.count}</td>
                <td>${format_currency(perf.avg_revenue)}</td>
                <td>${Math.round(perf.avg_employees || 0)}</td>
                <td>${perf.compliance_rate}%</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
                
                <h5>Growth Analysis by Age</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Age Group</th><th>Count</th><th>Average Revenue</th></tr>
                    </thead>
                    <tbody>
    `;
    
    growth.forEach(gr => {
        html += `<tr><td>${gr.age_group}</td><td>${gr.count}</td><td>${format_currency(gr.avg_revenue)}</td></tr>`;
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

function display_contact_analytics_dialog(data) {
    const contacts = data.contact_by_role;
    const communication = data.communication_preferences;

    let html = `
        <div class="row">
            <div class="col-md-6">
                <h5>Contacts by Regulatory Role</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Role</th><th>Total</th><th>Active</th><th>Organizations</th></tr>
                    </thead>
                    <tbody>
    `;
    
    contacts.forEach(contact => {
        html += `
            <tr>
                <td>${contact.regulatory_role || 'Not Set'}</td>
                <td>${contact.count}</td>
                <td>${contact.active_count}</td>
                <td>${contact.organizations_covered}</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
            </div>
            
            <div class="col-md-6">
                <h5>Communication Preferences</h5>
                <table class="table table-bordered">
                    <thead>
                        <tr><th>Preference</th><th>Count</th><th>Percentage</th></tr>
                    </thead>
                    <tbody>
    `;
    
    communication.forEach(comm => {
        html += `
            <tr>
                <td>${comm.communication_preference || 'Not Set'}</td>
                <td>${comm.count}</td>
                <td>${comm.percentage}%</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
            </div>
        </div>
    `;

    frappe.msgprint({
        title: __("Contact Analytics"),
        message: html,
        wide: true
    });
}

function export_distribution_analysis(report) {
    const data = report.data;
    if (!data || data.length === 0) {
        frappe.msgprint(__("No data to export"));
        return;
    }

    // Create comprehensive analysis export
    frappe.msgprint(__("Exporting distribution analysis..."));
    
    // In a real implementation, this would generate a comprehensive Excel report
    // with multiple sheets including summary, detailed data, and charts
}

function format_currency(amount) {
    if (!amount) return '$0';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    }).format(amount);
}
