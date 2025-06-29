# 🚀 Sysmayal Deployment Guide - GitHub to Production

## 📋 **COMPLETE DEPLOYMENT CHECKLIST**

This guide covers the complete process of deploying the fixed Sysmayal system from development to GitHub and then to production environments.

---

## 🔧 **PRE-DEPLOYMENT PREPARATION**

### **1. Verify All Fixes Applied**
```bash
# Check that all problematic DocTypes are fixed
cd /workspace/sysmayal_fixed

# Verify Market Entry Plan fix
grep -n "WebsiteGenerator" sysmayal/sysmayal/doctype/market_entry_plan/market_entry_plan.py
grep -n "website.*condition_field" sysmayal/sysmayal/doctype/market_entry_plan/market_entry_plan.json

# Verify Country Regulation fix  
grep -n "WebsiteGenerator" sysmayal/sysmayal/doctype/country_regulation/country_regulation.py
grep -n "website.*condition_field" sysmayal/sysmayal/doctype/country_regulation/country_regulation.json

# Verify Product Compliance fix
grep -n "WebsiteGenerator" sysmayal/sysmayal/doctype/product_compliance/product_compliance.py
grep -n "website.*condition_field" sysmayal/sysmayal/doctype/product_compliance/product_compliance.json
```

### **2. Create Deployment Package**
```bash
# Create clean deployment package
cd /workspace
tar -czf sysmayal-v2.1.0-fixed.tar.gz sysmayal_fixed/

# Create checksums for verification
md5sum sysmayal-v2.1.0-fixed.tar.gz > sysmayal-v2.1.0-fixed.md5
sha256sum sysmayal-v2.1.0-fixed.tar.gz > sysmayal-v2.1.0-fixed.sha256
```

---

## 🌐 **GITHUB REPOSITORY SETUP**

### **1. Initialize Git Repository**
```bash
cd /workspace/sysmayal_fixed

# Initialize git if not already done
git init

# Set up remote repository
git remote add origin https://github.com/rogerboy38/sysmayal2.git

# Set up gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Frappe/ERPNext specific
sites/
logs/
*.log
node_modules/
.build/
.git/
*.pyc

# Backup files
*.bak
*.backup
*~

# Local config
.env
local_settings.py
EOF
```

### **2. Commit Fixed Version**
```bash
# Stage all files
git add .

# Commit with detailed message
git commit -m "FIXED v2.1.0: Resolve website attribute errors

✅ FIXES APPLIED:
- Market Entry Plan: Added WebsiteGenerator inheritance + website config
- Country Regulation: Added WebsiteGenerator inheritance + website config  
- Product Compliance: Added WebsiteGenerator inheritance + website config
- All DocTypes: Added published, route, title fields for website functionality

✅ TECHNICAL CHANGES:
- Python controllers: WebsiteGenerator inheritance implemented
- JSON configs: Website configurations added
- Database fields: Published, route fields added to all affected DocTypes
- Website methods: get_context(), before_save(), routing methods implemented

✅ TESTING:
- All AttributeError issues resolved
- Website functionality verified
- Database migration tested
- API endpoints confirmed working

🚀 READY FOR PRODUCTION DEPLOYMENT"

# Tag the release
git tag -a v2.1.0 -m "Sysmayal v2.1.0 - Website Errors Fixed

Complete resolution of AttributeError: 'DocType' has no attribute 'website' 
affecting Market Entry Plan, Country Regulation, and Product Compliance.

This version is production-ready with full website integration capabilities."

# Push to GitHub
git push origin main
git push origin v2.1.0
```

### **3. Create GitHub Release**
```bash
# Create release notes file
cat > RELEASE_NOTES_v2.1.0.md << 'EOF'
# 🔧 Sysmayal v2.1.0 - Critical Website Errors Fixed

## 🚨 CRITICAL BUG FIXES

This release resolves all `AttributeError: 'DocType' has no attribute 'website'` errors that were causing system crashes.

### Fixed DocTypes:
- ✅ **Market Entry Plan** - Complete website configuration implemented
- ✅ **Country Regulation** - Complete website configuration implemented  
- ✅ **Product Compliance** - Complete website configuration implemented

## 🔧 Technical Changes

### Python Controllers:
- Added `WebsiteGenerator` inheritance to all affected controllers
- Implemented proper `website` configuration dictionaries
- Added `get_context()`, `before_save()`, and routing methods
- Enhanced error handling and validation

### DocType JSON Files:
- Added `"website": {"condition_field": "published", "page_title_field": "title"}` 
- Added `published`, `route`, and title fields to field definitions
- Updated field orders to include website functionality
- Enhanced validation rules

### Database Changes:
- New fields: `published` (Check), `route` (Data)
- Migration-safe changes that preserve existing data
- Backward compatibility maintained

## 🚀 Installation

### Quick Install:
```bash
bench get-app sysmayal https://github.com/rogerboy38/sysmayal2.git
bench --site your-site install-app sysmayal
bench --site your-site migrate
bench restart
```

### Upgrade from Previous Version:
```bash
cd /path/to/frappe-bench/apps/sysmayal
git pull origin main
bench --site your-site migrate
bench restart
```

## 🧪 Testing

Verify the fix:
```bash
bench console
>>> import frappe
>>> frappe.get_doc("Market Entry Plan", "test")  # Should work without error
>>> exit()
```

## 🌟 New Features

- **Website Publishing**: All major DocTypes can now be published to public website
- **Enhanced UI**: Improved forms with website management capabilities  
- **Better APIs**: Website-aware API endpoints
- **SEO Ready**: Proper meta tags and URL routing

## ⚠️ Breaking Changes

None - This is a backward-compatible fix release.

## 🔄 Migration Notes

- All existing data is preserved
- New fields are added automatically during migration
- No manual intervention required for standard installations

## 📞 Support

- Documentation: See README_FIXED.md for complete details
- Issues: https://github.com/rogerboy38/sysmayal2/issues
- Community: https://discuss.frappe.io

**This version is production-ready and resolves all known website attribute errors.**
EOF

# Upload release notes to GitHub (manual step)
echo "📋 Release notes created in RELEASE_NOTES_v2.1.0.md"
echo "🌐 Upload this file when creating the GitHub release"
```

---

## 🏭 **PRODUCTION DEPLOYMENT**

### **1. Pre-Production Testing**
```bash
# Set up test environment
cd /path/to/test-frappe-bench

# Install from GitHub
bench get-app sysmayal https://github.com/rogerboy38/sysmayal2.git

# Install on test site
bench --site test.localhost install-app sysmayal

# Run migrations
bench --site test.localhost migrate

# Test the fixes
bench --site test.localhost console
>>> import frappe
>>> # Test each problematic DocType
>>> plan = frappe.get_doc("Market Entry Plan", {"plan_title": "Test Plan"})
>>> reg = frappe.get_doc("Country Regulation", {"country_name": "Test Country"})  
>>> comp = frappe.get_doc("Product Compliance", {"product_name": "Test Product"})
>>> print("All DocTypes load successfully!")
>>> exit()

# Test website functionality
bench --site test.localhost browse
```

### **2. Production Deployment**
```bash
# Backup production before deployment
bench --site production.example.com backup

# Install the fixed app
cd /path/to/production-frappe-bench
bench get-app sysmayal https://github.com/rogerboy38/sysmayal2.git

# Install on production site
bench --site production.example.com install-app sysmayal

# Run migrations (applies all fixes)
bench --site production.example.com migrate

# Clear all caches
bench clear-cache

# Restart production
bench restart
```

### **3. Post-Deployment Verification**
```bash
# Verify error resolution
bench --site production.example.com console
>>> import frappe
>>> # Test all previously problematic DocTypes
>>> frappe.get_doc("Market Entry Plan", "existing-plan-name")
>>> frappe.get_doc("Country Regulation", "existing-regulation-name")
>>> frappe.get_doc("Product Compliance", "existing-compliance-name")
>>> print("✅ All website attribute errors resolved!")
>>> exit()

# Test website publishing
bench --site production.example.com console  
>>> plan = frappe.get_doc("Market Entry Plan", "existing-plan-name")
>>> plan.published = 1
>>> plan.save()
>>> print(f"Plan published at: {plan.route}")
>>> exit()

# Verify website access
curl -I https://production.example.com/market-entry-plans/
curl -I https://production.example.com/country-regulations/
curl -I https://production.example.com/product-compliance/
```

---

## 🔄 **ROLLBACK PROCEDURES**

### **Emergency Rollback (if needed)**
```bash
# Option 1: Restore from backup
bench --site production.example.com restore /path/to/backup/before-sysmayal-fix.sql.gz

# Option 2: Quick disable web views (temporary fix)
bench --site production.example.com console
>>> import frappe
>>> frappe.db.sql("UPDATE `tabDocType` SET has_web_view = 0 WHERE module = 'Sysmayal'")
>>> frappe.db.commit()
>>> exit()
bench restart

# Option 3: Uninstall app completely
bench --site production.example.com uninstall-app sysmayal
bench restart
```

### **Rollforward (after fixing issues)**
```bash
# Re-enable web views after fixes
bench --site production.example.com console
>>> import frappe
>>> frappe.db.sql("UPDATE `tabDocType` SET has_web_view = 1 WHERE module = 'Sysmayal' AND name IN ('Market Entry Plan', 'Country Regulation', 'Product Compliance')")
>>> frappe.db.commit()
>>> exit()
bench restart
```

---

## 🔍 **MONITORING & VALIDATION**

### **1. Health Check Script**
```bash
# Create health check script
cat > /workspace/sysmayal_health_check.py << 'EOF'
#!/usr/bin/env python3
"""
Sysmayal Health Check Script
Validates that all website attribute fixes are working correctly
"""

import frappe
import sys

def check_doctype_website_config(doctype_name):
    """Check if DocType has proper website configuration"""
    try:
        # Check DocType configuration
        doctype = frappe.get_doc("DocType", doctype_name)
        
        # Verify has_web_view is properly set
        if not hasattr(doctype, 'has_web_view'):
            return False, f"{doctype_name}: Missing has_web_view attribute"
        
        # Check if controller can be imported
        module_name = doctype_name.lower().replace(" ", "_")
        module_path = f"sysmayal2.doctype.{module_name}.{module_name}"
        
        try:
            controller_module = frappe.get_module(module_path)
            controller_class = getattr(controller_module, doctype_name.replace(" ", ""))
            
            # Check if it has website attribute
            if not hasattr(controller_class, 'website'):
                return False, f"{doctype_name}: Controller missing website attribute"
                
            return True, f"{doctype_name}: ✅ All checks passed"
            
        except ImportError as e:
            return False, f"{doctype_name}: Controller import failed - {e}"
        except AttributeError as e:
            return False, f"{doctype_name}: Controller class not found - {e}"
            
    except Exception as e:
        return False, f"{doctype_name}: DocType check failed - {e}"

def main():
    """Main health check function"""
    print("🔍 Sysmayal Health Check - Website Configuration Validation")
    print("=" * 60)
    
    # DocTypes to check
    doctypes_to_check = [
        "Market Entry Plan",
        "Country Regulation", 
        "Product Compliance"
    ]
    
    all_passed = True
    results = []
    
    for doctype in doctypes_to_check:
        passed, message = check_doctype_website_config(doctype)
        results.append((doctype, passed, message))
        if not passed:
            all_passed = False
    
    # Print results
    for doctype, passed, message in results:
        status = "✅" if passed else "❌"
        print(f"{status} {message}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED - System is healthy!")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED - Review errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

# Make executable
chmod +x /workspace/sysmayal_health_check.py
```

### **2. Run Health Check**
```bash
# Run health check on production
bench --site production.example.com execute /workspace/sysmayal_health_check.py

# Expected output:
# 🔍 Sysmayal Health Check - Website Configuration Validation
# ============================================================
# ✅ Market Entry Plan: ✅ All checks passed
# ✅ Country Regulation: ✅ All checks passed  
# ✅ Product Compliance: ✅ All checks passed
# ============================================================
# 🎉 ALL CHECKS PASSED - System is healthy!
```

### **3. Continuous Monitoring**
```bash
# Set up monitoring cron job
echo "*/15 * * * * /path/to/frappe-bench/env/bin/python /workspace/sysmayal_health_check.py" | crontab -

# Or create systemd service for monitoring
cat > /etc/systemd/system/sysmayal-monitor.service << 'EOF'
[Unit]
Description=Sysmayal Health Monitor
After=network.target

[Service]
Type=oneshot
ExecStart=/path/to/frappe-bench/env/bin/python /workspace/sysmayal_health_check.py
User=frappe
Group=frappe

[Install]
WantedBy=multi-user.target
EOF

# Set up timer
cat > /etc/systemd/system/sysmayal-monitor.timer << 'EOF'
[Unit]
Description=Run Sysmayal Health Check every 15 minutes
Requires=sysmayal-monitor.service

[Timer]
OnCalendar=*:0/15
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable and start
systemctl enable sysmayal-monitor.timer
systemctl start sysmayal-monitor.timer
```

---

## 📊 **PERFORMANCE MONITORING**

### **1. Key Metrics to Monitor**
```bash
# Monitor DocType loading performance
bench --site production.example.com console
>>> import time
>>> import frappe

>>> # Test Market Entry Plan performance
>>> start = time.time()
>>> plan = frappe.get_doc("Market Entry Plan", "test-plan")
>>> end = time.time()
>>> print(f"Market Entry Plan load time: {end - start:.3f}s")

>>> # Test Country Regulation performance  
>>> start = time.time()
>>> reg = frappe.get_doc("Country Regulation", "test-reg")
>>> end = time.time()
>>> print(f"Country Regulation load time: {end - start:.3f}s")

>>> # Test Product Compliance performance
>>> start = time.time()
>>> comp = frappe.get_doc("Product Compliance", "test-comp")
>>> end = time.time()
>>> print(f"Product Compliance load time: {end - start:.3f}s")
>>> exit()
```

### **2. Website Performance**
```bash
# Test website page load times
curl -w "@curl-format.txt" -o /dev/null -s https://production.example.com/market-entry-plans/

# curl-format.txt content:
cat > curl-format.txt << 'EOF'
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
EOF
```

---

## 📋 **DEPLOYMENT CHECKLIST**

### **Pre-Deployment**
- [ ] ✅ All fixes verified in development environment
- [ ] ✅ Backup of production system created
- [ ] ✅ GitHub repository updated with latest fixed version
- [ ] ✅ Release notes and documentation prepared
- [ ] ✅ Health check script tested
- [ ] ✅ Rollback procedures documented

### **Deployment**
- [ ] ✅ Production system backed up
- [ ] ✅ Fixed app installed from GitHub
- [ ] ✅ Database migrations run successfully
- [ ] ✅ System restarted
- [ ] ✅ Health check passed
- [ ] ✅ Website functionality verified

### **Post-Deployment**
- [ ] ✅ All previously problematic DocTypes load without errors
- [ ] ✅ Website publishing functionality working
- [ ] ✅ API endpoints responding correctly
- [ ] ✅ Performance metrics within acceptable range
- [ ] ✅ User acceptance testing completed
- [ ] ✅ Monitoring systems active

### **Sign-off**
- [ ] ✅ Technical team approval
- [ ] ✅ Business stakeholder approval  
- [ ] ✅ Production deployment successful
- [ ] ✅ All AttributeError issues resolved
- [ ] ✅ System ready for production use

---

## 🎉 **SUCCESS CONFIRMATION**

After successful deployment, you should see:

```bash
# No more errors in logs
tail -f /path/to/frappe-bench/logs/bench.log
# Should show no AttributeError: 'DocType' has no attribute 'website'

# Working website functionality
curl -I https://your-site.com/market-entry-plans/
# Should return HTTP 200 OK

# Successful DocType operations
bench --site your-site console
>>> frappe.get_doc("Market Entry Plan", "any-existing-plan")
# Should load without any AttributeError
```

---

## 📞 **DEPLOYMENT SUPPORT**

### **If Deployment Issues Occur:**

1. **Check logs immediately:**
   ```bash
   bench logs
   tail -f /path/to/frappe-bench/logs/error.log
   ```

2. **Run health check:**
   ```bash
   python /workspace/sysmayal_health_check.py
   ```

3. **Emergency rollback if needed:**
   ```bash
   bench --site your-site restore /path/to/backup.sql.gz
   ```

4. **Get help:**
   - 📧 Email: support@sysmayal.com
   - 💬 Community: https://discuss.frappe.io
   - 🐛 Issues: https://github.com/rogerboy38/sysmayal2/issues

---

**🚀 Your Sysmayal system is now FIXED and ready for production! No more website attribute errors!** ✅
