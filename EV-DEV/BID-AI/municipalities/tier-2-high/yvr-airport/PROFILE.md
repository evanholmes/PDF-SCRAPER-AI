# Vancouver Airport Authority (YVR) - Profile

## 🏛️ Basic Information

| Field | Value |
|-------|-------|
| **Official Name** | Vancouver Airport Authority |
| **Facility** | Vancouver International Airport (YVR) |
| **Type** | Airport Authority (Non-profit) |
| **Team ID** | TEAM-YVR |
| **Tier** | 2 - High |
| **Calendar Color** | #6A1B9A (Deep Purple) |
| **Status** | Priority |

---

## 🌐 Bid Portal Information

### Primary Portal: YVR Procurement

| Field | Value |
|-------|-------|
| **Portal Name** | YVR Procurement |
| **Portal URL** | https://www.yvr.ca/en/business/procurement |
| **Portal Type** | Custom Portal |
| **Account Required** | Yes |
| **Username** | [TO BE CONFIGURED] |
| **Password** | [SECURE STORAGE] |

### Secondary Sources
- MERX (for larger procurements)
- Direct vendor outreach

---

## ✈️ Facility Overview

### YVR Statistics
- **Passengers:** 25+ million annually (pre-pandemic peak)
- **Size:** One of Canada's largest airports
- **Terminals:** Domestic, International, South Terminal
- **Recognition:** Repeatedly voted Best Airport in North America

### Signage Inventory
| Area | Signage Types |
|------|---------------|
| Terminals | Wayfinding, gate signs, retail, regulatory |
| Curbside | Traffic, directional, pickup/dropoff |
| Parking | Wayfinding, level identification, payment |
| Airside | Regulatory, safety, operational |
| Retail | Tenant signage, advertising |

---

## 📅 Calendar Configuration

| Field | Value |
|-------|-------|
| Calendar Name | BID-AI: YVR Airport |
| Color | #6A1B9A (Deep Purple) |
| Event Prefix | `YVR-[YEAR]-[NUMBER]` |

---

## 🤖 Agent Team Configuration

```yaml
team_id: TEAM-YVR
municipality: Vancouver Airport Authority
tier: 2
priority: high
type: airport_authority

scout_agent:
  scan_interval: 30
  portal_url: https://www.yvr.ca/en/business/procurement
  scraper_type: custom
  merx_monitoring: true

analyst_agent:
  standard_processing: true
  security_considerations: true
  large_facility: true

compliance_agent:
  security_clearance: required
  insurance_minimum: 5000000
```

---

## 📝 Notes & Intelligence

### Strategic Importance
- **High-Profile:** Award-winning airport with high design standards
- **Volume:** Extensive signage throughout massive facility
- **Premium:** High-quality materials and installation expected
- **Recurring:** Ongoing maintenance and refresh programs
- **Expansion:** Terminal expansion projects

### Key Considerations
- **Security:** Airport security clearance required for workers
- **Quality:** Premium materials and craftsmanship expected
- **Brand:** Strict adherence to YVR brand guidelines
- **Accessibility:** Full accessibility compliance required
- **Multilingual:** English/French minimum, often more languages

### Contract Types
- Wayfinding system updates
- Terminal refresh projects
- Retail tenant signage programs
- Parking facility signage
- Curbside management signage
- Construction/renovation projects

---

## 🔗 Important Links

- **Procurement:** https://www.yvr.ca/en/business/procurement
- **YVR Website:** https://www.yvr.ca/
- **Business at YVR:** https://www.yvr.ca/en/business

---

*Profile Version: 1.0 | Last Updated: December 2025*
