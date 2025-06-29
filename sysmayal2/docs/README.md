<<<<<<< HEAD
# Sysmayal - Global Distribution & R&D Management

A comprehensive Frappe application for managing aloe vera product distribution, regulatory compliance, and research & development activities across global markets.

## Overview

Sysmayal is designed specifically for companies in the aloe vera industry who need to manage complex global distribution networks while maintaining strict regulatory compliance across different markets. The application provides tools for distributor management, regulatory tracking, R&D project coordination, and bulk data import capabilities.

## Features

### 🌍 Global Distribution Management
- **Distribution Organizations**: Comprehensive organization profiles with hierarchy support
- **Contact Management**: Enhanced contact tracking with regulatory roles and responsibilities
- **Territory Management**: Geographic distribution territory assignment and tracking
- **Multi-language Support**: Interface and data entry in multiple languages

### 📋 Regulatory Compliance
- **Country Regulations**: Database of country-specific aloe vera product regulations
- **Product Compliance**: Track compliance status by product and market
- **Certification Management**: Document storage and expiry tracking
- **Automated Alerts**: Renewal notifications and compliance deadlines

### 🔬 R&D Management
- **Product Development**: New product introduction workflow
- **Research Projects**: R&D project tracking with milestones and deliverables
- **Testing Results**: Laboratory testing data management
- **Market Research**: Competitive analysis and market intelligence

### 📊 Data Management
- **Bulk Import Tools**: CSV/Excel import for contacts, addresses, and organizations
- **Data Validation**: Comprehensive error checking and duplicate detection
- **Backup & Recovery**: Data export and rollback capabilities
- **Integration**: Seamless integration with ERPNext CRM and sales modules

### 📈 Analytics & Reporting
- **Compliance Status Report**: Comprehensive overview of product compliance across all markets
- **Distribution Analytics**: Network performance metrics and geographic coverage analysis
- **R&D Project Status**: Portfolio tracking with timeline analysis and risk assessment
- **Interactive Dashboards**: Real-time metrics and key performance indicators
- **Custom Analytics**: Advanced filtering and drill-down capabilities with export functionality

### ⚙️ Workflow Management
- **R&D Project Approval**: Multi-stage approval workflow for research projects with budget controls
- **Product Compliance Review**: Automated compliance review process with testing and regulatory submission stages
- **Market Entry Plan Approval**: Strategic approval workflow with market analysis and regulatory review phases
- **Automated Notifications**: Email alerts for workflow actions and approvals
- **Role-based Workflow**: Different approval paths based on user roles and project criteria

### 🎨 Enhanced User Interface
- **Custom Form Layouts**: Tailored forms with intelligent field grouping and conditional logic
- **Interactive List Views**: Color-coded status indicators, progress bars, and bulk action capabilities
- **Smart Buttons**: Context-sensitive action buttons for creating related documents and reports
- **Dashboard Indicators**: Real-time status indicators for compliance, risks, and deadlines
- **Mobile Responsive**: Optimized interface for mobile and tablet devices

## Installation

### Prerequisites
- Frappe Framework (v13+)
- ERPNext (v13+)
- Python 3.7+
- MariaDB 10.3+

### Install via bench

```bash
# Navigate to your frappe-bench directory
cd /path/to/frappe-bench

# Get the app
bench get-app https://github.com/your-repo/sysmayal.git

# Install on your site
bench --site your-site.com install-app sysmayal

# Migrate the database
bench --site your-site.com migrate
```

### Manual Installation

1. Copy the app to your apps directory:
   ```bash
   cp -r sysmayal /path/to/frappe-bench/apps/
   ```

2. Install the app:
   ```bash
   bench --site your-site.com install-app sysmayal
   ```

3. Run migrations:
   ```bash
   bench --site your-site.com migrate
   ```

## Configuration

### Initial Setup

1. **User Roles**: Configure user roles for different access levels:
   - Distribution Manager
   - R&D Manager
   - Compliance Officer
   - Data Entry Operator

2. **Country Regulations**: Import regulatory data using the provided fixtures:
   ```bash
   bench --site your-site.com execute sysmayal.setup.install.setup_country_regulations
   ```

3. **Import Templates**: Download CSV templates for bulk data import from:
   - Distribution Organizations
   - Distribution Contacts
   - Product Compliance data

### Data Import

The app includes comprehensive data import tools:

1. **Contact Import**: Bulk import distributor contacts with validation
2. **Organization Import**: Import organizational hierarchy and relationships
3. **Address Import**: Batch address import with geocoding support
4. **Compliance Data**: Import existing compliance and certification data

## Usage

### Managing Distributors

1. Navigate to **Sysmayal > Distribution > Distribution Organization**
2. Create new organization profiles with:
   - Basic company information
   - Primary contact details
   - Regulatory status by country
   - Distribution territories

### Tracking Compliance

1. Go to **Sysmayal > Compliance > Country Regulation**
2. View country-specific requirements
3. Track product compliance status
4. Manage certification documents and renewals

### R&D Projects

1. Access **Sysmayal > R&D > Product Development Project**
2. Create project timelines and milestones
3. Track testing phases and results
4. Monitor regulatory approval progress

### Analytics & Reports

1. **Compliance Status Report**: Monitor product compliance across all markets
   - Risk level assessment and timeline tracking
   - Automated alerts for expiring certifications
   - Bulk status updates and compliance actions

2. **Distribution Analytics**: Analyze network performance
   - Geographic coverage and market penetration
   - Partner performance metrics and growth analysis
   - Contact analytics and communication preferences

3. **R&D Project Status**: Track research and development portfolio
   - Project timeline and milestone tracking
   - Investment analysis and resource allocation
   - Risk assessment and performance metrics

## API Integration

Sysmayal provides REST API endpoints for:

- Contact and organization management
- Compliance status updates
- R&D project tracking
- Document management

Example API usage:
```python
import requests

# Get organization compliance status
response = requests.get(
    "https://your-site.com/api/resource/Distribution Organization/ORG-00001",
    headers={"Authorization": "token your-api-key:your-api-secret"}
)
```

## Customization

### Custom Fields

Add custom fields to DocTypes through the Frappe interface:

1. Go to **Setup > Customize Form**
2. Select the DocType (e.g., Distribution Organization)
3. Add custom fields as needed

### Custom Scripts

Client and server scripts can be added for business logic:

```javascript
// Client Script Example - Distribution Organization
frappe.ui.form.on('Distribution Organization', {
    country: function(frm) {
        // Auto-load country-specific regulations
        if (frm.doc.country) {
            frm.call('get_country_regulations');
        }
    }
});
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Check data format and required fields
2. **Permission Issues**: Verify user roles and permissions
3. **API Errors**: Validate API credentials and endpoints

### Support

For technical support:
- Review the documentation in the `docs/` directory
- Check the issue tracker for known problems
- Contact the development team

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release with core functionality
- Distribution organization management
- Basic compliance tracking
- R&D project management
- Data import tools

### Version 1.1.0 (Planned)
- Enhanced reporting capabilities
- Mobile app integration
- Advanced analytics dashboard
- Multi-company support

---

**Sysmayal** - Empowering global aloe vera distribution through intelligent management systems.
#   s y s m a y a l 6  
 #   s y s m a y a l 6  
 #   s y s m a y a l 6  
 
=======
# sysmayal4
>>>>>>> 8f4aa4e1514ecd0590d976f86a6862d2e9b557f0
