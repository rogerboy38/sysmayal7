"""
Desktop configuration for Sysmayal app.

This file defines how the Sysmayal module appears in the ERPNext desk,
including icons, links, and navigation structure.
"""

from frappe import _

def get_data():
    """Return desktop configuration for Sysmayal module."""
    
    return [
        {
            "module_name": "sysmayal2",
            "category": "Modules",
            "label": _("Sysmayal"),
            "color": "green",
            "icon": "octicon octicon-globe",
            "type": "module",
            "description": _("Global Distribution & R&D Management for Aloe Vera Products"),
            "onboard_present": True
        }
    ]
