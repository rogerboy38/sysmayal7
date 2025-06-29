# 🚀 Sysmayal V15 Installation Guide

## ⚡ Quick Start for ERPNext 15.65.1 & Frappe 15.70.0

### **Step 1: Pre-Installation Check**
```bash
# Check your current versions
bench version

# Expected output should show:
# frappe 15.x.x
# erpnext 15.x.x (optional)
```

<<<<<<< HEAD
### **Step 2: Install Sysmayal** new
=======
### **Step 2: Install Sysmayal**
>>>>>>> 3cf3cb8 (error website fixed V15)
```bash
# Navigate to your bench
cd /path/to/your/bench

# Get the V15-ready Sysmayal app
bench get-app sysmayal https://github.com/rogerboy38/sysmayal2.git

# Install on your site
bench --site your-site-name install-app sysmayal

# Run database migration
bench --site your-site-name migrate

# Restart all services
bench restart
```

### **Step 3: Verify Installation**
```bash
# Check installed apps
bench --site your-site-name list-apps

# You should see sysmayal in the list
```

### **Step 4: Access Sysmayal**
1. Login to your ERPNext site
2. Look for "Sysmayal" in the workspace menu
3. Click on Sysmayal workspace
4. You should see all distribution and compliance tools

## ✅ **Success Checklist**

After installation, verify these work without errors:

- [ ] **Sysmayal Workspace** loads successfully
- [ ] **Distribution Organization** DocType is accessible
- [ ] **Country Regulation** DocType opens without errors
- [ ] **Product Compliance** DocType functions properly
- [ ] **Market Entry Plan** can be created and saved
- [ ] **Website publishing** works (no AttributeError messages)

## 🔧 **Troubleshooting**

### **Common Issues**

#### **"AttributeError: type object has no attribute 'website'"**
✅ **FIXED** - This error has been resolved in V2.1.1

#### **Installation fails with dependency errors**
```bash
# Update pip and try again
pip install --upgrade pip setuptools wheel
bench get-app sysmayal https://github.com/rogerboy38/sysmayal2.git --force
```

#### **Migration errors**
```bash
# Skip failing migrations and check manually
bench --site your-site-name migrate --skip-failing
bench --site your-site-name console
```

#### **Website cache issues**
```bash
# Clear website cache
bench --site your-site-name rebuild-website-cache
bench restart
```

## 📞 **Support**

If you encounter issues:
1. Check the [troubleshooting section](#troubleshooting) above
2. Review the complete [README_V15.md](README_V15.md)
3. Submit an issue on [GitHub](https://github.com/rogerboy38/sysmayal2/issues)

---

**🎉 Welcome to Sysmayal V15 - Your aloe vera business management solution!**
