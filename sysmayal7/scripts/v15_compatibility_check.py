#!/usr/bin/env python3
"""
Sysmayal V15 Compatibility Check Script

This script validates Frappe/ERPNext V15 compatibility and performs
necessary checks before installation.
"""

import sys
import subprocess
import json
from packaging import version


def check_python_version():
    """Check if Python version is compatible."""
    min_python = "3.8"
    current_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    if version.parse(current_python) < version.parse(min_python):
        print(f"❌ Python {min_python}+ required. Current: {current_python}")
        return False
    
    print(f"✅ Python version compatible: {current_python}")
    return True


def check_frappe_version():
    """Check if Frappe version is compatible."""
    try:
        result = subprocess.run(['bench', 'version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Could not get Frappe version. Make sure you're in a bench directory.")
            return False
            
        output = result.stdout
        
        # Parse Frappe version
        for line in output.split('\n'):
            if 'frappe' in line.lower():
                parts = line.split()
                if len(parts) >= 2:
                    frappe_version = parts[1]
                    
                    if version.parse(frappe_version) >= version.parse("15.0.0"):
                        print(f"✅ Frappe version compatible: {frappe_version}")
                        return True
                    else:
                        print(f"❌ Frappe 15.0.0+ required. Current: {frappe_version}")
                        return False
        
        print("❌ Could not parse Frappe version from bench output")
        return False
        
    except FileNotFoundError:
        print("❌ Bench command not found. Make sure Frappe is installed.")
        return False
    except Exception as e:
        print(f"❌ Error checking Frappe version: {e}")
        return False


def check_erpnext_version():
    """Check if ERPNext version is compatible."""
    try:
        result = subprocess.run(['bench', 'version'], capture_output=True, text=True)
        if result.returncode != 0:
            return True  # ERPNext is optional
            
        output = result.stdout
        
        # Parse ERPNext version
        for line in output.split('\n'):
            if 'erpnext' in line.lower():
                parts = line.split()
                if len(parts) >= 2:
                    erpnext_version = parts[1]
                    
                    if version.parse(erpnext_version) >= version.parse("15.0.0"):
                        print(f"✅ ERPNext version compatible: {erpnext_version}")
                        return True
                    else:
                        print(f"❌ ERPNext 15.0.0+ required. Current: {erpnext_version}")
                        return False
        
        print("ℹ️  ERPNext not installed (optional)")
        return True
        
    except Exception as e:
        print(f"ℹ️  Could not check ERPNext version: {e}")
        return True  # ERPNext is optional


def check_dependencies():
    """Check if required Python packages are available."""
    required_packages = [
        'requests>=2.28.0',
        'pandas>=1.5.0',
        'openpyxl>=3.0.10', 
        'xlrd>=2.0.1',
        'python-dateutil>=2.8.2'
    ]
    
    print("\n📦 Checking Python dependencies...")
    all_good = True
    
    for package in required_packages:
        try:
            package_name = package.split('>=')[0] 
            __import__(package_name)
            print(f"✅ {package_name} available")
        except ImportError:
            print(f"⚠️  {package_name} not available (will be installed)")
    
    return True  # Dependencies will be installed during app installation


def run_compatibility_check():
    """Run all compatibility checks."""
    print("🔍 Sysmayal V15 Compatibility Check")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Frappe Version", check_frappe_version), 
        ("ERPNext Version", check_erpnext_version),
        ("Dependencies", check_dependencies)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("🎉 All compatibility checks passed!")
        print("✅ Sysmayal is ready for installation on your V15 system.")
        print("\nNext steps:")
        print("1. bench get-app sysmayal https://github.com/rogerboy38/sysmayal2.git")
        print("2. bench --site your-site install-app sysmayal")
        print("3. bench --site your-site migrate")
        return True
    else:
        print("❌ Some compatibility checks failed.")
        print("Please resolve the issues above before installing Sysmayal.")
        return False


if __name__ == "__main__":
    success = run_compatibility_check()
    sys.exit(0 if success else 1)
