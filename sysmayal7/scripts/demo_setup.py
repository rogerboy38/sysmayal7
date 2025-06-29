#!/usr/bin/env python3
"""
Sysmayal Demo Setup Script

This script demonstrates the key functionality of the Sysmayal app
and can be used to set up demo data for testing and evaluation.
"""

import frappe
import json
import os
from frappe.utils import nowdate, add_days

def setup_demo_data():
    """Set up demo data for Sysmayal app evaluation."""
    
    print("Setting up Sysmayal demo data...")
    
    # Create demo organizations
    create_demo_organizations()
    
    # Create demo contacts
    create_demo_contacts()
    
    # Create demo R&D projects
    create_demo_projects()
    
    # Create demo product compliance records
    create_demo_product_compliance()
    
    # Create demo certification documents
    create_demo_certification_documents()
    
    # Create demo market entry plans
    create_demo_market_entry_plans()
    
    # Create demo market research
    create_demo_market_research()
    
    # Import regulatory data if available
    import_regulatory_data()
    
    print("Demo data setup completed!")

def create_demo_organizations():
    """Create demo distribution organizations."""
    
    demo_orgs = [
        {
            "organization_name": "Global Aloe Distribution",
            "organization_type": "Distributor",
            "country": "United States",
            "territory": "North America",
            "status": "Active",
            "contact_person": "Jennifer Adams",
            "email_id": "jennifer@globalaloe.com",
            "phone": "+1-555-0100",
            "website": "www.globalaloe.com",
            "address_line_1": "100 Business Park Dr",
            "city": "Austin",
            "state": "TX",
            "postal_code": "78701",
            "business_focus": "Premium aloe vera product distribution across North America",
            "annual_revenue": 15000000,
            "employee_count": 85,
            "regulatory_status": "Compliant"
        },
        {
            "organization_name": "European Wellness Corp",
            "organization_type": "Retailer",
            "country": "Germany", 
            "territory": "Europe",
            "status": "Active",
            "contact_person": "Klaus Weber",
            "email_id": "klaus@eurwellness.de",
            "phone": "+49-30-555-0200",
            "website": "www.eurwellness.de",
            "address_line_1": "Potsdamer Platz 15",
            "city": "Berlin",
            "postal_code": "10785",
            "business_focus": "Retail wellness and natural health products",
            "annual_revenue": 8000000,
            "employee_count": 45,
            "regulatory_status": "Compliant"
        },
        {
            "organization_name": "Pacific Aloe Farms",
            "organization_type": "Supplier",
            "country": "Australia",
            "territory": "Australia and New Zealand", 
            "status": "Active",
            "contact_person": "Emma Thompson",
            "email_id": "emma@pacificaloe.au",
            "phone": "+61-7-555-0300",
            "website": "www.pacificaloe.au",
            "address_line_1": "245 Farm Road",
            "city": "Brisbane",
            "state": "QLD",
            "postal_code": "4000",
            "business_focus": "Organic aloe vera cultivation and raw material supply",
            "annual_revenue": 5000000,
            "employee_count": 60,
            "regulatory_status": "Pending Review"
        }
    ]
    
    for org_data in demo_orgs:
        if not frappe.db.exists("Distribution Organization", 
                               {"organization_name": org_data["organization_name"]}):
            org = frappe.new_doc("Distribution Organization")
            org.update(org_data)
            org.save(ignore_permissions=True)
            print(f"Created organization: {org_data['organization_name']}")

def create_demo_contacts():
    """Create demo distribution contacts."""
    
    demo_contacts = [
        {
            "first_name": "Jennifer",
            "last_name": "Adams", 
            "organization": "Global Aloe Distribution",
            "designation": "VP of Sales",
            "department": "Sales",
            "email_id": "jennifer.adams@globalaloe.com",
            "phone": "+1-555-0100",
            "mobile_no": "+1-555-0101",
            "country": "United States",
            "regulatory_role": "Sales Manager",
            "status": "Active",
            "preferred_language": "en",
            "communication_preference": "Email",
            "years_experience": 12,
            "certifications": "MBA Marketing, Sales Leadership Certificate"
        },
        {
            "first_name": "Robert",
            "last_name": "Chen",
            "organization": "Global Aloe Distribution", 
            "designation": "Quality Manager",
            "department": "Quality Assurance",
            "email_id": "robert.chen@globalaloe.com",
            "phone": "+1-555-0102",
            "country": "United States",
            "regulatory_role": "Quality Manager",
            "status": "Active",
            "preferred_language": "en",
            "communication_preference": "Phone",
            "years_experience": 15,
            "certifications": "ISO 9001 Lead Auditor, Six Sigma Black Belt"
        },
        {
            "first_name": "Klaus",
            "last_name": "Weber",
            "organization": "European Wellness Corp",
            "designation": "Managing Director",
            "department": "Executive",
            "email_id": "klaus.weber@eurwellness.de",
            "phone": "+49-30-555-0200",
            "country": "Germany",
            "regulatory_role": "Business Development",
            "status": "Active", 
            "preferred_language": "de",
            "communication_preference": "Video Call",
            "years_experience": 18,
            "certifications": "MBA International Business, EU Market Authorization"
        }
    ]
    
    for contact_data in demo_contacts:
        if not frappe.db.exists("Distribution Contact",
                               {"email_id": contact_data["email_id"]}):
            contact = frappe.new_doc("Distribution Contact")
            contact.update(contact_data)
            contact.save(ignore_permissions=True)
            print(f"Created contact: {contact_data['first_name']} {contact_data['last_name']}")

def create_demo_projects():
    """Create demo R&D projects."""
    
    demo_projects = [
        {
            "project_name": "Enhanced Aloe Juice Formula",
            "project_type": "Product Improvement",
            "status": "In Progress",
            "start_date": add_days(nowdate(), -90),
            "expected_completion": add_days(nowdate(), 60),
            "priority": "High",
            "product_category": "Aloe Juice",
            "target_markets": "United States, Canada, Mexico",
            "project_description": "<p>Development of improved aloe juice formula with enhanced bioavailability and extended shelf life.</p>",
            "business_case": "<p>Market research indicates strong demand for premium aloe juice products. Enhanced formula expected to increase market share by 15%.</p>",
            "success_criteria": "Achieve 20% higher acemannan content, 6-month shelf life, FDA approval",
            "estimated_investment": 500000,
            "completion_percentage": 65,
            "current_phase": "Laboratory Testing",
            "next_milestone": "Stability Testing Completion",
            "regulatory_strategy": "<p>FDA GRAS notification required. Coordinate with regulatory affairs for submission timeline.</p>",
            "target_countries": "United States, Canada",
            "required_certifications": "FDA GRAS, Health Canada NHP License",
            "compliance_status": "In Progress"
        },
        {
            "project_name": "Organic Aloe Powder Development",
            "project_type": "New Product Development",
            "status": "Planning",
            "start_date": add_days(nowdate(), 30),
            "expected_completion": add_days(nowdate(), 180),
            "priority": "Medium",
            "product_category": "Aloe Powder",
            "target_markets": "Europe, Australia",
            "project_description": "<p>Development of organic certified aloe powder for European and Australian markets.</p>",
            "business_case": "<p>Growing demand for organic ingredients in EU market. Projected revenue of $2M annually.</p>",
            "success_criteria": "EU Organic certification, 99% pure aloe content, cost under $15/kg",
            "estimated_investment": 750000,
            "completion_percentage": 10,
            "current_phase": "Requirements Analysis",
            "next_milestone": "Supplier Selection",
            "regulatory_strategy": "<p>EU organic certification required. Coordinate with certification bodies early in process.</p>",
            "target_countries": "Germany, France, Australia",
            "required_certifications": "EU Organic Certification, TGA Approval",
            "compliance_status": "Not Started"
        }
    ]
    
    for project_data in demo_projects:
        if not frappe.db.exists("Product Development Project",
                               {"project_name": project_data["project_name"]}):
            project = frappe.new_doc("Product Development Project")
            project.update(project_data)
            project.save(ignore_permissions=True)
            print(f"Created project: {project_data['project_name']}")

def create_demo_product_compliance():
    """Create demo product compliance records."""
    
    demo_compliance = [
        {
            "product_name": "Premium Aloe Juice Concentrate",
            "product_code": "AJC-001",
            "country": "United States",
            "compliance_status": "Compliant",
            "compliance_percentage": 100,
            "risk_level": "Low",
            "approval_status": "Approved",
            "testing_status": "Completed",
            "approval_date": add_days(nowdate(), -180),
            "next_review_date": add_days(nowdate(), 180),
            "expiry_date": add_days(nowdate(), 720),
            "manufacturer": "Global Aloe Distribution",
            "responsible_person": "Administrator",
            "regulatory_authority": "FDA",
            "approval_number": "FDA-GRAS-2024-001",
            "contact_email": "compliance@globalaloe.com",
            "compliance_notes": "Full FDA GRAS approval obtained. All testing requirements met.",
            "required_tests": "Microbiological Testing\nHeavy Metals Analysis\nPesticide Residue Testing\nAloesin Content Analysis",
            "certifications_held": "FDA GRAS\nOrganic Certification\nKosher Certification"
        },
        {
            "product_name": "Organic Aloe Powder 200X",
            "product_code": "OAP-200",
            "country": "Germany",
            "compliance_status": "Pending Review",
            "compliance_percentage": 75,
            "risk_level": "Medium",
            "approval_status": "Under Review",
            "testing_status": "In Progress",
            "next_review_date": add_days(nowdate(), 30),
            "expiry_date": add_days(nowdate(), 540),
            "manufacturer": "European Botanical Suppliers",
            "responsible_person": "Administrator",
            "regulatory_authority": "BfArM",
            "contact_email": "regulatory@eubotanical.eu",
            "compliance_notes": "EU Novel Food assessment ongoing. Additional documentation requested.",
            "required_tests": "EU Novel Food Safety Assessment\nContaminant Analysis\nAllergen Testing\nStability Studies",
            "certifications_held": "EU Organic Certification"
        },
        {
            "product_name": "Aloe Vera Gel Extract",
            "product_code": "AVG-100",
            "country": "Australia",
            "compliance_status": "Non-Compliant",
            "compliance_percentage": 45,
            "risk_level": "High",
            "approval_status": "Rejected",
            "testing_status": "Failed",
            "next_review_date": add_days(nowdate(), 7),
            "manufacturer": "Australian Natural Products",
            "responsible_person": "Administrator",
            "regulatory_authority": "TGA",
            "contact_email": "quality@ausnaturals.com.au",
            "compliance_notes": "TGA review identified contamination issues. Product recall initiated.",
            "required_tests": "Microbiological Testing\nContaminant Analysis\nGMP Audit",
            "certifications_held": "None"
        }
    ]
    
    for compliance_data in demo_compliance:
        if not frappe.db.exists("Product Compliance",
                               {"product_name": compliance_data["product_name"], 
                                "country": compliance_data["country"]}):
            compliance = frappe.new_doc("Product Compliance")
            compliance.update(compliance_data)
            compliance.save(ignore_permissions=True)
            print(f"Created compliance record: {compliance_data['product_name']} - {compliance_data['country']}")

def create_demo_certification_documents():
    """Create demo certification documents."""
    
    demo_certificates = [
        {
            "document_title": "FDA GRAS Notification - Aloe Juice",
            "certification_type": "Regulatory Approval",
            "issuing_authority": "FDA",
            "country": "United States",
            "certificate_number": "FDA-GRAS-2024-001",
            "issue_date": add_days(nowdate(), -180),
            "expiry_date": add_days(nowdate(), 720),
            "status": "Active",
            "related_product": "Premium Aloe Juice Concentrate",
            "organization": "Global Aloe Distribution",
            "primary_contact": "Jennifer Adams",
            "secondary_contact": "Michael Chen",
            "contact_email": "regulatory@globalaloe.com",
            "document_description": "FDA Generally Recognized as Safe (GRAS) notification for aloe juice concentrate product",
            "scope": "Manufacturing and distribution of aloe juice concentrate for food and beverage applications",
            "compliance_requirements": "Annual reporting required\nGMP compliance mandatory\nProduct testing every 6 months",
            "renewal_process": "Submit renewal application 90 days before expiry with updated safety data",
            "audit_frequency": "Annual",
            "next_audit_date": add_days(nowdate(), 180),
            "document_language": "English"
        },
        {
            "document_title": "EU Organic Certification",
            "certification_type": "Quality Certification",
            "issuing_authority": "ECOCERT",
            "country": "Germany",
            "certificate_number": "EU-ORG-2024-7890",
            "issue_date": add_days(nowdate(), -90),
            "expiry_date": add_days(nowdate(), 275),
            "status": "Active",
            "related_product": "Organic Aloe Powder 200X",
            "organization": "European Botanical Suppliers",
            "primary_contact": "Hans Mueller",
            "contact_email": "certification@eubotanical.eu",
            "document_description": "EU Organic certification for aloe powder production and processing",
            "scope": "Organic aloe vera cultivation, processing, and powder production",
            "compliance_requirements": "Organic farming standards\nProcessing facility certification\nSupply chain traceability",
            "renewal_process": "Annual inspection and certification renewal",
            "audit_frequency": "Annual",
            "next_audit_date": add_days(nowdate(), 90),
            "document_language": "German"
        },
        {
            "document_title": "TGA Manufacturing License",
            "certification_type": "Manufacturing License",
            "issuing_authority": "TGA",
            "country": "Australia",
            "certificate_number": "TGA-ML-2024-3456",
            "issue_date": add_days(nowdate(), -120),
            "expiry_date": add_days(nowdate(), 245),
            "status": "Suspended",
            "related_product": "Aloe Vera Gel Extract",
            "organization": "Australian Natural Products",
            "primary_contact": "Sarah Thompson",
            "contact_email": "licensing@ausnaturals.com.au",
            "document_description": "TGA manufacturing license for therapeutic goods containing aloe vera",
            "scope": "Manufacturing of aloe vera based therapeutic goods",
            "compliance_requirements": "GMP compliance\nQuality management system\nRegular product testing",
            "renewal_process": "License renewal with updated GMP certification",
            "audit_frequency": "Bi-annual",
            "next_audit_date": add_days(nowdate(), 14),
            "document_language": "English",
            "suspension_reason": "Non-compliance with GMP standards identified during inspection"
        }
    ]
    
    for cert_data in demo_certificates:
        if not frappe.db.exists("Certification Document",
                               {"certificate_number": cert_data["certificate_number"]}):
            certificate = frappe.new_doc("Certification Document")
            certificate.update(cert_data)
            certificate.save(ignore_permissions=True)
            print(f"Created certificate: {cert_data['document_title']}")

def create_demo_market_entry_plans():
    """Create demo market entry plans."""
    
    demo_plans = [
        {
            "plan_name": "European Market Entry - Premium Aloe Products",
            "target_country": "Germany",
            "target_market": "European Union",
            "product_category": "Aloe Juice",
            "entry_strategy": "Direct Distribution",
            "status": "In Progress",
            "priority": "High",
            "start_date": add_days(nowdate(), -60),
            "target_launch_date": add_days(nowdate(), 120),
            "estimated_budget": 1500000,
            "project_manager": "Administrator",
            "market_lead": "European Botanical Suppliers",
            "regulatory_lead": "Administrator",
            "business_objective": "Establish strong market presence in EU with premium aloe juice products targeting health-conscious consumers",
            "market_analysis": "EU health food market valued at €15B with 8% annual growth. Germany represents 35% of market share.",
            "target_customers": "Health food stores\nOrganic retailers\nOnline wellness platforms\nPrivate label manufacturers",
            "competitive_landscape": "Limited premium aloe juice offerings. Main competitors include Forever Living and Lily of the Desert.",
            "regulatory_requirements": "Novel Food authorization\nOrganic certification\nFood safety compliance\nLabeling requirements",
            "market_barriers": "Strict EU regulatory environment\nEstablished competitor relationships\nHigh market entry costs",
            "success_metrics": "€2M revenue in Year 1\n15% market share in premium segment\n50+ retail partnerships",
            "risk_assessment": "Regulatory delays (High)\nCurrency fluctuation (Medium)\nSupply chain disruption (Low)",
            "go_to_market_strategy": "Phase 1: Regulatory approval and certification\nPhase 2: Distributor partnerships\nPhase 3: Direct retail relationships",
            "expected_revenue_y1": 2000000,
            "expected_revenue_y3": 6000000,
            "completion_percentage": 45
        },
        {
            "plan_name": "Asian Pacific Expansion - Aloe Powder",
            "target_country": "Japan",
            "target_market": "Asia Pacific",
            "product_category": "Aloe Powder",
            "entry_strategy": "Joint Venture",
            "status": "Planning",
            "priority": "Medium",
            "start_date": nowdate(),
            "target_launch_date": add_days(nowdate(), 270),
            "estimated_budget": 2000000,
            "project_manager": "Administrator",
            "local_partner": "Tokyo Natural Ingredients",
            "regulatory_lead": "Administrator",
            "business_objective": "Enter Japanese market through strategic partnership leveraging local expertise and distribution networks",
            "market_analysis": "Japan dietary supplement market worth ¥1.5T with strong preference for natural ingredients and premium quality",
            "target_customers": "Pharmaceutical companies\nCosmetic manufacturers\nDietary supplement brands\nTraditional medicine practitioners",
            "competitive_landscape": "Dominated by local suppliers with limited international premium offerings",
            "regulatory_requirements": "PMDA approval for health claims\nFood safety certification\nImport licensing\nGMP compliance",
            "market_barriers": "Complex regulatory environment\nCultural preferences\nLanguage barriers\nEstablished supply chains",
            "success_metrics": "¥500M revenue in Year 2\n5 major pharmaceutical partnerships\nRegulatory approval within 12 months",
            "risk_assessment": "Regulatory complexity (High)\nPartnership risks (Medium)\nMarket acceptance (Medium)",
            "go_to_market_strategy": "Joint venture with local partner\nLeverage existing distribution\nFocus on B2B pharmaceutical market",
            "expected_revenue_y1": 500000,
            "expected_revenue_y3": 3000000,
            "completion_percentage": 15
        },
        {
            "plan_name": "Canadian Health Products Expansion",
            "target_country": "Canada",
            "target_market": "North America",
            "product_category": "Dietary Supplement",
            "entry_strategy": "Direct Sales",
            "status": "Completed",
            "priority": "High",
            "start_date": add_days(nowdate(), -365),
            "target_launch_date": add_days(nowdate(), -90),
            "actual_launch_date": add_days(nowdate(), -75),
            "estimated_budget": 800000,
            "actual_budget": 750000,
            "project_manager": "Administrator",
            "regulatory_lead": "Administrator",
            "business_objective": "Successfully launched aloe-based dietary supplements in Canadian market with Health Canada NHP approval",
            "market_analysis": "Canadian natural health products market worth CAD $5.2B with 7% annual growth",
            "target_customers": "Health food retailers\nPharmacies\nOnline marketplaces\nNaturopathic practitioners",
            "regulatory_requirements": "Health Canada NHP License\nGMP certification\nProduct licensing\nSafety assessments",
            "success_metrics": "CAD $1.2M revenue in Year 1 (Achieved)\n25+ retail partnerships (Achieved: 32)\nNHP approval within 8 months (Achieved: 6 months)",
            "go_to_market_strategy": "Health Canada approval first\nPartnership with major retailers\nDigital marketing campaign",
            "expected_revenue_y1": 1200000,
            "actual_revenue_y1": 1350000,
            "expected_revenue_y3": 3600000,
            "completion_percentage": 100,
            "lessons_learned": "Early regulatory engagement crucial\nStrong digital presence drives sales\nCanadian consumers prefer premium quality",
            "post_launch_performance": "Exceeded revenue targets by 12.5%\nStrong customer satisfaction ratings (4.8/5)\nSuccessful expansion to 5 provinces"
        }
    ]
    
    for plan_data in demo_plans:
        if not frappe.db.exists("Market Entry Plan",
                               {"plan_name": plan_data["plan_name"]}):
            plan = frappe.new_doc("Market Entry Plan")
            plan.update(plan_data)
            plan.save(ignore_permissions=True)
            print(f"Created market entry plan: {plan_data['plan_name']}")

def create_demo_market_research():
    """Create demo market research records."""
    
    demo_research = [
        {
            "research_title": "North American Aloe Juice Market Analysis",
            "research_type": "Market Analysis",
            "research_status": "Completed",
            "country": "United States",
            "region": "North America",
            "product_category": "Aloe Juice",
            "research_date": add_days(nowdate(), -90),
            "research_lead": "Administrator",
            "priority": "High",
            "completion_percentage": 100,
            "market_size": "$450 million USD",
            "market_growth_rate": 8.5,
            "market_value": 450000000,
            "target_segments": "Health-conscious consumers, Wellness industry, Functional beverage market",
            "key_drivers": "Increasing health awareness, Growing demand for natural products, Rising disposable income",
            "market_barriers": "Regulatory complexity, High competition, Consumer education needs",
            "main_competitors": "Forever Living Products, Lily of the Desert, George's Aloe Vera, Stockton Aloe 1",
            "competitive_landscape": "<p>The North American aloe juice market is dominated by established players with strong brand recognition. Forever Living leads with ~25% market share, followed by Lily of the Desert at ~18%. The market shows consolidation trends with top 5 players controlling 65% of market share.</p>",
            "market_share_analysis": "Forever Living (25%), Lily of the Desert (18%), George's Aloe Vera (12%), Stockton Aloe 1 (10%), Others (35%)",
            "competitive_advantages": "Superior product quality, Organic certification, Sustainable sourcing, Strong R&D capabilities",
            "competitive_threats": "Price competition from low-cost producers, Private label growth, New market entrants",
            "target_demographics": "Adults 25-55, Higher income households ($50K+), Health and wellness focused consumers",
            "customer_behavior": "<p>Customers primarily purchase through health food stores (40%), online channels (35%), and pharmacies (25%). Brand loyalty is moderate with 60% willing to switch for better quality or price.</p>",
            "buying_patterns": "Regular monthly purchases, Bulk buying for better pricing, Seasonal increases in winter months",
            "customer_preferences": "Organic certification, No added sugars, Sustainable packaging, Third-party testing verification",
            "price_sensitivity": "Moderate price sensitivity, Premium pricing acceptable for quality products (up to 20% premium)",
            "strengths": "High product quality, Strong brand recognition, Established distribution channels",
            "weaknesses": "Higher production costs, Limited marketing budget, Regulatory compliance complexity",
            "opportunities": "Growing wellness trend, E-commerce expansion, Private label partnerships",
            "threats": "Increased competition, Regulatory changes, Supply chain disruptions",
            "regulatory_environment": "<p>FDA oversight through GRAS notifications for health claims. FTC regulation for marketing claims. Organic certification requirements for organic products.</p>",
            "compliance_requirements": "FDA GRAS notification, Organic certification (if applicable), Good Manufacturing Practices (GMP)",
            "regulatory_challenges": "Complex health claim regulations, State-by-state labeling requirements, Import documentation",
            "regulatory_opportunities": "New FDA guidance on functional foods, Growing acceptance of natural health products",
            "market_trends": "<p>Increasing demand for functional beverages, Growth in online sales channels, Premium product segment expansion, Sustainability focus in packaging</p>",
            "future_projections": "8-10% annual growth projected through 2028, E-commerce to reach 50% by 2026",
            "growth_opportunities": "Product innovation, Geographic expansion, Private label partnerships, Subscription models",
            "risk_factors": "Supply chain disruptions, Regulatory changes, Economic downturns affecting discretionary spending",
            "research_methods": "Market surveys, Industry interviews, Competitor analysis, Sales data analysis",
            "data_sources": "IBISWorld reports, Nielsen data, Industry trade publications, Company financial reports",
            "sample_size": 2500,
            "research_duration": "6 months",
            "research_budget": 85000,
            "external_consultants": "Market Research Solutions Inc.",
            "reliability_score": "High",
            "key_findings": "<p>The North American aloe juice market shows strong growth potential with 8.5% CAGR. Key success factors include organic certification, premium positioning, and strong online presence. Market entry barriers are moderate but require significant investment in compliance and marketing.</p>",
            "strategic_recommendations": "<p>1. Target premium market segment with organic certification<br>2. Invest in e-commerce capabilities<br>3. Partner with established distributors<br>4. Focus on health claims substantiation<br>5. Develop subscription-based sales model</p>",
            "next_steps": "Develop market entry plan, Conduct regulatory compliance review, Identify potential distribution partners",
            "action_items": "1. Secure organic certification\n2. Develop e-commerce platform\n3. Create marketing materials\n4. Establish quality testing protocols"
        },
        {
            "research_title": "European Aloe Powder Market Competitive Analysis",
            "research_type": "Competitive Intelligence",
            "research_status": "In Progress",
            "country": "Germany",
            "region": "European Union",
            "product_category": "Aloe Powder",
            "research_date": add_days(nowdate(), -30),
            "research_lead": "Administrator",
            "priority": "Medium",
            "completion_percentage": 65,
            "market_size": "€180 million EUR",
            "market_growth_rate": 12.3,
            "market_value": 200000000,
            "target_segments": "Pharmaceutical industry, Cosmetic manufacturers, Dietary supplement companies",
            "key_drivers": "Growing demand for natural ingredients, EU organic regulations favor natural products, Pharmaceutical industry growth",
            "market_barriers": "Strict EU Novel Food regulations, High certification costs, Established supplier relationships",
            "main_competitors": "Naturex (Givaudan), Nexira, Bioactive International, Aloecorp",
            "competitive_landscape": "<p>European aloe powder market is fragmented with multiple regional players. Market leadership varies by application segment - pharmaceuticals vs cosmetics vs supplements.</p>",
            "competitive_advantages": "High purity products, EU organic certification, Pharmaceutical grade quality, Reliable supply chain",
            "competitive_threats": "Asian low-cost producers, Vertical integration by large pharmaceutical companies",
            "target_demographics": "B2B customers: Pharmaceutical companies, Cosmetic manufacturers, Supplement brands",
            "customer_behavior": "<p>Long-term contracts preferred, Quality and certification critical, Price secondary to reliability and compliance</p>",
            "research_methods": "Industry interviews, Competitor product analysis, Trade show research, Patent analysis",
            "data_sources": "Euromonitor, Industry associations, Trade publications, Company reports",
            "sample_size": 150,
            "research_duration": "4 months",
            "research_budget": 45000,
            "reliability_score": "Medium",
            "key_findings": "<p>European market prioritizes quality and certification over price. Novel Food regulations create barriers but also protect market for compliant suppliers.</p>",
            "strategic_recommendations": "<p>Focus on pharmaceutical grade quality, Secure EU Novel Food authorization, Establish local distribution partnerships</p>"
        },
        {
            "research_title": "Asian Pacific Aloe Market Customer Research",
            "research_type": "Customer Research", 
            "research_status": "Planning",
            "country": "Japan",
            "region": "Asia Pacific",
            "product_category": "Aloe Juice",
            "research_date": nowdate(),
            "research_lead": "Administrator",
            "priority": "Medium",
            "completion_percentage": 15,
            "target_segments": "Health-conscious consumers, Traditional medicine practitioners, Beauty and wellness market",
            "research_methods": "Consumer surveys, Focus groups, In-store interviews, Online behavior analysis",
            "data_sources": "Consumer panels, Retail data, Social media analysis, Industry surveys",
            "sample_size": 1200,
            "research_duration": "5 months",
            "research_budget": 65000,
            "reliability_score": "High",
            "key_findings": "<p>Initial research indicates strong preference for traditional health products and premium quality positioning.</p>"
        }
    ]
    
    for research_data in demo_research:
        if not frappe.db.exists("Market Research",
                               {"research_title": research_data["research_title"]}):
            research = frappe.new_doc("Market Research")
            research.update(research_data)
            research.save(ignore_permissions=True)
            print(f"Created market research: {research_data['research_title']}")

def import_regulatory_data():
    """Import sample regulatory data."""
    
    # This would import from the fixtures if available
    try:
        fixtures_path = os.path.join(frappe.get_app_path("sysmayal"), "sysmayal", "fixtures")
        country_reg_file = os.path.join(fixtures_path, "country_regulation.json")
        
        if os.path.exists(country_reg_file):
            with open(country_reg_file, 'r') as f:
                regulations = json.load(f)
                
            for reg_data in regulations:
                if not frappe.db.exists("Country Regulation", reg_data["name"]):
                    reg = frappe.new_doc("Country Regulation")
                    reg.update(reg_data)
                    reg.save(ignore_permissions=True)
                    print(f"Imported regulation for: {reg_data['country_name']}")
                    
    except Exception as e:
        print(f"Could not import regulatory data: {str(e)}")

def generate_demo_reports():
    """Generate sample reports to demonstrate functionality."""
    
    print("\nDemo Reports Available:")
    print("=" * 50)
    
    # Organization summary
    org_count = frappe.db.count("Distribution Organization")
    contact_count = frappe.db.count("Distribution Contact")
    project_count = frappe.db.count("Product Development Project")
    regulation_count = frappe.db.count("Country Regulation")
    compliance_count = frappe.db.count("Product Compliance")
    certificate_count = frappe.db.count("Certification Document")
    market_plan_count = frappe.db.count("Market Entry Plan")
    market_research_count = frappe.db.count("Market Research")
    
    print(f"Distribution Organizations: {org_count}")
    print(f"Distribution Contacts: {contact_count}")
    print(f"R&D Projects: {project_count}")
    print(f"Country Regulations: {regulation_count}")
    print(f"Product Compliance Records: {compliance_count}")
    print(f"Certification Documents: {certificate_count}")
    print(f"Market Entry Plans: {market_plan_count}")
    print(f"Market Research Studies: {market_research_count}")
    
    # Status breakdown
    print("\nOrganization Status:")
    statuses = frappe.db.sql("""
        SELECT status, COUNT(*) as count 
        FROM `tabDistribution Organization` 
        GROUP BY status
    """, as_dict=True)
    
    for status in statuses:
        print(f"  {status.status}: {status.count}")
        
    print("\nProject Status:")
    project_statuses = frappe.db.sql("""
        SELECT status, COUNT(*) as count 
        FROM `tabProduct Development Project` 
        GROUP BY status
    """, as_dict=True)
    
    for status in project_statuses:
        print(f"  {status.status}: {status.count}")

if __name__ == "__main__":
    # This script should be run from within a Frappe context
    print("Sysmayal Demo Setup")
    print("This script should be executed from within ERPNext using:")
    print("bench --site your-site.com execute sysmayal.scripts.demo_setup.setup_demo_data")
