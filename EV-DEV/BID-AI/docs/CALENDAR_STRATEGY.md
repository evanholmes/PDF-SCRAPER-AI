# Calendar Integration Strategy

## 🎯 Overview

BID-AI utilizes Google Calendar as the central scheduling and tracking system for all bid opportunities across municipalities. Each municipality has its own color-coded calendar, allowing for clear visual organization and easy filtering.

---

## 📅 Calendar Structure

### Master Calendar Hierarchy

```
BID-AI Calendar System
│
├── 🔷 BID-AI Master (Aggregate View)
│   └── Subscribe to all municipal calendars
│   └── CEO primary view
│
├── 📁 REGIONAL DISTRICTS
│   ├── 📅 Metro Vancouver (#4285F4 - Blue)
│   └── 📅 Fraser Valley Regional District (#0F9D58 - Green)
│
├── 📁 METRO VANCOUVER CITIES
│   ├── 📅 City of Vancouver (#F4B400 - Yellow)
│   ├── 📅 City of Surrey (#AB47BC - Purple)
│   ├── 📅 City of Burnaby (#00ACC1 - Cyan)
│   ├── 📅 City of Richmond (#FF7043 - Deep Orange)
│   ├── 📅 City of Coquitlam (#9CCC65 - Light Green)
│   ├── 📅 City of New Westminster (#26A69A - Teal)
│   ├── 📅 City of Delta (#5C6BC0 - Indigo)
│   ├── 📅 City of North Vancouver (#EF5350 - Red)
│   ├── 📅 District of North Vancouver (#EC407A - Pink)
│   ├── 📅 City of West Vancouver (#7E57C2 - Deep Purple)
│   ├── 📅 City of Port Coquitlam (#42A5F5 - Light Blue)
│   ├── 📅 City of Port Moody (#66BB6A - Green)
│   └── 📅 City of White Rock (#80DEEA - Cyan Light)
│
├── 📁 FRASER VALLEY CITIES
│   ├── 📅 City of Langley (#FFCA28 - Amber)
│   ├── 📅 Township of Langley (#FFA726 - Orange)
│   ├── 📅 City of Abbotsford (#8D6E63 - Brown)
│   ├── 📅 City of Chilliwack (#78909C - Blue Grey)
│   ├── 📅 City of Mission (#A1887F - Brown Light)
│   ├── 📅 District of Maple Ridge (#90A4AE - Grey)
│   ├── 📅 City of Pitt Meadows (#BCAAA4 - Brown Lighter)
│   ├── 📅 District of Hope (#B0BEC5 - Grey Light)
│   └── 📅 Village of Harrison Hot Springs (#D7CCC8 - Brown Lightest)
│
└── 📁 SPECIAL AGENCIES
    ├── 📅 Port of Vancouver (#DB4437 - Red Dark)
    ├── 📅 TransLink (#C62828 - Red Deep)
    ├── 📅 Vancouver Airport Authority (#6A1B9A - Purple Deep)
    ├── 📅 BC Hydro (#1565C0 - Blue Dark)
    ├── 📅 BC Ferries (#00838F - Cyan Dark)
    ├── 📅 UBC (#2E7D32 - Green Dark)
    └── 📅 SFU (#F57F17 - Yellow Dark)
```

---

## 🎨 Color Coding System

### Calendar Colors (by Municipality)

| Municipality | Hex Color | Visual |
|--------------|-----------|--------|
| Metro Vancouver | #4285F4 | 🔵 |
| FVRD | #0F9D58 | 🟢 |
| Vancouver | #F4B400 | 🟡 |
| Surrey | #AB47BC | 🟣 |
| Burnaby | #00ACC1 | 🔵 |
| Richmond | #FF7043 | 🟠 |
| Port of Vancouver | #DB4437 | 🔴 |
| TransLink | #C62828 | 🔴 |
| YVR | #6A1B9A | 🟣 |

### Event Type Indicators (Emoji Prefixes)

| Emoji | Event Type | Description |
|-------|------------|-------------|
| 🆕 | New Opportunity | Bid just posted |
| ❓ | Q&A Period | Questions can be submitted |
| ⏰ | Q&A Deadline | Last day for questions |
| 📝 | Addendum Posted | Amendment to bid documents |
| 🚨 | Submission Deadline | CRITICAL - bid due |
| 📋 | Site Visit | Mandatory or optional site visit |
| 📣 | Award Expected | Anticipated decision date |
| ✅ | Awarded | Contract decision made |
| ❌ | Closed - No Bid | Opportunity passed |

---

## 📆 Event Formatting Standards

### Event Title Format
```
[Emoji] [Bid ID] - [Brief Description] - [Municipality]
```

**Examples:**
- `🆕 VAN-2025-127 - Park Wayfinding Signage - Vancouver`
- `🚨 SUR-RFP-2025-89 - Transit Shelter Signs - Surrey`
- `❓ MV-T-2025-45 - Regulatory Signage - Metro Van`

### Event Description Template
```
📋 BID DETAILS
━━━━━━━━━━━━━━━━━━━━━━━
Bid ID: [Official Reference Number]
Title: [Full Title]
Municipality: [Full Name]
Type: [RFP/RFQ/Tender]
Estimated Value: $[Amount] (if known)

📅 KEY DATES
━━━━━━━━━━━━━━━━━━━━━━━
Posted: [Date]
Q&A Deadline: [Date]
Submission Deadline: [Date & Time]
Award Expected: [Date] (if known)

🔗 LINKS
━━━━━━━━━━━━━━━━━━━━━━━
Portal: [URL]
Documents: [URL]

📊 STATUS
━━━━━━━━━━━━━━━━━━━━━━━
Decision: [GO/NO-GO/PENDING]
Team Lead: [Agent/Team Name]
Priority: [HIGH/MEDIUM/LOW]

📝 NOTES
━━━━━━━━━━━━━━━━━━━━━━━
[Any relevant notes]
```

---

## ⏰ Reminder Strategy

### Automated Reminders

| Event Type | Reminder 1 | Reminder 2 | Reminder 3 |
|------------|------------|------------|------------|
| Submission Deadline | 7 days | 3 days | 1 day |
| Q&A Deadline | 3 days | 1 day | 4 hours |
| Site Visit | 3 days | 1 day | 2 hours |
| Award Expected | 1 day | Morning of | - |

### Escalation Path

1. **7 Days Before Deadline**
   - Standard team notification
   - Proposal draft should be 75% complete

2. **3 Days Before Deadline**
   - BID MASTER review required
   - All sections must be complete

3. **1 Day Before Deadline**
   - Final CEO review (if required)
   - Compliance check completed
   - Submission package ready

4. **Day of Deadline**
   - Final submission confirmation
   - Backup submission plan activated if needed

---

## 🔄 Integration Workflow

### New Bid Discovery Flow

```
Scout Agent Detects Bid
         │
         ▼
┌─────────────────────┐
│ Create Calendar     │
│ Event: 🆕 New Opp   │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Add all known dates │
│ to municipality     │
│ calendar            │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Set appropriate     │
│ reminders           │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Notify BID MASTER   │
│ via calendar invite │
└─────────────────────┘
```

### Status Update Flow

```
Status Change Occurs
         │
         ▼
┌─────────────────────┐
│ Update event emoji  │
│ (🆕 → ❓ → 🚨 → ✅)  │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Update event        │
│ description         │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ Trigger appropriate │
│ notifications       │
└─────────────────────┘
```

---

## 📱 Google Calendar API Implementation

### Required Scopes
```
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/calendar.events
```

### Key Operations

```python
# Create Municipality Calendar
def create_municipality_calendar(name, color_id):
    calendar = {
        'summary': f'BID-AI: {name}',
        'timeZone': 'America/Vancouver'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    
    # Set color
    calendar_list_entry = {
        'colorId': color_id
    }
    service.calendarList().update(
        calendarId=created_calendar['id'],
        body=calendar_list_entry
    ).execute()
    
    return created_calendar

# Create Bid Event
def create_bid_event(calendar_id, bid_data):
    event = {
        'summary': f"🚨 {bid_data['id']} - {bid_data['title']}",
        'description': format_bid_description(bid_data),
        'start': {
            'dateTime': bid_data['deadline'],
            'timeZone': 'America/Vancouver',
        },
        'end': {
            'dateTime': bid_data['deadline'],
            'timeZone': 'America/Vancouver',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 10080},  # 7 days
                {'method': 'email', 'minutes': 4320},   # 3 days
                {'method': 'popup', 'minutes': 1440},   # 1 day
            ],
        },
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()
```

---

## 📊 Calendar Views

### CEO Dashboard View
- All calendars visible
- Filter by:
  - Priority (High/Medium/Low)
  - Status (Active/Pending/Closed)
  - Value (>$100K, $50K-$100K, <$50K)
  - Municipality
  - Event Type

### Team View
- Single municipality calendar
- Detailed task assignments
- Deadline focus

### BID MASTER View
- All calendars with priority overlay
- Resource allocation view
- Conflict detection

---

## 🔐 Access Permissions

| Role | Access Level |
|------|--------------|
| CEO | Full read/write to all calendars |
| BID MASTER | Full read/write to all calendars |
| Municipal Team | Read/write to assigned calendar only |
| System | API access for automation |

---

## 📋 Implementation Checklist

- [ ] Create Google Workspace service account
- [ ] Set up OAuth credentials
- [ ] Create master calendar
- [ ] Create all municipality calendars (31)
- [ ] Apply color coding
- [ ] Set up calendar sharing
- [ ] Implement API integration
- [ ] Create event templates
- [ ] Configure reminder rules
- [ ] Test notification flow
- [ ] Document calendar IDs in config

---

*Calendar Strategy Version: 1.0*
*Last Updated: December 2025*
