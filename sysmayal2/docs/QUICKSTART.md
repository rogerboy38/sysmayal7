# Sysmayal - Quick Start Guide

## Overview

**Sysmayal** is a comprehensive Frappe application for managing global aloe vera distribution networks, regulatory compliance, and R&D operations. This app provides everything you need to manage complex international distribution relationships while maintaining strict regulatory compliance.

## Key Features

✅ **Distribution Organization Management** - Comprehensive organization profiles with hierarchy support  
✅ **Contact Management** - Enhanced contact tracking with regulatory roles  
✅ **Regulatory Compliance** - Country-specific requirements and certification tracking  
✅ **R&D Project Management** - Product development and research project coordination  
✅ **Bulk Data Import** - CSV/Excel import tools with validation and error handling  
✅ **Integration** - Seamless ERPNext CRM and sales module integration  
✅ **Multi-language Support** - Global distribution network support  

## Quick Installation

### Prerequisites
- Frappe Framework v13+
- ERPNext v13+ (recommended)
- Python 3.7+
- Administrator access to your Frappe bench

### Install Steps

```bash
# 1. Navigate to your frappe-bench
cd /path/to/frappe-bench

# 2. Copy the sysmayal app to apps directory
cp -r /path/to/sysmayal ./apps/

# 3. Install the app
bench --site your-site.com install-app sysmayal

# 4. Run migrations
bench --site your-site.com migrate

# 5. Restart services (if needed)
bench restart
```

### Verify Installation

1. Login to your ERPNext instance
2. Look for the **Sysmayal** module on the main desk
3. Navigate to **Sysmayal > Distribution > Distribution Organization**
4. Verify the module loaded correctly

## Quick Setup

### 1. Import Demo Data (Optional)

```bash
bench --site your-site.com execute sysmayal.scripts.demo_setup.setup_demo_data
```

### 2. Configure User Roles

Go to **Setup > Users and Permissions > Role** and assign these roles:
- **Distribution Manager** - Full distribution management access
- **R&D Manager** - Complete R&D project management  
- **Compliance Officer** - Regulatory compliance and certification management
- **Data Entry Operator** - Limited data entry permissions

### 3. Import Your Data

Use the bulk import tools:

**Organizations:**
1. Go to **Sysmayal > Tools > Import Organizations**
2. Download template: `/templates/distribution_organization_template.csv`
3. Prepare your data and upload

**Contacts:**
1. Go to **Sysmayal > Tools > Import Contacts** 
2. Download template: `/templates/distribution_contact_template.csv`
3. Ensure organization names match existing records

### 4. Configure Country Regulations

The app includes regulatory data for major markets (US, Canada, Australia). Additional countries can be added manually or imported from JSON files.

## App Structure

### Core DocTypes

| DocType | Purpose | Key Features |
|---------|---------|--------------|
| **Distribution Organization** | Organization management | Hierarchy, compliance tracking, ERPNext integration |
| **Distribution Contact** | Contact management | Regulatory roles, communication preferences |
| **Country Regulation** | Regulatory requirements | Country-specific rules, certification requirements |
| **Product Development Project** | R&D management | Project tracking, team management, compliance planning |

### Integration Points

- **Customer/Supplier**: Automatic ERPNext record creation
- **Contact**: Bidirectional contact synchronization  
- **Territory**: Geographic distribution management
- **Communication**: Full communication tracking

### Data Import Tools

- **Bulk Organization Import** - CSV/Excel with field mapping
- **Bulk Contact Import** - Validation and duplicate handling
- **Regulatory Data Import** - JSON format for complex regulatory data
- **Address Import** - Geographic and compliance data

## Key Workflows

### 1. Distribution Partner Onboarding

1. Create **Distribution Organization** record
2. Add **Distribution Contacts** with regulatory roles
3. Set up compliance requirements by country
4. Generate ERPNext Customer/Supplier records automatically
5. Track agreements and certification status

### 2. R&D Project Management

1. Create **Product Development Project**
2. Assign project team and responsibilities  
3. Define regulatory strategy and target markets
4. Track progress through development phases
5. Monitor compliance requirements and certifications

### 3. Regulatory Compliance

1. Maintain **Country Regulation** database
2. Track product compliance by market
3. Monitor certification expiry dates
4. Generate compliance reports and alerts
5. Coordinate regulatory submissions

## Sample Data

The app includes sample data demonstrating:
- **3 Distribution Organizations** across different countries and types
- **Multiple contacts** with various regulatory roles
- **2 R&D Projects** in different development phases  
- **Regulatory data** for US, Canada, and Australia

## Advanced Features

### Bulk Operations
- Mass status updates for contacts and organizations
- Bulk data export for compliance reporting
- Batch processing for large datasets

### Reporting & Analytics
- Distribution network analysis
- Compliance status dashboards
- R&D project portfolio management
- Regulatory requirement tracking

### Customization
- Custom fields for organization-specific data
- Configurable workflows and approval processes
- Custom reports and dashboards
- API integration capabilities

## Support & Documentation

### Documentation
- **Installation Guide**: `/docs/INSTALLATION.md`
- **User Guide**: `/docs/USER_GUIDE.md`
- **API Documentation**: Available in ERPNext API explorer

### Import Templates
- **Organizations**: `/templates/distribution_organization_template.csv`
- **Contacts**: `/templates/distribution_contact_template.csv`

### Demo Setup
- **Demo Data Script**: `/scripts/demo_setup.py`
- **Sample Fixtures**: `/sysmayal/fixtures/`

## Technical Specifications

### System Requirements
- **Frappe Framework**: 13.0+
- **ERPNext**: 13.0+ (optional but recommended)
- **Python**: 3.7+
- **Database**: MariaDB 10.3+
- **Memory**: 4GB+ recommended
- **Storage**: 1GB+ for app and data

### Performance
- **Scalability**: Supports thousands of organizations and contacts
- **Concurrency**: Multi-user concurrent access
- **Data Volume**: Optimized for large regulatory datasets
- **Response Time**: Sub-second response for most operations

### Security
- **Role-based Access Control**: Granular permissions by user role
- **Data Protection**: GDPR compliance features included
- **Audit Trail**: Complete change tracking and history
- **API Security**: Standard Frappe authentication and authorization

## Next Steps

1. **Complete Installation** using the steps above
2. **Import Your Data** using the provided templates
3. **Configure User Access** and assign appropriate roles
4. **Customize** fields and workflows for your specific needs
5. **Train Users** on the new system capabilities
6. **Monitor Performance** and optimize as needed

## Getting Help

- **GitHub Repository**: Issues and feature requests
- **Documentation**: Comprehensive guides in `/docs/`
- **Community Support**: Frappe community forums
- **Professional Support**: Available from the development team

---

**Sysmayal** - Empowering global aloe vera distribution through intelligent management systems.

*Version 1.0.0 | Compatible with Frappe v13+ and ERPNext v13+*
