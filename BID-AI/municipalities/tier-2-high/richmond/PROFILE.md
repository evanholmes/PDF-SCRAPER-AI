# City of Richmond - Municipality Profile

## 🏛️ Basic Information

| Field | Value |
|-------|-------|
| **Official Name** | City of Richmond |
| **Region** | Metro Vancouver |
| **Population** | ~225,000 |
| **Team ID** | TEAM-RIC |
| **Tier** | 2 - High |
| **Calendar Color** | #FF7043 (Deep Orange) |
| **Status** | Pending Setup |

---

## 🌐 Bid Portal Information

### Primary Portal: City of Richmond Website

| Field | Value |
|-------|-------|
| **Portal Name** | Purchasing & Tenders |
| **Portal URL** | https://www.richmond.ca/busdev/tenders/tenders.htm |
| **Portal Type** | Direct Website |
| **Account Required** | To Be Verified |
| **Username** | [TO BE CONFIGURED] |
| **Password** | [SECURE STORAGE] |

### Portal Features
- Direct document downloads
- Vendor registration system
- Contact per tender

### Relevant Categories to Monitor
- General Construction
- Parks & Recreation
- Transportation
- Facilities

---

## 📋 Procurement Process

### Standard Requirements
- Business License
- WorkSafeBC Registration
- Insurance ($2M-$5M typical)
- References

---

## 📅 Calendar Configuration

| Field | Value |
|-------|-------|
| Calendar Name | BID-AI: City of Richmond |
| Color | #FF7043 (Deep Orange) |
| Event Prefix | `RIC-[YEAR]-[NUMBER]` |

---

## 🤖 Agent Team Configuration

```yaml
team_id: TEAM-RIC
municipality: City of Richmond
tier: 2
priority: high

scout_agent:
  scan_interval: 30
  portal_url: https://www.richmond.ca/busdev/tenders/tenders.htm
  scraper_type: direct_website

analyst_agent:
  standard_processing: true

writer_agent:
  template_set: standard

compliance_agent:
  checklist: standard
```

---

## 📝 Notes & Intelligence

### Strategic Importance
- Airport city (YVR) - high-profile signage needs
- Significant development activity
- Olympic Oval and major recreation facilities
- Steveston historic district

### Key Facilities
- Richmond Olympic Oval
- Minoru Park Complex
- Steveston waterfront
- City Centre developments
- Multiple community centers

### Multilingual Considerations
- Large Chinese-speaking population
- Multilingual signage often required
- Additional design complexity = opportunity

---

## 🔗 Important Links

- **Portal:** https://www.richmond.ca/busdev/tenders/tenders.htm
- **City Website:** https://www.richmond.ca/

---

*Profile Version: 1.0*  
*Last Updated: December 2025*
