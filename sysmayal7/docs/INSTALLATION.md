# Sysmayal Installation Guide

This guide provides step-by-step instructions for installing and configuring the Sysmayal app on your ERPNext/Frappe system.

## Prerequisites

Before installing Sysmayal, ensure you have:

- **Frappe Framework**: Version 13.0 or higher
- **ERPNext**: Version 13.0 or higher (recommended)
- **Python**: Version 3.7 or higher
- **MariaDB**: Version 10.3 or higher
- **System Access**: Administrator privileges on your Frappe bench

## Installation Methods

### Method 1: Production Installation (Recommended)

#### Step 1: Download the App

```bash
# Navigate to your frappe-bench directory
cd /path/to/your/frappe-bench

# Get the Sysmayal app
bench get-app https://github.com/your-org/sysmayal.git
```

#### Step 2: Install on Site

```bash
# Install the app on your site
bench --site your-site.com install-app sysmayal

# Run database migrations
bench --site your-site.com migrate
```

#### Step 3: Set Permissions

```bash
# Set proper permissions
bench setup supervisor
bench setup nginx

# Restart services
sudo supervisorctl restart all
```

### Method 2: Development Installation

#### Step 1: Clone Repository

```bash
# Navigate to apps directory
cd /path/to/frappe-bench/apps

# Clone the repository
git clone https://github.com/your-org/sysmayal.git
cd sysmayal

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Install for Development

```bash
# Navigate back to bench directory
cd /path/to/frappe-bench

# Install app in development mode
bench --site your-site.com install-app sysmayal

# Start development server
bench start
```

### Method 3: Manual Installation

#### Step 1: Copy Files

```bash
# Copy the sysmayal directory to your apps folder
cp -r sysmayal /path/to/frappe-bench/apps/

# Navigate to bench directory
cd /path/to/frappe-bench
```

#### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r apps/sysmayal/requirements.txt
```

#### Step 3: Install App

```bash
# Install the app
bench --site your-site.com install-app sysmayal

# Migrate database
bench --site your-site.com migrate
```

## Post-Installation Configuration

### Step 1: Verify Installation

```bash
# Check if app is installed
bench --site your-site.com list-apps

# Verify app status
bench --site your-site.com console
```

In the Frappe console:
```python
import frappe
print(frappe.get_installed_apps())
```

### Step 2: Initial Setup

1. **Access ERPNext**: Login to your ERPNext instance
2. **Navigate to Sysmayal**: Go to the Sysmayal module from the desk
3. **Setup User Roles**: Configure user permissions

#### Configure User Roles

```bash
# Run setup script
bench --site your-site.com execute sysmayal.setup.install.after_install
```

Or manually in ERPNext:

1. Go to **Setup > Users and Permissions > Role**
2. Create/verify these roles exist:
   - Distribution Manager
   - R&D Manager
   - Compliance Officer
   - Data Entry Operator

### Step 3: Import Initial Data

#### Import Country Regulations

The app includes regulatory data for major markets:

```bash
# Import country regulation fixtures
bench --site your-site.com execute sysmayal.setup.install.setup_country_regulations
```

#### Import Your Data

1. **Organizations**: Use the bulk import tool for distribution organizations
2. **Contacts**: Import your contact database
3. **Addresses**: Upload address information

## Configuration Options

### Custom Field Setup

The app automatically adds custom fields to existing ERPNext DocTypes:

- **Customer**: Territory Manager, Regulatory Status
- **Supplier**: Compliance Status
- **Contact**: Regulatory Role

### Email Configuration

Configure email templates for:
- Welcome notifications
- Compliance alerts
- Project updates

```bash
# Copy email templates
bench --site your-site.com migrate
```

### Permission Configuration

Set up role-based permissions:

1. **Distribution Manager**: Full access to distribution modules
2. **R&D Manager**: Full access to R&D projects
3. **Compliance Officer**: Read/write access to compliance data
4. **Data Entry Operator**: Limited create/edit permissions

### System Settings

Configure system-wide settings:

1. Go to **Sysmayal > Settings > Sysmayal Settings**
2. Set default values for:
   - Default currency
   - Default territory
   - Email notifications
   - Compliance check frequency

## Troubleshooting

### Common Installation Issues

#### Issue: App Installation Fails

**Solution:**
```bash
# Check bench logs
bench --site your-site.com console

# Verify dependencies
pip install -r apps/sysmayal/requirements.txt

# Retry installation
bench --site your-site.com install-app sysmayal --force
```

#### Issue: Database Migration Errors

**Solution:**
```bash
# Check migration status
bench --site your-site.com show-pending-migrations

# Run specific migration
bench --site your-site.com migrate --skip-failing

# Check error logs
tail -f logs/bench.log
```

#### Issue: Permission Denied Errors

**Solution:**
```bash
# Set proper ownership
sudo chown -R [user]:[group] /path/to/frappe-bench

# Set proper permissions
chmod -R 755 /path/to/frappe-bench
```

#### Issue: Import Data Fails

**Solution:**
1. Check file format (CSV/Excel)
2. Verify column mapping
3. Check for required fields
4. Review error logs in import results

### Getting Help

#### Log Files

Check these log files for troubleshooting:
- `logs/bench.log`: General bench operations
- `logs/error.log`: Application errors
- `logs/worker.log`: Background job errors

#### Console Commands

Useful commands for troubleshooting:
```bash
# Check app status
bench --site your-site.com list-apps

# Verify DocTypes
bench --site your-site.com console
frappe.get_all("DocType", filters={"module": "Sysmayal"})

# Check permissions
frappe.get_all("Role", filters={"name": ["like", "%Distribution%"]})
```

#### Support Resources

- **Documentation**: See the `/docs` directory
- **GitHub Issues**: Report bugs and feature requests
- **Community Forum**: Ask questions and get help
- **Email Support**: Contact the development team

## Security Considerations

### Data Protection

- Enable encryption for sensitive data
- Configure proper backup procedures
- Set up audit trails for compliance

### Access Control

- Use strong passwords
- Enable two-factor authentication
- Regularly review user permissions
- Implement IP restrictions if needed

### Compliance

- Configure GDPR compliance features
- Set up data retention policies
- Enable audit logging
- Regular security updates

## Performance Optimization

### Database Optimization

```bash
# Optimize database
bench --site your-site.com execute frappe.utils.bench_helper.optimize_database

# Update schema
bench --site your-site.com migrate
```

### Caching

Enable Redis caching for better performance:
```bash
# Configure Redis
bench setup redis-server
```

### Background Jobs

Set up proper background job processing:
```bash
# Start background workers
bench worker --queue short,default,long
```

## Backup and Recovery

### Regular Backups

```bash
# Create database backup
bench --site your-site.com backup --with-files

# Automated backup setup
crontab -e
# Add: 0 2 * * * /path/to/frappe-bench/env/bin/bench --site your-site.com backup --with-files
```

### Recovery Process

```bash
# Restore from backup
bench --site your-site.com restore /path/to/backup.sql.gz --with-public-files /path/to/files-backup.tar.gz
```

## Next Steps

After successful installation:

1. **User Training**: Train your team on the new system
2. **Data Migration**: Import your existing data
3. **Customization**: Configure workflows and reports
4. **Integration**: Set up API integrations if needed
5. **Monitoring**: Implement system monitoring and alerts

## Version Compatibility

| Sysmayal Version | Frappe Version | ERPNext Version | Python Version |
|------------------|----------------|-----------------|----------------|
| 1.0.x            | 13.x           | 13.x            | 3.7+           |
| 1.1.x (planned) | 14.x           | 14.x            | 3.8+           |

## License

This software is licensed under the MIT License. See the LICENSE file for details.

---

For additional support, please contact the Sysmayal development team or refer to the comprehensive user documentation.
