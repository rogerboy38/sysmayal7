/**
 * Sysmayal Dashboard - Main Dashboard Page
 * 
 * Comprehensive dashboard showing key metrics and analytics for:
 * - Distribution organizations and contacts
 * - Product compliance status
 * - R&D project progress
 * - Market entry plans
 * - Certification documents
 */

frappe.pages['sysmayal-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Sysmayal Dashboard',
        single_column: true
    });

    // Add refresh button
    page.add_inner_button(__('Refresh'), function() {
        page.dashboard.refresh();
    });

    // Add export button
    page.add_inner_button(__('Export Report'), function() {
        page.dashboard.export_dashboard_data();
    });

    // Initialize dashboard
    page.dashboard = new SysmayalDashboard(page);
};

class SysmayalDashboard {
    constructor(page) {
        this.page = page;
        this.container = $(page.body);
        this.charts = {};
        this.init();
    }

    init() {
        this.render_dashboard_structure();
        this.load_dashboard_data();
    }

    render_dashboard_structure() {
        this.container.html(`
            <div class="dashboard-container">
                <!-- Key Metrics Row -->
                <div class="row dashboard-section">
                    <div class="col-sm-12">
                        <h4>Key Metrics Overview</h4>
                    </div>
                    <div class="col-sm-3">
                        <div class="dashboard-card" id="organizations-card">
                            <div class="card-header">Organizations</div>
                            <div class="card-value" id="organizations-count">--</div>
                            <div class="card-subtitle">Distribution Partners</div>
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="dashboard-card" id="contacts-card">
                            <div class="card-header">Contacts</div>
                            <div class="card-value" id="contacts-count">--</div>
                            <div class="card-subtitle">Active Contacts</div>
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="dashboard-card" id="compliance-card">
                            <div class="card-header">Compliance</div>
                            <div class="card-value" id="compliance-rate">--%</div>
                            <div class="card-subtitle">Products Compliant</div>
                        </div>
                    </div>
                    <div class="col-sm-3">
                        <div class="dashboard-card" id="projects-card">
                            <div class="card-header">R&D Projects</div>
                            <div class="card-value" id="projects-count">--</div>
                            <div class="card-subtitle">Active Projects</div>
                        </div>
                    </div>
                </div>

                <!-- Charts Row -->
                <div class="row dashboard-section">
                    <div class="col-sm-6">
                        <div class="dashboard-chart-container">
                            <h5>Distribution by Country</h5>
                            <div id="country-distribution-chart"></div>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="dashboard-chart-container">
                            <h5>Compliance Status Distribution</h5>
                            <div id="compliance-status-chart"></div>
                        </div>
                    </div>
                </div>

                <!-- Progress and Alerts Row -->
                <div class="row dashboard-section">
                    <div class="col-sm-6">
                        <div class="dashboard-table-container">
                            <h5>R&D Project Progress</h5>
                            <div id="project-progress-table"></div>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="dashboard-alerts-container">
                            <h5>Recent Alerts</h5>
                            <div id="alerts-list"></div>
                        </div>
                    </div>
                </div>

                <!-- Expiring Certificates and Market Plans -->
                <div class="row dashboard-section">
                    <div class="col-sm-6">
                        <div class="dashboard-table-container">
                            <h5>Expiring Certificates</h5>
                            <div id="expiring-certificates"></div>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="dashboard-table-container">
                            <h5>Market Entry Plans</h5>
                            <div id="market-plans-summary"></div>
                        </div>
                    </div>
                </div>
            </div>
        `);

        // Add CSS styles
        this.add_dashboard_styles();
    }

    add_dashboard_styles() {
        if (!$('#sysmayal-dashboard-styles').length) {
            $('<style id="sysmayal-dashboard-styles">').appendTo('head').text(`
                .dashboard-container {
                    padding: 20px;
                }
                
                .dashboard-section {
                    margin-bottom: 30px;
                }
                
                .dashboard-card {
                    background: #fff;
                    border: 1px solid #d1d8dd;
                    border-radius: 6px;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 15px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    transition: transform 0.2s;
                }
                
                .dashboard-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                }
                
                .card-header {
                    font-size: 14px;
                    color: #8D99A6;
                    font-weight: 500;
                    margin-bottom: 10px;
                }
                
                .card-value {
                    font-size: 32px;
                    font-weight: bold;
                    color: #36414C;
                    margin-bottom: 5px;
                }
                
                .card-subtitle {
                    font-size: 12px;
                    color: #8D99A6;
                }
                
                .dashboard-chart-container,
                .dashboard-table-container,
                .dashboard-alerts-container {
                    background: #fff;
                    border: 1px solid #d1d8dd;
                    border-radius: 6px;
                    padding: 20px;
                    margin-bottom: 15px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }
                
                .alert-item {
                    padding: 10px;
                    margin-bottom: 10px;
                    border-left: 4px solid #ffa00a;
                    background: #fff8e1;
                    border-radius: 4px;
                }
                
                .alert-item.critical {
                    border-left-color: #ff5858;
                    background: #ffebee;
                }
                
                .alert-item.info {
                    border-left-color: #2e7d32;
                    background: #e8f5e8;
                }
                
                .progress-bar-container {
                    width: 100%;
                    height: 8px;
                    background: #f5f5f5;
                    border-radius: 4px;
                    overflow: hidden;
                    margin: 5px 0;
                }
                
                .progress-bar {
                    height: 100%;
                    border-radius: 4px;
                    transition: width 0.3s ease;
                }
                
                .progress-low { background-color: #ff5858; }
                .progress-medium { background-color: #ffa00a; }
                .progress-high { background-color: #2e7d32; }
            `);
        }
    }

    async load_dashboard_data() {
        try {
            // Load all dashboard data in parallel
            const [
                organizationsData,
                contactsData, 
                complianceData,
                projectsData,
                certificatesData,
                marketPlansData
            ] = await Promise.all([
                this.get_organizations_data(),
                this.get_contacts_data(),
                this.get_compliance_data(),
                this.get_projects_data(),
                this.get_certificates_data(),
                this.get_market_plans_data()
            ]);

            // Update dashboard components
            this.update_key_metrics(organizationsData, contactsData, complianceData, projectsData);
            this.render_charts(organizationsData, complianceData);
            this.render_project_progress(projectsData);
            this.render_alerts(complianceData, certificatesData, projectsData);
            this.render_expiring_certificates(certificatesData);
            this.render_market_plans(marketPlansData);

        } catch (error) {
            console.error('Dashboard data loading error:', error);
            frappe.msgprint(__('Error loading dashboard data. Please refresh the page.'));
        }
    }

    async get_organizations_data() {
        return await frappe.call({
            method: 'frappe.client.get_count',
            args: {
                doctype: 'Distribution Organization',
                filters: {status: 'Active'}
            }
        });
    }

    async get_contacts_data() {
        return await frappe.call({
            method: 'frappe.client.get_count',
            args: {
                doctype: 'Distribution Contact',
                filters: {status: 'Active'}
            }
        });
    }

    async get_compliance_data() {
        return await frappe.call({
            method: 'doctype.product_compliance.product_compliance.get_compliance_dashboard_data',
            args: {}
        });
    }
        return await frappe.call({
            method: 'doctype.product_compliance.product_compliance.get_compliance_dashboard_data'
        });
    }

    async get_projects_data() {
        return await frappe.call({
            method: 'product_development_project.product_development_project.get_project_dashboard_data'
        });
    }

    async get_certificates_data() {
        return await frappe.call({
            method: 'doctype.certification_document.certification_document.get_certificate_dashboard_data'
        });
    }

    async get_market_plans_data() {
        return await frappe.call({
            method: 'sysmayal.doctype.market_entry_plan.market_entry_plan.get_market_entry_dashboard'
        });
    }

    update_key_metrics(orgs, contacts, compliance, projects) {
        // Update organization count
        $('#organizations-count').text(orgs.message || 0);
        
        // Update contacts count
        $('#contacts-count').text(contacts.message || 0);
        
        // Calculate compliance rate
        const complianceData = compliance.message;
        if (complianceData && complianceData.status_distribution) {
            const total = complianceData.status_distribution.reduce((sum, item) => sum + item.count, 0);
            const compliant = complianceData.status_distribution.find(item => item.compliance_status === 'Compliant');
            const rate = total > 0 ? Math.round((compliant?.count || 0) / total * 100) : 0;
            $('#compliance-rate').text(rate + '%');
        }
        
        // Update projects count  
        const projectsData = projects.message;
        if (projectsData && projectsData.status_summary) {
            const activeProjects = projectsData.status_summary
                .filter(item => ['In Progress', 'Testing', 'Regulatory Review'].includes(item.status))
                .reduce((sum, item) => sum + item.count, 0);
            $('#projects-count').text(activeProjects);
        }
    }

    render_charts(orgsData, complianceData) {
        // Country distribution chart would go here
        // In a full implementation, this would use Chart.js or similar
        $('#country-distribution-chart').html('<div class="text-muted text-center">Chart visualization would be rendered here</div>');
        
        // Compliance status chart
        $('#compliance-status-chart').html('<div class="text-muted text-center">Compliance status chart would be rendered here</div>');
    }

    render_project_progress(projectsData) {
        const data = projectsData.message;
        if (!data) return;

        let html = '<table class="table table-bordered"><thead><tr><th>Project</th><th>Progress</th><th>Status</th></tr></thead><tbody>';
        
        // This would be populated with actual project data
        html += '<tr><td colspan="3" class="text-muted text-center">Project progress data would be displayed here</td></tr>';
        
        html += '</tbody></table>';
        $('#project-progress-table').html(html);
    }

    render_alerts(complianceData, certificatesData, projectsData) {
        const alerts = [];
        
        // Add compliance alerts
        const compliance = complianceData.message;
        if (compliance && compliance.expiring_products) {
            compliance.expiring_products.forEach(product => {
                alerts.push({
                    type: 'critical',
                    message: `Product ${product.product_name} expires in ${product.days_to_expiry} days`,
                    date: product.expiry_date
                });
            });
        }
        
        // Add certificate alerts
        const certificates = certificatesData.message;
        if (certificates && certificates.expiry_forecast) {
            // Add alerts for certificates expiring soon
            alerts.push({
                type: 'warning',
                message: 'Certificate renewals due this month',
                date: frappe.datetime.get_today()
            });
        }
        
        // Render alerts
        let html = '';
        if (alerts.length === 0) {
            html = '<div class="text-muted text-center">No active alerts</div>';
        } else {
            alerts.forEach(alert => {
                html += `<div class="alert-item ${alert.type}">
                    <div style="font-weight: 500;">${alert.message}</div>
                    <div style="font-size: 12px; color: #666;">${alert.date}</div>
                </div>`;
            });
        }
        
        $('#alerts-list').html(html);
    }

    render_expiring_certificates(certificatesData) {
        let html = '<table class="table table-bordered"><thead><tr><th>Certificate</th><th>Expiry Date</th><th>Days Left</th></tr></thead><tbody>';
        
        // This would be populated with actual expiring certificates
        html += '<tr><td colspan="3" class="text-muted text-center">Expiring certificates would be listed here</td></tr>';
        
        html += '</tbody></table>';
        $('#expiring-certificates').html(html);
    }

    render_market_plans(marketPlansData) {
        let html = '<table class="table table-bordered"><thead><tr><th>Country</th><th>Status</th><th>Progress</th></tr></thead><tbody>';
        
        // This would be populated with actual market entry plans
        html += '<tr><td colspan="3" class="text-muted text-center">Market entry plans would be displayed here</td></tr>';
        
        html += '</tbody></table>';
        $('#market-plans-summary').html(html);
    }

    refresh() {
        this.load_dashboard_data();
        frappe.show_alert(__('Dashboard refreshed'), 2);
    }

    export_dashboard_data() {
        // Export dashboard data to Excel/CSV
        frappe.msgprint(__('Export functionality would be implemented here'));
    }
}
