# City of Burnaby - Municipality Profile

## 🏛️ Basic Information

| Field | Value |
|-------|-------|
| **Official Name** | City of Burnaby |
| **Region** | Metro Vancouver |
| **Population** | ~250,000 |
| **Team ID** | TEAM-BUR |
| **Tier** | 2 - High |
| **Calendar Color** | #00ACC1 (Cyan) |
| **Status** | Pending Setup |

---

## 🌐 Bid Portal Information

### Primary Portal: BidsAndTenders

| Field | Value |
|-------|-------|
| **Portal Name** | Burnaby Bids and Tenders |
| **Portal URL** | https://burnaby.bidsandtenders.ca/Module/Tenders |
| **Portal Type** | BidsAndTenders Platform |
| **Account Required** | Yes |
| **Username** | [TO BE CONFIGURED] |
| **Password** | [SECURE STORAGE] |
| **Registration URL** | https://burnaby.bidsandtenders.ca/Registration |

### Portal Features
- Email notifications
- Saved searches
- Document downloads
- Online Q&A
- Addenda tracking

### Relevant Categories to Monitor
- Signs & Signage
- Printing Services
- Parks & Recreation
- Public Works
- Construction

---

## 📋 Procurement Process

### Standard Requirements
- Business License (Burnaby or Inter-Municipal)
- WorkSafeBC Registration
- Insurance ($2M-$5M typical)
- References

---

## 📅 Calendar Configuration

| Field | Value |
|-------|-------|
| Calendar Name | BID-AI: City of Burnaby |
| Color | #00ACC1 (Cyan) |
| Event Prefix | `BUR-[YEAR]-[NUMBER]` |

---

## 🤖 Agent Team Configuration

```yaml
team_id: TEAM-BUR
municipality: City of Burnaby
tier: 2
priority: high

scout_agent:
  scan_interval: 30
  portal_url: https://burnaby.bidsandtenders.ca/Module/Tenders
  scraper_type: bidsandtenders

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
- Major municipality with significant parks and civic facilities
- Metrotown area represents high-visibility opportunities
- SFU campus adjacent - potential coordination

### Key Facilities
- Burnaby Lake Regional Park
- Central Park
- Burnaby Mountain
- Metrotown civic facilities
- Multiple community centers

---

## 🔗 Important Links

- **Portal:** https://burnaby.bidsandtenders.ca/Module/Tenders
- **City Website:** https://www.burnaby.ca/

---

*Profile Version: 1.0*  
*Last Updated: December 2025*
