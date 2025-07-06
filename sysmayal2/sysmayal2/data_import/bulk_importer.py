"""
Bulk Data Import Utility for Sysmayal

This module provides comprehensive bulk import functionality for organizations,
contacts, addresses, and regulatory data with validation and error handling.
"""

import frappe
import pandas as pd
import json
import os
from frappe.utils import validate_email_address, nowdate, cstr
from frappe import _

class SysmayalBulkImporter:
    """
    Main class for handling bulk data imports into Sysmayal DocTypes.
    
    Supports:
    - CSV/Excel file imports
    - Data validation and error handling
    - Duplicate detection and management
    - Batch processing for large datasets
    """
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.skip_count = 0
        
    def import_organizations(self, file_path, mapping=None):
        """
        Import distribution organizations from CSV/Excel file.
        
        Args:
            file_path (str): Path to the import file
            mapping (dict): Field mapping configuration
            
        Returns:
            dict: Import results with statistics
        """
        
        try:
            # Read file based on extension
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
                
            # Apply field mapping if provided
            if mapping:
                df = df.rename(columns=mapping)
                
            # Process each row
            for index, row in df.iterrows():
                try:
                    self._import_organization_row(row, index + 1)
                except Exception as e:
                    self.errors.append({
                        "row": index + 1,
                        "error": str(e),
                        "data": dict(row)
                    })
                    
            return self._get_import_results("Distribution Organizations")
            
        except Exception as e:
            frappe.throw(_("Error reading import file: {0}").format(str(e)))
            
    def import_contacts(self, file_path, mapping=None):
        """
        Import distribution contacts from CSV/Excel file.
        
        Args:
            file_path (str): Path to the import file
            mapping (dict): Field mapping configuration
            
        Returns:
            dict: Import results with statistics
        """
        
        try:
            # Read file based on extension
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
                
            # Apply field mapping if provided
            if mapping:
                df = df.rename(columns=mapping)
                
            # Process each row
            for index, row in df.iterrows():
                try:
                    self._import_contact_row(row, index + 1)
                except Exception as e:
                    self.errors.append({
                        "row": index + 1,
                        "error": str(e),
                        "data": dict(row)
                    })
                    
            return self._get_import_results("Distribution Contacts")
            
        except Exception as e:
            frappe.throw(_("Error reading import file: {0}").format(str(e)))
            
    def import_regulatory_data(self, file_path):
        """
        Import regulatory data from JSON file.
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            dict: Import results
        """
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                regulation_data = json.load(f)
                
            # Import country regulations
            result = frappe.call(
                "sysmayal.sysmayal.doctype.country_regulation.country_regulation.import_regulation_data",
                regulation_data=regulation_data
            )
            
            return {
                "doctype": "Country Regulations",
                "total_records": result.get("total", 0),
                "created": result.get("created", 0),
                "updated": result.get("updated", 0),
                "errors": [],
                "warnings": []
            }
            
        except Exception as e:
            frappe.throw(_("Error importing regulatory data: {0}").format(str(e)))
            
    def _import_organization_row(self, row, row_number):
        """Import a single organization row."""
        
        # Validate required fields
        if not row.get('organization_name'):
            raise Exception("Organization name is required")
            
        if not row.get('country'):
            raise Exception("Country is required")
            
        # Check for duplicate
        existing = frappe.db.get_value(
            "Distribution Organization",
            {"organization_name": row['organization_name'], "country": row['country']},
            "name"
        )
        
        if existing:
            self.warnings.append({
                "row": row_number,
                "message": f"Organization '{row['organization_name']}' already exists in {row['country']}",
                "action": "Skipped"
            })
            self.skip_count += 1
            return
            
        # Create new organization
        org = frappe.new_doc("Distribution Organization")
        
        # Map basic fields
        field_mapping = {
            'organization_name': 'organization_name',
            'organization_type': 'organization_type',
            'country': 'country',
            'territory': 'territory',
            'status': 'status',
            'contact_person': 'contact_person',
            'email_id': 'email_id',
            'phone': 'phone',
            'mobile_no': 'mobile_no',
            'website': 'website',
            'address_line_1': 'address_line_1',
            'address_line_2': 'address_line_2',
            'city': 'city',
            'state': 'state',
            'postal_code': 'postal_code',
            'business_focus': 'business_focus',
            'annual_revenue': 'annual_revenue',
            'employee_count': 'employee_count',
            'regulatory_status': 'regulatory_status'
        }
        
        for csv_field, doctype_field in field_mapping.items():
            if csv_field in row and pd.notna(row[csv_field]):
                setattr(org, doctype_field, cstr(row[csv_field]).strip())
                
        # Validate email if provided
        if org.email_id and not validate_email_address(org.email_id):
            raise Exception(f"Invalid email address: {org.email_id}")
            
        # Set defaults
        if not org.status:
            org.status = "Active"
            
        if not org.organization_type:
            org.organization_type = "Distributor"
            
        # Save the organization
        org.save(ignore_permissions=True)
        self.success_count += 1
        
    def _import_contact_row(self, row, row_number):
        """Import a single contact row."""
        
        # Validate required fields
        if not row.get('first_name'):
            raise Exception("First name is required")
            
        if not row.get('email_id'):
            raise Exception("Email ID is required")
            
        if not row.get('organization'):
            raise Exception("Organization is required")
            
        # Validate email format
        if not validate_email_address(row['email_id']):
            raise Exception(f"Invalid email address: {row['email_id']}")
            
        # Check if organization exists
        if not frappe.db.exists("Distribution Organization", row['organization']):
            raise Exception(f"Organization '{row['organization']}' does not exist")
            
        # Check for duplicate email in same organization
        existing = frappe.db.get_value(
            "Distribution Contact",
            {"email_id": row['email_id'], "organization": row['organization']},
            "name"
        )
        
        if existing:
            self.warnings.append({
                "row": row_number,
                "message": f"Contact with email '{row['email_id']}' already exists in organization",
                "action": "Skipped"
            })
            self.skip_count += 1
            return
            
        # Create new contact
        contact = frappe.new_doc("Distribution Contact")
        
        # Map basic fields
        field_mapping = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'organization': 'organization',
            'designation': 'designation',
            'department': 'department',
            'email_id': 'email_id',
            'phone': 'phone',
            'mobile_no': 'mobile_no',
            'country': 'country',
            'regulatory_role': 'regulatory_role',
            'status': 'status',
            'preferred_language': 'preferred_language',
            'communication_preference': 'communication_preference',
            'years_experience': 'years_experience',
            'certifications': 'certifications'
        }
        
        for csv_field, doctype_field in field_mapping.items():
            if csv_field in row and pd.notna(row[csv_field]):
                setattr(contact, doctype_field, cstr(row[csv_field]).strip())
                
        # Set defaults
        if not contact.status:
            contact.status = "Active"
            
        # Save the contact
        contact.save(ignore_permissions=True)
        self.success_count += 1
        
    def _get_import_results(self, doctype_name):
        """Get formatted import results."""
        
        return {
            "doctype": doctype_name,
            "total_records": self.success_count + self.skip_count + len(self.errors),
            "imported": self.success_count,
            "skipped": self.skip_count,
            "errors": len(self.errors),
            "error_details": self.errors,
            "warnings": self.warnings
        }

# Frappe whitelisted functions for API access

@frappe.whitelist()
def import_organizations_from_file(file_url, mapping=None):
    """
    Import organizations from uploaded file.
    
    Args:
        file_url (str): URL of the uploaded file
        mapping (dict): Field mapping configuration
        
    Returns:
        dict: Import results
    """
    
    try:
        # Download file to temporary location
        file_doc = frappe.get_doc("File", {"file_url": file_url})
        file_path = file_doc.get_full_path()
        
        # Parse mapping if string
        if isinstance(mapping, str):
            mapping = json.loads(mapping)
            
        # Import organizations
        importer = SysmayalBulkImporter()
        results = importer.import_organizations(file_path, mapping)
        
        # Log import activity
        frappe.log_error(
            message=f"Organization import completed: {results}",
            title="Sysmayal Organization Import"
        )
        
        return results
        
    except Exception as e:
        frappe.log_error(
            message=f"Organization import failed: {str(e)}",
            title="Sysmayal Organization Import Error"
        )
        frappe.throw(_("Import failed: {0}").format(str(e)))

@frappe.whitelist()
def import_contacts_from_file(file_url, mapping=None):
    """
    Import contacts from uploaded file.
    
    Args:
        file_url (str): URL of the uploaded file
        mapping (dict): Field mapping configuration
        
    Returns:
        dict: Import results
    """
    
    try:
        # Download file to temporary location  
        file_doc = frappe.get_doc("File", {"file_url": file_url})
        file_path = file_doc.get_full_path()
        
        # Parse mapping if string
        if isinstance(mapping, str):
            mapping = json.loads(mapping)
            
        # Import contacts
        importer = SysmayalBulkImporter()
        results = importer.import_contacts(file_path, mapping)
        
        # Log import activity
        frappe.log_error(
            message=f"Contact import completed: {results}",
            title="Sysmayal Contact Import"
        )
        
        return results
        
    except Exception as e:
        frappe.log_error(
            message=f"Contact import failed: {str(e)}",
            title="Sysmayal Contact Import Error"
        )
        frappe.throw(_("Import failed: {0}").format(str(e)))

@frappe.whitelist()
def get_import_template(doctype_name):
    """
    Generate CSV template for data import.
    
    Args:
        doctype_name (str): Name of the DocType
        
    Returns:
        dict: Template structure with fields and sample data
    """
    
    templates = {
        "Distribution Organization": {
            "fields": [
                "organization_name", "organization_type", "country", "territory",
                "status", "contact_person", "email_id", "phone", "mobile_no",
                "website", "address_line_1", "city", "state", "postal_code",
                "business_focus", "annual_revenue", "employee_count", "regulatory_status"
            ],
            "sample_data": [
                [
                    "ABC Distribution Ltd", "Distributor", "United States", "North America",
                    "Active", "John Smith", "john@abcdist.com", "+1-555-0123", "+1-555-0124",
                    "www.abcdist.com", "123 Main St", "New York", "NY", "10001",
                    "Aloe vera product distribution", "5000000", "50", "Compliant"
                ]
            ]
        },
        "Distribution Contact": {
            "fields": [
                "first_name", "last_name", "organization", "designation", "department",
                "email_id", "phone", "mobile_no", "country", "regulatory_role",
                "status", "preferred_language", "communication_preference", "years_experience"
            ],
            "sample_data": [
                [
                    "John", "Smith", "ABC Distribution Ltd", "Sales Manager", "Sales",
                    "john.smith@abcdist.com", "+1-555-0123", "+1-555-0124", "United States",
                    "Sales Manager", "Active", "English", "Email", "10"
                ]
            ]
        }
    }
    
    if doctype_name not in templates:
        frappe.throw(_("Template not available for {0}").format(doctype_name))
        
    return templates[doctype_name]

@frappe.whitelist()
def validate_import_data(file_url, doctype_name, mapping=None):
    """
    Validate import data without actually importing.
    
    Args:
        file_url (str): URL of the uploaded file
        doctype_name (str): Target DocType name
        mapping (dict): Field mapping configuration
        
    Returns:
        dict: Validation results
    """
    
    try:
        # Download file to temporary location
        file_doc = frappe.get_doc("File", {"file_url": file_url})
        file_path = file_doc.get_full_path()
        
        # Parse mapping if string
        if isinstance(mapping, str):
            mapping = json.loads(mapping)
            
        # Read file
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
            
        # Apply field mapping if provided
        if mapping:
            df = df.rename(columns=mapping)
            
        validation_results = {
            "total_rows": len(df),
            "columns": list(df.columns),
            "missing_required_fields": [],
            "invalid_data": [],
            "duplicates": [],
            "warnings": []
        }
        
        # Validate based on DocType
        if doctype_name == "Distribution Organization":
            validation_results = _validate_organization_data(df, validation_results)
        elif doctype_name == "Distribution Contact":
            validation_results = _validate_contact_data(df, validation_results)
            
        return validation_results
        
    except Exception as e:
        frappe.throw(_("Validation failed: {0}").format(str(e)))

def _validate_organization_data(df, results):
    """Validate organization import data."""
    
    required_fields = ["organization_name", "country"]
    
    # Check for missing required fields
    for field in required_fields:
        if field not in df.columns:
            results["missing_required_fields"].append(field)
            
    # Check for empty required values
    for index, row in df.iterrows():
        for field in required_fields:
            if field in df.columns and pd.isna(row[field]):
                results["invalid_data"].append({
                    "row": index + 1,
                    "field": field,
                    "issue": "Required field is empty"
                })
                
    # Check for duplicates
    if "organization_name" in df.columns and "country" in df.columns:
        duplicates = df[df.duplicated(['organization_name', 'country'], keep=False)]
        for index, row in duplicates.iterrows():
            results["duplicates"].append({
                "row": index + 1,
                "organization_name": row['organization_name'],
                "country": row['country']
            })
            
    return results

def _validate_contact_data(df, results):
    """Validate contact import data."""
    
    required_fields = ["first_name", "email_id", "organization"]
    
    # Check for missing required fields
    for field in required_fields:
        if field not in df.columns:
            results["missing_required_fields"].append(field)
            
    # Check for empty required values and email format
    for index, row in df.iterrows():
        for field in required_fields:
            if field in df.columns and pd.isna(row[field]):
                results["invalid_data"].append({
                    "row": index + 1,
                    "field": field,
                    "issue": "Required field is empty"
                })
                
        # Validate email format
        if "email_id" in df.columns and pd.notna(row['email_id']):
            if not validate_email_address(str(row['email_id'])):
                results["invalid_data"].append({
                    "row": index + 1,
                    "field": "email_id",
                    "issue": "Invalid email format"
                })
                
    # Check for duplicate emails within same organization
    if "email_id" in df.columns and "organization" in df.columns:
        duplicates = df[df.duplicated(['email_id', 'organization'], keep=False)]
        for index, row in duplicates.iterrows():
            results["duplicates"].append({
                "row": index + 1,
                "email_id": row['email_id'],
                "organization": row['organization']
            })
            
    return results
