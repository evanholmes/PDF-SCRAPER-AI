# BID-AI Database Schema Design

## Philosophy
The database must support:
1. **Multi-source aggregation** - Bids from BC Bid, MERX, and 31+ municipal portals
2. **Intelligent categorization** - Tier A (fulfill), Tier B (assign), Tier C (partner), Tier D (broker), Tier E (archive)
3. **Relationship tracking** - Partner network, subcontractors, assignment deals
4. **Calendar integration** - Deadline tracking, color-coded by municipality
5. **Audit trail** - Who saw what, when, and what action was taken

---

## Core Tables

### 1. `opportunities`
The master table for all bid opportunities.

```sql
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    
    -- Source Information
    source_portal VARCHAR(100) NOT NULL,  -- 'BC Bid', 'MERX', 'City of Vancouver', etc.
    source_url TEXT NOT NULL,
    external_id VARCHAR(255),  -- Portal's internal ID/reference number
    
    -- Opportunity Details
    title TEXT NOT NULL,
    description TEXT,
    opportunity_type VARCHAR(50),  -- 'RFP', 'RFQ', 'Tender', 'ITB', etc.
    category VARCHAR(100),  -- 'Signage', 'Printing', 'Construction', etc.
    
    -- Issuing Organization
    municipality_id INTEGER REFERENCES municipalities(id),
    issuing_department VARCHAR(255),
    contact_name VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    
    -- Timeline
    posted_date TIMESTAMP,
    closing_date TIMESTAMP NOT NULL,
    closing_time TIME,
    mandatory_site_visit BOOLEAN DEFAULT FALSE,
    site_visit_date TIMESTAMP,
    
    -- Financials
    estimated_value DECIMAL(12, 2),
    estimated_value_min DECIMAL(12, 2),
    estimated_value_max DECIMAL(12, 2),
    currency VARCHAR(3) DEFAULT 'CAD',
    
    -- BID-AI Classification
    tier VARCHAR(10),  -- 'A', 'B', 'C', 'D', 'E'
    tier_rationale TEXT,
    keywords_matched TEXT[],  -- Array of matched keywords
    relevance_score INTEGER,  -- 0-100 based on keyword matching
    
    -- Status Tracking
    status VARCHAR(50) DEFAULT 'discovered',  
    -- 'discovered', 'reviewed', 'bidding', 'submitted', 'awarded', 'lost', 'archived'
    assigned_to VARCHAR(100),  -- THE BID MASTER or specific agent team
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_scraped_at TIMESTAMP,
    
    -- Full text search
    search_vector TSVECTOR,
    
    CONSTRAINT unique_opportunity UNIQUE(source_portal, external_id)
);

-- Indexes for performance
CREATE INDEX idx_opportunities_closing_date ON opportunities(closing_date);
CREATE INDEX idx_opportunities_status ON opportunities(status);
CREATE INDEX idx_opportunities_tier ON opportunities(tier);
CREATE INDEX idx_opportunities_municipality ON opportunities(municipality_id);
CREATE INDEX idx_opportunities_search ON opportunities USING GIN(search_vector);
```

---

### 2. `municipalities`
Reference table for all municipalities and organizations we monitor.

```sql
CREATE TABLE municipalities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    region VARCHAR(100),  -- 'Metro Vancouver', 'Fraser Valley', etc.
    
    -- Portal Information
    portal_name VARCHAR(255),
    portal_url TEXT,
    portal_type VARCHAR(100),  -- 'BidsAndTenders', 'Direct Website', 'Custom', etc.
    account_required BOOLEAN DEFAULT FALSE,
    
    -- Access Credentials (encrypted)
    username_encrypted TEXT,
    password_encrypted TEXT,
    
    -- Calendar Integration
    calendar_color VARCHAR(7),  -- Hex color code
    google_calendar_id VARCHAR(255),
    
    -- Status
    monitoring_status VARCHAR(50) DEFAULT 'active',  -- 'active', 'pending', 'inactive'
    priority INTEGER DEFAULT 5,  -- 1-10, higher = more important
    
    -- Agent Assignment
    agent_team_assigned VARCHAR(100),
    
    -- Metadata
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 3. `keywords`
Signage and printing keywords for filtering.

```sql
CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100),  -- 'signage', 'printing', 'wayfinding', 'graphics', etc.
    weight INTEGER DEFAULT 1,  -- Importance multiplier for relevance scoring
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pre-populate with signage/printing keywords
INSERT INTO keywords (keyword, category, weight) VALUES
('signage', 'signage', 10),
('wayfinding', 'signage', 10),
('sign', 'signage', 8),
('dimensional letters', 'signage', 10),
('monument sign', 'signage', 10),
('pylon sign', 'signage', 10),
('channel letters', 'signage', 10),
('illuminated sign', 'signage', 9),
('digital signage', 'signage', 9),
('directional signs', 'signage', 8),
('building signage', 'signage', 8),
('exterior signage', 'signage', 8),
('interior signage', 'signage', 8),
('ADA signage', 'signage', 7),
('braille signage', 'signage', 7),
('safety signs', 'signage', 6),
('parking signs', 'signage', 6),
('traffic signs', 'signage', 5),
('printing', 'printing', 10),
('print', 'printing', 8),
('digital printing', 'printing', 9),
('large format printing', 'printing', 10),
('offset printing', 'printing', 8),
('banners', 'printing', 8),
('posters', 'printing', 7),
('vinyl graphics', 'printing', 9),
('decals', 'printing', 7),
('vehicle wrap', 'printing', 8),
('window graphics', 'printing', 8),
('floor graphics', 'printing', 7),
('wall murals', 'printing', 8),
('CNC', 'fabrication', 9),
('millwork', 'fabrication', 9),
('router', 'fabrication', 7),
('acrylic', 'materials', 7),
('aluminum', 'materials', 6),
('bronze', 'materials', 6),
('wood', 'materials', 5);
```

---

### 4. `bids`
Tracks our bidding activity on opportunities.

```sql
CREATE TABLE bids (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id) ON DELETE CASCADE,
    
    -- Bid Strategy
    bid_tier VARCHAR(10),  -- 'A', 'B', 'C', 'D' (matches opportunity tier)
    strategy TEXT,  -- Direct, Assignment, Partner, Broker
    
    -- Pricing
    our_bid_amount DECIMAL(12, 2),
    cost_estimate DECIMAL(12, 2),
    margin_percentage DECIMAL(5, 2),
    
    -- Partners (if applicable)
    partner_company_id INTEGER REFERENCES partners(id),
    our_role VARCHAR(100),  -- 'Prime', 'Subcontractor', 'Consultant', 'Referrer'
    partner_role VARCHAR(100),
    
    -- Submission
    submitted_date TIMESTAMP,
    submitted_by VARCHAR(255),
    submission_confirmation TEXT,
    
    -- Outcome
    outcome VARCHAR(50),  -- 'won', 'lost', 'withdrawn', 'pending'
    award_date TIMESTAMP,
    awarded_to VARCHAR(255),
    award_amount DECIMAL(12, 2),
    
    -- Deal Flow (for Tier B/C/D)
    referral_fee DECIMAL(12, 2),
    referral_fee_type VARCHAR(50),  -- 'flat', 'percentage'
    referral_status VARCHAR(50),  -- 'proposed', 'accepted', 'invoiced', 'paid'
    
    -- Documents
    documents JSONB,  -- Array of document references
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 5. `partners`
Network of companies we can assign work to or partner with.

```sql
CREATE TABLE partners (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    
    -- Contact Information
    primary_contact VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    website VARCHAR(255),
    
    -- Capabilities
    specialties TEXT[],  -- Array: ['large format digital', 'architectural signage', etc.]
    capacity_rating INTEGER,  -- 1-10 subjective assessment
    geographic_coverage TEXT[],  -- ['Metro Vancouver', 'Fraser Valley']
    
    -- Relationship
    relationship_type VARCHAR(100),  -- 'Referral Partner', 'Joint Venture', 'Subcontractor'
    preferred_partner BOOLEAN DEFAULT FALSE,
    
    -- Performance Tracking
    opportunities_referred INTEGER DEFAULT 0,
    opportunities_won INTEGER DEFAULT 0,
    total_referral_fees DECIMAL(12, 2) DEFAULT 0,
    
    -- Status
    status VARCHAR(50) DEFAULT 'active',
    
    -- Notes
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 6. `activity_log`
Audit trail of all system and user actions.

```sql
CREATE TABLE activity_log (
    id SERIAL PRIMARY KEY,
    
    -- What happened
    action VARCHAR(100) NOT NULL,  -- 'opportunity_discovered', 'tier_assigned', 'bid_submitted', etc.
    entity_type VARCHAR(50),  -- 'opportunity', 'bid', 'partner'
    entity_id INTEGER,
    
    -- Who did it
    actor VARCHAR(255),  -- 'THE BID MASTER', 'Team Vancouver', 'CEO', 'scraper_bot'
    
    -- Details
    details JSONB,  -- Flexible JSON for any additional context
    
    -- When
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activity_log_timestamp ON activity_log(timestamp DESC);
CREATE INDEX idx_activity_log_entity ON activity_log(entity_type, entity_id);
```

---

### 7. `scraper_runs`
Track scraper execution and health.

```sql
CREATE TABLE scraper_runs (
    id SERIAL PRIMARY KEY,
    
    source_portal VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    
    -- Results
    opportunities_found INTEGER DEFAULT 0,
    opportunities_new INTEGER DEFAULT 0,
    opportunities_updated INTEGER DEFAULT 0,
    
    -- Status
    status VARCHAR(50),  -- 'running', 'completed', 'failed'
    error_message TEXT,
    
    -- Performance
    duration_seconds INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scraper_runs_portal ON scraper_runs(source_portal, start_time DESC);
```

---

## Supporting Tables

### 8. `documents`
Store references to bid documents.

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id) ON DELETE CASCADE,
    
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),  -- 'pdf', 'doc', 'xls', etc.
    file_size INTEGER,  -- bytes
    
    -- Storage
    storage_path TEXT,  -- Local or cloud storage path
    download_url TEXT,
    
    -- Classification
    document_type VARCHAR(100),  -- 'RFP', 'Addendum', 'Plans', 'Specifications'
    
    downloaded BOOLEAN DEFAULT FALSE,
    downloaded_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 9. `calendar_events`
Google Calendar integration tracking.

```sql
CREATE TABLE calendar_events (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id) ON DELETE CASCADE,
    
    google_event_id VARCHAR(255) UNIQUE,
    calendar_id VARCHAR(255),  -- Which Google Calendar
    
    event_created BOOLEAN DEFAULT FALSE,
    event_updated_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Relationships Diagram

```
municipalities (1) ----< (M) opportunities
opportunities (1) ----< (M) bids
opportunities (1) ----< (M) documents
opportunities (1) ----< (1) calendar_events
partners (1) ----< (M) bids
keywords (M) ----< (M) opportunities (via array matching)
```

---

## Future Enhancements

1. **Machine Learning Table**: Store training data for automatic tier classification
2. **Email Integration**: Track email communications about opportunities
3. **Pricing History**: Historical pricing data for better bidding
4. **Competitor Intelligence**: Track who wins what, identify patterns

---

*Schema Version: 1.0*
*Last Updated: Dec 23, 2025*
