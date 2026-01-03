# Supabase Migration Plan - ON HOLD

**Status:** ⏸️ Paused pending architecture review  
**Date Created:** 2025-12-29  
**Reason for Pause:** Need to finalize database schema before migration

---

## Why We're Waiting

✅ **Smart decision to pause!**  
- Changing database structure AFTER migration = double work
- Better to finalize architecture first, then migrate once
- Brainstorm session may reveal important structural changes

---

## What We've Completed

### ✅ Local PostgreSQL 18 Setup
- Database: `bidai` created in Postgres.app
- Tables: 9 tables initialized
- Data: 31 municipalities loaded
- Backup: `bidai_backup.sql` created (926 lines)
- Status: Fully functional locally

### ✅ Supabase Account Setup
- Project: BID-AI
- Region: us-west-2 (AWS)
- Schema: Public schema selected for Data API
- Status: Ready to receive data

### ✅ Connection Strings Obtained

**Direct Connection (port 5432) - for migration:**
```
postgresql://postgres:[PASSWORD]@db.ryrgfoptugwbpodttzms.supabase.co:5432/postgres
```

**Transaction Pooler (port 6543) - for application:**
```
postgresql://postgres.ryrgfoptugwbpodttzms:[PASSWORD]@aws-0-us-west-2.pooler.supabase.com:6543/postgres
```

---

## Current Database Structure

### Tables (9)
1. **municipalities** - 31 Greater Vancouver municipalities
2. **opportunities** - Scraped bid opportunities
3. **bids** - Submitted bids tracking
4. **partners** - Partner network for deal flow tiers
5. **keywords** - Keyword matching for relevance scoring
6. **documents** - Bid documents and attachments
7. **calendar_events** - Deadline tracking
8. **scraper_runs** - Scraper execution logs
9. **activity_log** - System activity tracking

### Known Schema Considerations
- Agent hierarchy (THE BID MASTER + Municipal Teams) - not yet in DB
- Deal flow tiers (A-E) - classification logic exists, but may need schema updates
- Multi-tier partner relationships - current schema may need enhancement
- Scraper metadata - may need additional fields based on portal variations

---

## Migration Steps (Execute When Ready)

### Prerequisites Checklist
- [ ] Architecture brainstorm completed
- [ ] Database schema finalized and reviewed
- [ ] All structural changes implemented locally
- [ ] Local database tested with new schema
- [ ] Fresh backup created with final structure
- [ ] Supabase password accessible

### Step 1: Finalize Local Schema
```bash
# After schema changes, create fresh backup
cd /Users/evanholmes/* PROJECTS/BID-AI
/Applications/Postgres.app/Contents/Versions/18/bin/pg_dump \
  -U evanholmes -d bidai \
  --clean --if-exists \
  > bidai_final_backup.sql
```

### Step 2: Restore to Supabase (Direct Connection)
```bash
# Replace [PASSWORD] with your actual Supabase password
# Use DIRECT connection (port 5432) for migration

PGPASSWORD='[PASSWORD]' psql \
  -h db.ryrgfoptugwbpodttzms.supabase.co \
  -p 5432 \
  -U postgres \
  -d postgres \
  < bidai_final_backup.sql
```

### Step 3: Verify Migration
```bash
# Connect to Supabase and verify
PGPASSWORD='[PASSWORD]' psql \
  -h db.ryrgfoptugwbpodttzms.supabase.co \
  -p 5432 \
  -U postgres \
  -d postgres

# Then run these checks:
\dt                          # List tables (should show 9)
SELECT COUNT(*) FROM municipalities;  # Should be 31
\q
```

### Step 4: Update .env for Production
```bash
# Replace DATABASE_URL in .env with Transaction Pooler connection
DATABASE_URL=postgresql://postgres.ryrgfoptugwbpodttzms:[PASSWORD]@aws-0-us-west-2.pooler.supabase.com:6543/postgres
```

### Step 5: Update MCP Server
```bash
# Update postgres MCP server to use Supabase
claude mcp remove postgres
claude mcp add postgres --scope user -- \
  npx -y @modelcontextprotocol/server-postgres \
  postgresql://postgres.ryrgfoptugwbpodttzms:[PASSWORD]@aws-0-us-west-2.pooler.supabase.com:6543/postgres
```

### Step 6: Test Application
```bash
# Test Python connection
cd /Users/evanholmes/* PROJECTS/BID-AI
source venv/bin/activate
python -c "from src.config.settings import get_settings; print(get_settings().database.url)"

# Test database queries
python scripts/test_keyword_matcher.py

# Verify data integrity
python -c "
from src.database.connection import get_db_session
from src.database.models import Municipality
with get_db_session() as db:
    count = db.query(Municipality).count()
    print(f'Municipalities: {count}')
"
```

---

## Questions for Architecture Review

### Database Schema Questions
1. **Agent System Storage**
   - How to store THE BID MASTER + Municipal Team agents?
   - Track agent decisions/recommendations?
   - Store agent performance metrics?

2. **Deal Flow Tiers**
   - Current: `bid_classifier.py` has tier logic
   - Missing: Tier transition tracking, partner assignments?
   - Need: Historical tier changes, success rates per tier?

3. **Partner Network**
   - Current: Basic `partners` table
   - Missing: Capability matching, referral fee tracking?
   - Need: Partner performance analytics?

4. **Scraper Enhancements**
   - Portal-specific metadata fields?
   - Retry/failure tracking improvements?
   - Authentication session management?

5. **Opportunity Tracking**
   - Relevance score calculations - stored or computed?
   - Keyword match details - store which keywords matched?
   - Historical relevance trends?

6. **Multi-Municipality Coordination**
   - Cross-municipality opportunity deduplication?
   - Regional aggregation views?
   - Competition tracking between municipalities?

### Integration Questions
1. **Google Sheets (Awesome Table)**
   - Which tables/views to expose?
   - Real-time updates or periodic sync?
   - Read-only or read-write access?

2. **Calendar Integration**
   - Supabase has webhooks - use for deadline notifications?
   - Google Calendar API integration architecture?

3. **External APIs**
   - BC Bid, MERX portal authentication in cloud?
   - Store credentials in Supabase Vault?

---

## Resources

### Documentation
- **Local DB**: `src/database/models.py` - SQLAlchemy models
- **Schema SQL**: `src/database/schema.sql` - Triggers, indexes
- **Database docs**: `docs/DATABASE_SCHEMA.md`
- **Architecture**: `docs/ARCHITECTURE.md`

### Backups
- **Current backup**: `bidai_backup.sql` (926 lines)
- **Location**: `/Users/evanholmes/* PROJECTS/BID-AI/`
- **Date**: 2025-12-29

### Supabase Dashboard
- **URL**: https://supabase.com/dashboard/project/ryrgfoptugwbpodttzms
- **Region**: us-west-2 (AWS)
- **Database**: postgres

---

## After Migration Benefits

### For BID-AI Application
✅ Cloud-hosted database (accessible from anywhere)  
✅ Automatic backups (Supabase handles this)  
✅ Connection pooling (better performance)  
✅ Real-time subscriptions (PostgreSQL pub/sub)  
✅ PostgREST API (auto-generated REST API)  
✅ Row Level Security (fine-grained permissions)

### For Google Sheets Integration
✅ Direct PostgreSQL connection from Awesome Table  
✅ No local server required  
✅ Real-time data sync  
✅ Secure authenticated access

### For Development
✅ Team collaboration (shared database)  
✅ Production/staging separation  
✅ Better monitoring and logs  
✅ Scalability for multi-user access

---

## Timeline (Suggested)

1. **Now → Architecture Review** (1-2 sessions)
   - Brainstorm database schema changes
   - Review agent system storage needs
   - Finalize deal flow tier tracking
   - Document all structural requirements

2. **After Review → Schema Updates** (1-3 days)
   - Implement schema changes locally
   - Update SQLAlchemy models
   - Create migration scripts
   - Test with sample data

3. **After Testing → Migration** (1-2 hours)
   - Fresh backup with final schema
   - Restore to Supabase
   - Update application configuration
   - Verify all functionality

---

## Notes

- **Backup is safe**: Local `bidai` database remains unchanged
- **Supabase is ready**: Empty project waiting for data
- **No rush**: Better to get schema right first
- **Reversible**: Can always start over with new Supabase project

---

## Next Steps

1. ✅ **This document created** - Migration plan preserved
2. 🎯 **Schedule brainstorm session** - Review architecture
3. 📋 **Document schema changes** - Create schema update plan
4. 🔧 **Implement changes locally** - Test thoroughly
5. 🚀 **Execute migration** - When ready and tested

**When ready to migrate, refer back to this document for step-by-step instructions.**
