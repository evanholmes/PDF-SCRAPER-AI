# BID-AI Visualization Dashboard Design

## 🎯 Overview

The BID-AI Dashboard serves as the command center for THE PARENT COMPANY's bidding operations. It provides real-time visibility into all bid opportunities, agent team activities, and pipeline performance.

---

## 👤 User Roles & Views

### 1. CEO Dashboard
**Primary User:** Company CEO  
**Purpose:** Strategic oversight and business intelligence

### 2. BID MASTER Console
**Primary User:** THE BID MASTER AI  
**Purpose:** Operational command and control

### 3. Team View
**Primary User:** Municipal Agent Teams  
**Purpose:** Focused execution on assigned bids

---

## 🖥️ CEO Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  BID-AI                                 [CEO View]    🔔 3        👤 CEO Logout │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │                         EXECUTIVE SUMMARY                                   ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       ││
│  │  │ ACTIVE   │  │ PENDING  │  │ SUBMITTED│  │ WON THIS │  │ WIN RATE │       ││
│  │  │ BIDS     │  │ DECISION │  │ AWAITING │  │ QUARTER  │  │          │       ││
│  │  │    12    │  │    5     │  │    3     │  │ $245K    │  │   34%    │       ││
│  │  │ ↑2 today │  │          │  │          │  │ 4 wins   │  │ ↑5% YoY  │       ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘       ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                                                                 │
│  ┌────────────────────────────────────┐  ┌────────────────────────────────────┐ │
│  │      UPCOMING DEADLINES            │  │        BID PIPELINE                │ │
│  │  ┌─────────────────────────────┐   │  │                                    │ │
│  │  │ 🚨 Dec 20 - Surrey Transit  │   │  │    Discovery    Analysis    Draft  │ │
│  │  │    Signs - 2 DAYS LEFT      │   │  │        │          │           │    │ │
│  │  ├─────────────────────────────┤   │  │       ●●●        ●●        ●●● ●●● │ │
│  │  │ ⏰ Dec 23 - Vancouver Park  │   │  │        8          4          6     │ │
│  │  │    Wayfinding - 5 days      │   │  │                                    │ │
│  │  ├─────────────────────────────┤   │  │    Review     Submit    Awarded    │ │
│  │  │ 📝 Dec 28 - Burnaby Civic   │   │  │        │         │          │      │ │
│  │  │    Signage - 10 days        │   │  │       ●●        ●●●         ●●     │ │
│  │  └─────────────────────────────┘   │  │        3          5          4     │ │
│  │  [View All →]                      │  │                                    │ │
│  └────────────────────────────────────┘  └────────────────────────────────────┘ │
│                                                                                 │
│  ┌────────────────────────────────────┐  ┌────────────────────────────────────┐ │
│  │      GEOGRAPHIC DISTRIBUTION       │  │      AGENT TEAM STATUS             │ │
│  │                                    │  │                                    │ │
│  │    [Interactive Map of GVA/FV]     │  │  Vancouver  ████████░░  8 active   │ │
│  │                                    │  │  Surrey     ██████░░░░  6 active   │ │
│  │    ● Vancouver (4)                 │  │  Burnaby    ████░░░░░░  4 active   │ │
│  │    ● Surrey (3)                    │  │  Metro Van  ███░░░░░░░  3 active   │ │
│  │    ● Burnaby (2)                   │  │  Richmond   ██░░░░░░░░  2 active   │ │
│  │    ● Metro Van (2)                 │  │  Langley    ██░░░░░░░░  2 active   │ │
│  │    ● Other (1)                     │  │  [+18 more teams]                  │ │
│  │                                    │  │                                    │ │
│  └────────────────────────────────────┘  └────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐│
│  │                     BID MASTER ACTIVITY LOG                                 ││
│  │  ───────────────────────────────────────────────────────────────────────    ││
│  │  10:34 AM  🤖 Approved proposal for Surrey Transit Signs - Ready to submit  ││
│  │  10:12 AM  📋 New opportunity detected: Richmond City Hall Wayfinding       ││
│  │  09:45 AM  ✅ Submitted bid: Vancouver Park Regulatory Signs                ││
│  │  09:30 AM  🔍 Analyzed: Coquitlam Trail Signage - Recommend GO              ││
│  │  [View Full Log →]                                                          ││
│  └─────────────────────────────────────────────────────────────────────────────┘│
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 BID MASTER Console Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  BID-AI                              [BID MASTER CONSOLE]              🔔 12    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│  │   COMMAND CENTER        │  │            ACTIVE OPERATIONS                │   │
│  │                         │  │                                             │   │
│  │  Monitoring: 31 portals │  │  ┌─────────────────────────────────────────┐│   │
│  │  Active Teams: 24       │  │  │ PRIORITY QUEUE                          ││   │
│  │  Bids in Progress: 18   │  │  │                                         ││   │
│  │  Awaiting Decision: 7   │  │  │ 1. 🔴 Surrey Transit - SUBMIT TODAY     ││   │
│  │                         │  │  │ 2. 🟠 Vancouver Park - Review needed    ││   │
│  │  ┌───────────────────┐  │  │  │ 3. 🟡 Burnaby Civic - Draft 80%         ││   │
│  │  │ QUICK ACTIONS     │  │  │  │ 4. 🟢 Richmond City - Analysis phase    ││   │
│  │  │                   │  │  │  │ 5. 🔵 Langley Trail - New opportunity   ││   │
│  │  │ [Scan All Portals]│  │  │  └─────────────────────────────────────────┘│   │
│  │  │ [Review Queue]    │  │  │                                             │   │
│  │  │ [Generate Report] │  │  │  ┌─────────────────────────────────────────┐│   │
│  │  │ [Message CEO]     │  │  │  │ NEW OPPORTUNITIES (Last 24h)            ││   │
│  │  └───────────────────┘  │  │  │                                         ││   │
│  │                         │  │  │ • Richmond Wayfinding - $85K est        ││   │
│  └─────────────────────────┘  │  │ • Chilliwack Park Signs - $25K est      ││   │
│                               │  │ • TransLink Shelter - $120K est         ││   │
│  ┌─────────────────────────┐  │  │                                         ││   │
│  │  TEAM DEPLOYMENT        │  │  │ [Analyze All] [Dismiss Non-Relevant]    ││   │
│  │                         │  │  └─────────────────────────────────────────┘│   │
│  │  ┌─ Vancouver ────────┐ │  │                                             │   │
│  │  │ Scout: Active ✓    │ │  └─────────────────────────────────────────────┘   │
│  │  │ Analyst: Working   │ │                                                    │
│  │  │ Writer: Drafting   │ │  ┌─────────────────────────────────────────────┐   │
│  │  │ Compliance: Ready  │ │  │            DECISION QUEUE                   │   │
│  │  └────────────────────┘ │  │                                             │   │
│  │                         │  │  Bid: Vancouver Park Regulatory Signs       │   │
│  │  ┌─ Surrey ───────────┐ │  │  Value: $45,000 | Win Prob: 62%             │   │
│  │  │ Scout: Active ✓    │ │  │  Deadline: Dec 23, 2025                     │   │
│  │  │ Analyst: Complete  │ │  │  Status: Analysis Complete                  │   │
│  │  │ Writer: Complete   │ │  │                                             │   │
│  │  │ Compliance: Review │ │  │  Recommendation: GO                         │   │
│  │  └────────────────────┘ │  │  Rationale: Strong alignment with past      │   │
│  │                         │  │  work; similar scope to successful 2023     │   │
│  │  [+22 more teams...]    │  │  Stanley Park project.                      │   │
│  │                         │  │                                             │   │
│  └─────────────────────────┘  │  [✓ APPROVE GO] [✗ NO-BID] [? MORE INFO]    │   │
│                               └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Key Dashboard Components

### 1. Executive Summary Cards

| Card | Metric | Purpose |
|------|--------|---------|
| Active Bids | Count + trend | Current workload |
| Pending Decision | Count | Awaiting outcomes |
| Submitted | Count | In evaluation |
| Won This Quarter | $ value + count | Performance |
| Win Rate | % + trend | Effectiveness |


### 2. Pipeline Kanban Board

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│  DISCOVERY  │  ANALYSIS   │   DRAFT     │   REVIEW    │   SUBMIT    │   RESULT    │
│             │             │             │             │             │             │
│  ┌───────┐  │  ┌───────┐  │  ┌───────┐  │  ┌───────┐  │  ┌───────┐  │  ┌───────┐  │
│  │ Bid 1 │  │  │ Bid 3 │  │  │ Bid 5 │  │  │ Bid 7 │  │  │ Bid 9 │  │  │ WON   │  │
│  │ $45K  │  │  │ $80K  │  │  │ $35K  │  │  │ $120K │  │  │ $55K  │  │  │ Bid 11│  │
│  └───────┘  │  └───────┘  │  └───────┘  │  └───────┘  │  └───────┘  │  └───────┘  │
│  ┌───────┐  │  ┌───────┐  │  ┌───────┐  │             │  ┌───────┐  │  ┌───────┐  │
│  │ Bid 2 │  │  │ Bid 4 │  │  │ Bid 6 │  │             │  │ Bid 10│  │  │ LOST  │  │
│  │ $25K  │  │  │ $60K  │  │  │ $90K  │  │             │  │ $40K  │  │  │ Bid 12│  │
│  └───────┘  │  └───────┘  │  └───────┘  │             │  └───────┘  │  └───────┘  │
│             │             │             │             │             │             │
│     8       │     4       │     6       │     3       │     5       │    12       │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```


### 3. Geographic Map View

Interactive map showing:
- Municipality boundaries
- Active bid locations (markers)
- Bid density heat map
- Win/loss history by area
- Team assignment zones

### 4. Calendar Integration Widget

Embedded Google Calendar showing:
- 7-day rolling view
- Color-coded by municipality
- Deadline highlights
- Quick-add capability

### 5. Agent Team Status Panel

Real-time agent status:
```
Vancouver Team
├── 🟢 Scout Agent      - Last scan: 5 min ago
├── 🟡 Analyst Agent    - Working on: VAN-2025-127
├── 🔵 Writer Agent     - Drafting: VAN-2025-125
└── 🟢 Compliance Agent - Ready
```

### 6. Activity Feed

Real-time log of:
- New opportunities detected
- Analysis completions
- Proposal submissions
- Status changes
- Win/loss notifications

---

## 📱 Responsive Design

### Desktop (1920px+)
- Full dashboard with all panels
- Side-by-side layouts
- Expanded data tables

### Laptop (1024px - 1919px)
- Condensed layout
- Collapsible panels
- Tabbed navigation for sections

### Tablet (768px - 1023px)
- Stacked layout
- Priority content first
- Touch-optimized controls

### Mobile (< 768px)
- Single column
- Critical metrics only
- Swipe navigation
- Quick actions prominent

---

## 🎨 Visual Design System

### Color Palette

| Purpose | Color | Hex     |
|---------|-------|---------|
| Primary | Blue  | #2563EB |
| Success | Green | #16A34A |
| Warning | Amber | #F59E0B |
| Danger  | Red   | #DC2626 |
| Info    | Cyan  | #0891B2 |
| Neutral | Slate | #64748B |

### Status Colors

| Status | Color | Usage |
|--------|-------|-------|
| Discovery | Blue | New opportunities |
| Analysis | Purple | Being evaluated |
| Drafting | Yellow | Proposal in progress |
| Review | Orange | Awaiting approval |
| Submitted | Green | Sent to municipality |
| Won | Green (bold) | Contract awarded |
| Lost | Red | Not selected |
| No-Bid | Gray | Declined to bid |

### Typography

- **Headings:** Inter Bold
- **Body:** Inter Regular
- **Monospace:** JetBrains Mono (for IDs, data)

---

## 🔔 Notification System

### Alert Types

| Priority | Trigger | Channel |
|----------|---------|---------|
| Critical | Deadline < 24h | Push + Email + Dashboard |
| High | New high-value opportunity | Push + Dashboard |
| Medium | Status change | Dashboard |
| Low | Informational | Dashboard only |

### Notification Panel

```
┌─────────────────────────────────────┐
│  🔔 Notifications (3 unread)        │
├─────────────────────────────────────┤
│  🔴 URGENT - 2 hours ago            │
│  Surrey Transit deadline in 24h     │
│  [View Bid] [Mark Read]             │
├─────────────────────────────────────┤
│  🟠 HIGH - 4 hours ago              │
│  New opportunity: Richmond $85K     │
│  [Analyze] [Dismiss]                │
├─────────────────────────────────────┤
│  🟢 INFO - 6 hours ago              │
│  Bid VAN-2025-125 submitted         │
│  [View Details]                     │
└─────────────────────────────────────┘
```

---

## 📈 Analytics & Reporting

### Standard Reports

1. **Pipeline Report**
   - All active bids by stage
   - Expected close dates
   - Value projections

2. **Win/Loss Analysis**
   - Win rate by municipality
   - Win rate by bid type
   - Competitor analysis

3. **Performance Dashboard**
   - Bids submitted vs. opportunities
   - Response time metrics
   - Team productivity

4. **Financial Report**
   - Revenue from contracts
   - Pipeline value
   - ROI on bidding efforts

### Custom Report Builder

Allow CEO to build custom reports with:
- Date range selection
- Municipality filters
- Bid type filters
- Value range filters
- Export options (PDF, Excel, CSV)

---

## 🛠️ Technical Implementation

### Frontend Stack
```
- Framework: Next.js 14 (App Router)
- UI Library: shadcn/ui + Tailwind CSS
- State: Zustand
- Charts: Recharts
- Maps: Mapbox GL JS
- Calendar: react-big-calendar
- Tables: TanStack Table
```

### Key Components

```
/components
├── dashboard/
│   ├── ExecutiveSummary.tsx
│   ├── PipelineKanban.tsx
│   ├── GeographicMap.tsx
│   ├── CalendarWidget.tsx
│   ├── TeamStatus.tsx
│   └── ActivityFeed.tsx
├── bids/
│   ├── BidCard.tsx
│   ├── BidDetail.tsx
│   └── BidTimeline.tsx
├── teams/
│   ├── TeamCard.tsx
│   └── AgentStatus.tsx
└── shared/
    ├── StatusBadge.tsx
    ├── PriorityIndicator.tsx
    └── NotificationPanel.tsx
```

### Data Refresh Strategy

| Component | Refresh Rate | Method |
|-----------|--------------|--------|
| Metrics | 30 seconds | Polling |
| Pipeline | 1 minute | Polling |
| Activity | Real-time | WebSocket |
| Calendar | 5 minutes | Polling |
| Teams | 15 seconds | Polling |

---

## 🔐 Access Control

### Permission Matrix

| Feature | CEO | BID MASTER | Team     |
|---------|-----|------------|----------|
| View all bids | ✅ | ✅    | Own only |
| Approve bids  | ✅ | ✅    | ❌       |
| View analytics| ✅ | ✅    | Limited  |
| Manage teams  | ✅ | ✅    | ❌       |
| System config | ✅ | ❌    | ❌       |
-----------------------------------------
---

*Dashboard Design Version: 1.0*
*Last Updated: December 2025*
