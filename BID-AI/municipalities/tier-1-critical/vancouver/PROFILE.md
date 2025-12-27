# City of Vancouver - Municipality Profile

## 🏛️ Basic Information

| Field | Value |
|-------|-------|
| **Official Name** | City of Vancouver |
| **Region** | Metro Vancouver |
| **Population** | ~700,000 |
| **Team ID** | TEAM-VAN |
| **Tier** | 1 - Critical |
| **Calendar Color** | #F4B400 (Yellow) |
| **Status** | Active |

---

## 🌐 Bid Portal Information

### Primary Portal: VendorLink

| Field | Value |
|-------|-------|
| **Portal Name** | Vancouver VendorLink |
| **Portal URL** | https://vancouver.vendorlink.ca/ |
| **Portal Type** | VendorLink Platform |
| **Account Required** | Yes |
| **Username** | [TO BE CONFIGURED] |
| **Password** | [SECURE STORAGE] |
| **Registration URL** | https://vancouver.vendorlink.ca/registration |

### Portal Features
- Email notifications for new opportunities
- Saved search functionality
- Document download
- Online Q&A submission
- Electronic bid submission

### Relevant Categories to Monitor
- Signs & Signage
- Printing Services
- Construction - General
- Parks & Recreation
- Transportation

---

## 📋 Procurement Process

### Bid Types Used
- **RFP** (Request for Proposal) - Complex projects, weighted evaluation
- **RFQ** (Request for Quote) - Simpler projects, price-focused
- **ITT** (Invitation to Tender) - Formal tender process
- **RFSQ** (Request for Supplier Qualifications) - Pre-qualification

### Typical Evaluation Criteria

| Criteria | Typical Weight |
|----------|----------------|
| Technical Approach | 30-40% |
| Experience & Qualifications | 20-30% |
| Price | 25-35% |
| Schedule | 5-10% |
| Local Preference | 0-5% |

### Standard Requirements
- Business License (City of Vancouver or Inter-Municipal)
- WorkSafeBC Coverage
- Insurance ($2M-$5M typical)
- References (3-5 required)
- WCB Clearance Letter

---

## 📅 Calendar Configuration

### Google Calendar Details
| Field | Value |
|-------|-------|
| Calendar Name | BID-AI: City of Vancouver |
| Calendar ID | [TO BE CREATED] |
| Color | #F4B400 (Yellow) |
| Time Zone | America/Vancouver |

### Event Prefix
All events use prefix: `VAN-[YEAR]-[NUMBER]`  
Example: `VAN-2025-127`

---

## 🤖 Agent Team Configuration

### Team: TEAM-VAN

```yaml
team_id: TEAM-VAN
municipality: City of Vancouver
tier: 1
priority: critical

scout_agent:
  scan_interval: 15  # minutes
  portal_url: https://vancouver.vendorlink.ca/
  keywords_profile: extended
  alert_threshold: 35
  categories:
    - Signs & Signage
    - Printing Services
    - Parks & Recreation
    - Construction

analyst_agent:
  priority_processing: true
  deep_analysis: true
  capability_threshold: 0.65
  auto_recommend: false  # Requires BID MASTER review

writer_agent:
  template_set: vancouver-custom
  tone: professional-civic
  include_local_references: true

compliance_agent:
  checklist: vancouver-standard
  multi_reviewer: true
  insurance_minimum: 2000000
```

---

## 🏢 Key Departments & Contacts

### Procurement Services
- **Department:** Supply Chain Management
- **General Inquiries:** procurement@vancouver.ca
- **Website:** https://vancouver.ca/doing-business/selling-to-the-city.aspx

### Relevant Departments for Signage
- **Engineering Services** - Street signage, traffic signs
- **Parks & Recreation** - Park wayfinding, trail signs
- **Planning & Development** - Civic facility signage
- **Transportation** - Transit-related signage

---

## 📊 Historical Data

### Past Signage/Printing Opportunities (Known)
| Year | Opportunity | Value | Outcome |
|------|-------------|-------|---------|
| 2025 | TBD | TBD | TBD |
| 2023 | TBD | TBD | TBD |

*To be populated as data is gathered*

### Win/Loss Record
| Metric | Value |
|--------|-------|
| Total Bids Submitted | 0 |
| Wins | 0 |
| Losses | 0 |
| Win Rate | N/A |

---

## 📁 Folder Contents

```
vancouver/
├── PROFILE.md (this file)
├── portal-docs/
│   ├── vendor-registration-guide.pdf
│   ├── procurement-policy.pdf
│   └── standard-terms-conditions.pdf
├── bids-active/
│   └── [active bid folders]
├── bids-archive/
│   └── [completed/passed bid folders]
├── proposals/
│   └── [submitted proposals]
├── templates/
│   └── vancouver-proposal-template.md
└── research/
    ├── department-contacts.md
    ├── historical-contracts.md
    └── competitor-analysis.md
```

---

## 🔗 Important Links

- **Main Procurement Page:** https://vancouver.ca/doing-business/selling-to-the-city.aspx
- **VendorLink Portal:** https://vancouver.vendorlink.ca/
- **Vendor Registration:** https://vancouver.vendorlink.ca/registration
- **Current Opportunities:** https://vancouver.vendorlink.ca/opportunities
- **Awarded Contracts:** https://vancouver.ca/doing-business/awarded-contracts.aspx

---

## 📝 Notes & Intelligence

### Strategic Importance
Vancouver is the largest city in the region and represents the highest volume of signage opportunities. Key focus areas include:
- **Parks & Recreation:** Extensive park system with ongoing wayfinding needs
- **Olympic Village:** Ongoing signage maintenance and updates
- **Downtown Core:** High-visibility civic signage projects
- **Transit Integration:** Coordination with TransLink signage

### Competitive Landscape
- High competition from established local sign companies
- Preference for vendors with City of Vancouver experience
- Sustainability and accessibility requirements increasingly important

### Opportunity Patterns
- Park signage projects typically post in Q1-Q2
- Traffic/regulatory signage year-round
- Large facility projects often Q3-Q4 for budget allocation

---

*Profile Version: 1.0*  
*Last Updated: December 2025*  
*Next Review: January 2025*
