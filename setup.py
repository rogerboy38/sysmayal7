#!/usr/bin/env python
"""
Sysmayal - Global Distribution & R&D Management
A comprehensive Frappe app for managing aloe vera product distribution,
regulatory compliance, and research & development activities globally.
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sysmayal/__init__.py
from sysmayal import __version__ as version

setup(
    name="sysmayal",
    version=version,
    description="Global Distribution & R&D Management for Aloe Vera Products",
    author="Sysmayal Development Team",
    author_email="dev@sysmayal.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    long_description="""
    Sysmayal is a comprehensive Frappe application designed specifically for global 
    distribution and research & development management of aloe vera products. 
    
    Key Features:
    - Global distributor and organization management
    - Country-specific regulatory compliance tracking
    - R&D project management and product development tracking
    - Certification and document management
    - Bulk data import tools for contacts and addresses
    - Integration with ERPNext CRM and sales modules
    - Multi-language and multi-currency support
    - Automated compliance monitoring and reporting
    
    This app is ideal for companies involved in the aloe vera industry who need to 
    manage complex global distribution networks while maintaining strict regulatory 
    compliance across different markets.
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Frappe",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Enterprise Resource Planning",
        "Topic :: Scientific/Engineering :: Medical Science Apps",
    ],
    keywords="frappe erpnext aloe vera distribution r&d regulatory compliance",
    python_requires=">=3.8",
)
