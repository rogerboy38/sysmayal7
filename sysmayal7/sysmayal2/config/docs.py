"""
Documentation configuration for Sysmayal app.

This file defines the structure and organization of documentation
for the Sysmayal application.
"""

source_link = "https://github.com/sysmayal/sysmayal"
docs_base_url = "https://sysmayal.readthedocs.io"
headline = "Global Distribution & R&D Management"
sub_heading = "Comprehensive solution for aloe vera product distribution and regulatory compliance"

def get_context(context):
    """Get context for documentation pages."""
    
    context.brand_html = """
        <div class="navbar-brand">
            <img src="/assets/sysmayal/images/sysmayal-logo.png" alt="Sysmayal" height="30">
        </div>
    """
    
    context.top_bar_items = [
        {"label": "User Guide", "url": context.docs_base_url + "/user-guide", "right": 1},
        {"label": "API", "url": context.docs_base_url + "/api", "right": 1},
        {"label": "GitHub", "url": source_link, "right": 1},
    ]
