/**
 * Compliance Status Report - Client Side Configuration
 */

frappe.query_reports["Compliance Status Report"] = {
    "filters": [
        {
            "fieldname": "country",
            "label": __("Country"),
            "fieldtype": "Link",
            "options": "Country",
            "width": "100px"
        },
        {
            "fieldname": "compliance_status",
            "label": __("Compliance Status"),
            "fieldtype": "Select",
            "options": "\nCompliant\nPending Review\nNon-Compliant\nPartially Compliant\nExpired\nNot Applicable",
            "width": "100px"
        },
        {
            "fieldname": "risk_level",
            "label": __("Risk Level"),
            "fieldtype": "Select",
            "options": "\nLow\nMedium\nHigh\nCritical",
            "width": "100px"
        },
        {
            "fieldname": "manufacturer",
            "label": __("Manufacturer"),
            "fieldtype": "Link",
            "options": "Distribution Organization",
            "get_query": function() {
                return {
                    "filters": {
                        "organization_type": ["in", ["Manufacturer", "Supplier"]]
                    }
                };
            },
            "width": "100px"
        },
        {
            "fieldname": "responsible_person",
            "label": __("Responsible Person"),
            "fieldtype": "Link",
            "options": "User",
            "width": "100px"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "width": "80px"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "width": "80px"
        }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        // Color coding for compliance status
        if (column.fieldname == "compliance_status") {
            if (value == "Compliant") {
                value = `<span style="color: #28a745; font-weight: bold;">${value}</span>`;
            } else if (value == "Non-Compliant" || value == "Expired") {
                value = `<span style="color: #dc3545; font-weight: bold;">${value}</span>`;
            } else if (value == "Pending Review" || value == "Partially Compliant") {
                value = `<span style="color: #ffc107; font-weight: bold;">${value}</span>`;
            }
        }

        // Color coding for risk level
        if (column.fieldname == "risk_level") {
            if (value == "Critical") {
                value = `<span style="color: #dc3545; font-weight: bold;">${value}</span>`;
            } else if (value == "High") {
                value = `<span style="color: #fd7e14; font-weight: bold;">${value}</span>`;
            } else if (value == "Medium") {
                value = `<span style="color: #ffc107;">${value}</span>`;
            } else if (value == "Low") {
                value = `<span style="color: #28a745;">${value}</span>`;
            }
        }

        // Highlight expiring products
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

        // Highlight overdue reviews
        if (column.fieldname == "days_to_review") {
            if (data && data.days_to_review !== null) {
                if (data.days_to_review < 0) {
                    value = `<span style="color: #dc3545; font-weight: bold;">${value} (Overdue)</span>`;
                } else if (data.days_to_review <= 7) {
                    value = `<span style="color: #fd7e14; font-weight: bold;">${value}</span>`;
                } else if (data.days_to_review <= 30) {
                    value = `<span style="color: #ffc107;">${value}</span>`;
                }
            }
        }

        // Progress bar for compliance percentage
        if (column.fieldname == "compliance_percentage") {
            if (data && data.compliance_percentage !== null) {
                const percentage = data.compliance_percentage;
                let color = "#28a745"; // Green for high compliance
                
                if (percentage < 50) {
                    color = "#dc3545"; // Red for low compliance
                } else if (percentage < 80) {
                    color = "#ffc107"; // Yellow for medium compliance
                }
                
                value = `
                    <div style="display: flex; align-items: center;">
                        <div style="
                            width: 60px; 
                            height: 8px; 
                            background: #f5f5f5; 
                            border-radius: 4px; 
                            margin-right: 8px; 
                            overflow: hidden;
                        ">
                            <div style="
                                width: ${percentage}%; 
                                height: 100%; 
                                background: ${color}; 
                                transition: width 0.3s ease;
                            "></div>
                        </div>
                        <span>${percentage}%</span>
                    </div>
                `;
            }
        }

        return value;
    },

    "onload": function(report) {
        // Add custom buttons
        report.page.add_inner_button(__("Export Compliance Summary"), function() {
            export_compliance_summary(report);
        });

        report.page.add_inner_button(__("Send Alerts"), function() {
            send_compliance_alerts(report);
        });

        report.page.add_inner_button(__("Update Status"), function() {
            bulk_update_compliance_status(report);
        });
    }
};

function export_compliance_summary(report) {
    // Export compliance summary
    const data = report.data;
    if (!data || data.length === 0) {
        frappe.msgprint(__("No data to export"));
        return;
    }

    // Generate summary data
    const summary = generate_summary_data(data);
    
    // Create and download CSV
    const csv_data = convert_to_csv(summary);
    download_csv(csv_data, "compliance_summary.csv");
}

function send_compliance_alerts(report) {
    const data = report.data;
    if (!data || data.length === 0) {
        frappe.msgprint(__("No data available"));
        return;
    }

    // Find products that need alerts
    const alerts_needed = data.filter(row => {
        return (row.days_to_expiry && row.days_to_expiry <= 30 && row.days_to_expiry > 0) ||
               (row.days_to_review && row.days_to_review <= 7 && row.days_to_review > 0) ||
               row.compliance_status === "Non-Compliant";
    });

    if (alerts_needed.length === 0) {
        frappe.msgprint(__("No alerts needed at this time"));
        return;
    }

    frappe.confirm(
        __("Send compliance alerts for {0} products?", [alerts_needed.length]),
        function() {
            frappe.call({
                method: "sysmayal.sysmayal_module.report.compliance_status_report.compliance_status_report.send_compliance_alerts",
                args: {
                    products: alerts_needed
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__("Alerts sent successfully"));
                    }
                }
            });
        }
    );
}

function bulk_update_compliance_status(report) {
    const selected_rows = report.datatable.rowmanager.getCheckedRows();
    
    if (selected_rows.length === 0) {
        frappe.msgprint(__("Please select products to update"));
        return;
    }

    const dialog = new frappe.ui.Dialog({
        title: __("Update Compliance Status"),
        fields: [
            {
                fieldname: "new_status",
                label: __("New Status"),
                fieldtype: "Select",
                options: "Compliant\nPending Review\nNon-Compliant\nPartially Compliant\nExpired\nNot Applicable",
                reqd: 1
            },
            {
                fieldname: "notes",
                label: __("Notes"),
                fieldtype: "Text",
                description: __("Optional notes about the status change")
            }
        ],
        primary_action_label: __("Update"),
        primary_action: function(values) {
            const product_names = selected_rows.map(idx => report.data[idx].name);
            
            frappe.call({
                method: "sysmayal.sysmayal_module.doctype.product_compliance.product_compliance.bulk_update_compliance_status",
                args: {
                    product_names: product_names,
                    new_status: values.new_status,
                    notes: values.notes
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(r.message);
                        report.refresh();
                        dialog.hide();
                    }
                }
            });
        }
    });

    dialog.show();
}

function generate_summary_data(data) {
    // Generate summary statistics
    const total = data.length;
    const compliant = data.filter(row => row.compliance_status === "Compliant").length;
    const non_compliant = data.filter(row => row.compliance_status === "Non-Compliant").length;
    const expired = data.filter(row => row.compliance_status === "Expired").length;
    const expiring_soon = data.filter(row => row.days_to_expiry && row.days_to_expiry <= 30 && row.days_to_expiry > 0).length;

    return [
        ["Metric", "Count", "Percentage"],
        ["Total Products", total, "100%"],
        ["Compliant", compliant, `${(compliant/total*100).toFixed(1)}%`],
        ["Non-Compliant", non_compliant, `${(non_compliant/total*100).toFixed(1)}%`],
        ["Expired", expired, `${(expired/total*100).toFixed(1)}%`],
        ["Expiring Soon", expiring_soon, `${(expiring_soon/total*100).toFixed(1)}%`]
    ];
}

function convert_to_csv(data) {
    return data.map(row => row.join(",")).join("\n");
}

function download_csv(csv_data, filename) {
    const blob = new Blob([csv_data], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", filename);
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}
