# TASK PRP Example: User Dashboard with Analytics

**Type**: TASK PRP (Task Breakdown)
**Complexity**: Medium
**Use Case**: Breaking complex feature into manageable tasks

---

## Project Description

Implement a user dashboard showing analytics:
- Profile stats (join date, last active, account status)
- Activity metrics (posts, comments, likes over time)
- Data visualization (charts showing trends)
- Export functionality (download data as CSV)

## Critical Context

```yaml
patterns:
  - file: src/components/AdminDashboard.tsx
    copy: Layout and data fetching pattern

  - file: src/api/users.ts
    copy: API endpoint structure

gotchas:
  - issue: "Chart library requires data in specific format"
    fix: "Transform API response before passing to Chart component"

  - issue: "CSV export fails on large datasets (>10k rows)"
    fix: "Implement server-side export, don't generate client-side"
```

## Task List

### Phase 1: Database & API

```yaml
Task 1: Create Analytics Data Model
STATUS [ ]
CREATE src/models/user_analytics.ts:
  - MIRROR pattern from: src/models/user_stats.ts
  - ADD fields: date, posts_count, comments_count, likes_count
  - KEEP: timestamp fields (created_at, updated_at)
VALIDATE: npm run typecheck

Task 2: Create Analytics API Endpoint
STATUS [ ]
CREATE src/api/analytics.ts:
  - MIRROR pattern from: src/api/users.ts (endpoint structure)
  - IMPLEMENT: GET /api/users/{id}/analytics
  - INCLUDE: Query params for date range (start_date, end_date)
VALIDATE: curl http://localhost:3000/api/users/1/analytics?start_date=2024-01-01
IF_FAIL: Check database connection, verify user exists
```

### Phase 2: Data Visualization

```yaml
Task 3: Install Chart Library
STATUS [ ]
UPDATE package.json:
  - ADD: "recharts": "^2.5.0" (our standard chart library)
  - RUN: npm install
VALIDATE: npm list recharts → shows version 2.5.0

Task 4: Create Chart Component
STATUS [ ]
CREATE src/components/AnalyticsChart.tsx:
  - MIRROR pattern from: src/components/AdminChart.tsx
  - MODIFY: Use LineChart for trend visualization
  - KEEP: Responsive container pattern
  - IMPLEMENT: Props interface:
      * data: Array<{date: string, value: number}>
      * label: string
      * color: string
VALIDATE: npm test AnalyticsChart.test.tsx
IF_FAIL: Check recharts data format matches our transformed data
```

### Phase 3: Dashboard Layout

```yaml
Task 5: Create Dashboard Page
STATUS [ ]
CREATE src/pages/dashboard.tsx:
  - MIRROR layout from: src/pages/admin-dashboard.tsx
  - ADD sections:
      * Profile stats card (top)
      * Activity metrics cards (row of 3)
      * Charts section (2 column grid)
      * Export button (bottom right)
VALIDATE: npm run dev → visit http://localhost:3000/dashboard

Task 6: Fetch and Display Data
STATUS [ ]
MODIFY src/pages/dashboard.tsx:
  - ADD: useSWR hook for data fetching (see src/hooks/useUser.ts)
  - IMPLEMENT: Data transformation for charts
  - HANDLE: Loading and error states
VALIDATE: Check browser console for no errors, data loads
IF_FAIL: Check network tab, verify API returns correct format
```

### Phase 4: Export Functionality

```yaml
Task 7: Create Export API Endpoint
STATUS [ ]
CREATE src/api/export.ts:
  - IMPLEMENT: GET /api/users/{id}/export
  - RETURN: CSV file as download
  - LIMIT: Max 10,000 rows (pagination for larger)
VALIDATE: curl http://localhost:3000/api/users/1/export → downloads CSV file
IF_FAIL: Check CSV formatting, verify content-type header

Task 8: Add Export Button to Dashboard
STATUS [ ]
MODIFY src/pages/dashboard.tsx:
  - FIND: Section for action buttons
  - ADD: <ExportButton /> component
  - IMPLEMENT: onClick calls /api/export endpoint
  - SHOW: Loading spinner during export
VALIDATE: Click button → CSV downloads with correct data
```

### Phase 5: Testing & Polish

```yaml
Task 9: Write Unit Tests
STATUS [ ]
CREATE tests for all new components:
  - tests/components/AnalyticsChart.test.tsx
  - tests/pages/dashboard.test.tsx
  - tests/api/analytics.test.ts
VALIDATE: npm test → all tests pass
IF_FAIL: Run npm test -- --verbose for details

Task 10: Integration Testing
STATUS [ ]
TEST complete user flow:
  - Navigate to /dashboard
  - Verify data loads correctly
  - Interact with date range filter
  - Export data to CSV
  - Check CSV content matches displayed data
VALIDATE: Manual test checklist complete
```

## Completion Checklist

- [ ] All tasks marked [DONE]
- [ ] All tests passing
- [ ] Dashboard loads without errors
- [ ] Charts display correct data
- [ ] Export functionality works
- [ ] Responsive on mobile
- [ ] Accessible (keyboard navigation works)

## Notes

- Each task builds on previous ones - don't skip order
- Mark [DONE] after each task completes
- If a task fails validation, fix before continuing
- Export feature can be moved to Phase 6 if time-constrained

---

**Time Estimate**: 4-6 hours total
**Dependencies**: recharts library, existing user API