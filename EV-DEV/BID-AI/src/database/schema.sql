-- BID-AI Database Schema
-- PostgreSQL 12+
-- Created: Dec 23, 2025

-- Enable UUID extension for unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable full-text search extension
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ======================
-- CORE TABLES
-- ======================

-- Table 1: Municipalities
CREATE TABLE municipalities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    region VARCHAR(100),

    portal_name VARCHAR(255),
    portal_url TEXT,
    portal_type VARCHAR(100),
    account_required BOOLEAN DEFAULT FALSE,

    username_encrypted TEXT,
    password_encrypted TEXT,

    calendar_color VARCHAR(7),
    google_calendar_id VARCHAR(255),

    monitoring_status VARCHAR(50) DEFAULT 'active',
    priority INTEGER DEFAULT 5,

    agent_team_assigned VARCHAR(100),

    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Keywords
CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(100),
    weight INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Opportunities (Main table)
CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,

    -- Source
    source_portal VARCHAR(100) NOT NULL,
    source_url TEXT NOT NULL,
    external_id VARCHAR(255),

    -- Details
    title TEXT NOT NULL,
    description TEXT,
    opportunity_type VARCHAR(50),
    category VARCHAR(100),

    -- Issuer
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

    -- BID-AI Intelligence
    tier VARCHAR(10),
    tier_rationale TEXT,
    keywords_matched TEXT[],
    relevance_score INTEGER,

    -- Status
    status VARCHAR(50) DEFAULT 'discovered',
    assigned_to VARCHAR(100),

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_scraped_at TIMESTAMP,

    -- Full text search
    search_vector TSVECTOR,

    CONSTRAINT unique_opportunity UNIQUE(source_portal, external_id)
);

-- Table 4: Partners
CREATE TABLE partners (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,

    primary_contact VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    website VARCHAR(255),

    specialties TEXT[],
    capacity_rating INTEGER,
    geographic_coverage TEXT[],

    relationship_type VARCHAR(100),
    preferred_partner BOOLEAN DEFAULT FALSE,

    opportunities_referred INTEGER DEFAULT 0,
    opportunities_won INTEGER DEFAULT 0,
    total_referral_fees DECIMAL(12, 2) DEFAULT 0,

    status VARCHAR(50) DEFAULT 'active',
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 5: Bids
CREATE TABLE bids (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id) ON DELETE CASCADE,

    bid_tier VARCHAR(10),
    strategy TEXT,

    our_bid_amount DECIMAL(12, 2),
    cost_estimate DECIMAL(12, 2),
    margin_percentage DECIMAL(5, 2),

    partner_company_id INTEGER REFERENCES partners(id),
    our_role VARCHAR(100),
    partner_role VARCHAR(100),

    submitted_date TIMESTAMP,
    submitted_by VARCHAR(255),
    submission_confirmation TEXT,

    outcome VARCHAR(50),
    award_date TIMESTAMP,
    awarded_to VARCHAR(255),
    award_amount DECIMAL(12, 2),

    referral_fee DECIMAL(12, 2),
    referral_fee_type VARCHAR(50),
    referral_status VARCHAR(50),

    documents JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 6: Documents
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id) ON DELETE CASCADE,

    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,

    storage_path TEXT,
    download_url TEXT,

    document_type VARCHAR(100),

    downloaded BOOLEAN DEFAULT FALSE,
    downloaded_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 7: Activity Log
CREATE TABLE activity_log (
    id SERIAL PRIMARY KEY,

    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,

    actor VARCHAR(255),
    details JSONB,

    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 8: Scraper Runs
CREATE TABLE scraper_runs (
    id SERIAL PRIMARY KEY,

    source_portal VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,

    opportunities_found INTEGER DEFAULT 0,
    opportunities_new INTEGER DEFAULT 0,
    opportunities_updated INTEGER DEFAULT 0,

    status VARCHAR(50),
    error_message TEXT,

    duration_seconds INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 9: Calendar Events
CREATE TABLE calendar_events (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id) ON DELETE CASCADE,

    google_event_id VARCHAR(255) UNIQUE,
    calendar_id VARCHAR(255),

    event_created BOOLEAN DEFAULT FALSE,
    event_updated_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- INDEXES
-- ======================

-- Opportunities
CREATE INDEX idx_opportunities_closing_date ON opportunities(closing_date);
CREATE INDEX idx_opportunities_status ON opportunities(status);
CREATE INDEX idx_opportunities_tier ON opportunities(tier);
CREATE INDEX idx_opportunities_municipality ON opportunities(municipality_id);
CREATE INDEX idx_opportunities_search ON opportunities USING GIN(search_vector);
CREATE INDEX idx_opportunities_keywords ON opportunities USING GIN(keywords_matched);

-- Activity Log
CREATE INDEX idx_activity_log_timestamp ON activity_log(timestamp DESC);
CREATE INDEX idx_activity_log_entity ON activity_log(entity_type, entity_id);

-- Scraper Runs
CREATE INDEX idx_scraper_runs_portal ON scraper_runs(source_portal, start_time DESC);

-- ======================
-- TRIGGERS
-- ======================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_municipalities_updated_at BEFORE UPDATE ON municipalities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_partners_updated_at BEFORE UPDATE ON partners
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bids_updated_at BEFORE UPDATE ON bids
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Auto-populate search_vector for opportunities
CREATE OR REPLACE FUNCTION opportunities_search_vector_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvector_update BEFORE INSERT OR UPDATE ON opportunities
    FOR EACH ROW EXECUTE FUNCTION opportunities_search_vector_update();

-- ======================
-- SEED DATA
-- ======================

-- Insert Keywords
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
('wood', 'materials', 5)
ON CONFLICT (keyword) DO NOTHING;

-- ======================
-- VIEWS
-- ======================

-- Active opportunities view
CREATE VIEW active_opportunities AS
SELECT
    o.*,
    m.name as municipality_name,
    m.region,
    m.calendar_color
FROM opportunities o
LEFT JOIN municipalities m ON o.municipality_id = m.id
WHERE o.status IN ('discovered', 'reviewed', 'bidding')
  AND o.closing_date > CURRENT_TIMESTAMP
ORDER BY o.closing_date ASC;

-- Tier A opportunities (we can fulfill)
CREATE VIEW tier_a_opportunities AS
SELECT * FROM active_opportunities
WHERE tier = 'A'
ORDER BY closing_date ASC;

-- High value opportunities
CREATE VIEW high_value_opportunities AS
SELECT * FROM active_opportunities
WHERE estimated_value > 50000 OR estimated_value_min > 50000
ORDER BY estimated_value DESC NULLS LAST;

-- ======================
-- FUNCTIONS
-- ======================

-- Calculate relevance score based on keywords
CREATE OR REPLACE FUNCTION calculate_relevance_score(title TEXT, description TEXT)
RETURNS INTEGER AS $$
DECLARE
    score INTEGER := 0;
    keyword_record RECORD;
BEGIN
    FOR keyword_record IN
        SELECT keyword, weight FROM keywords WHERE is_active = TRUE
    LOOP
        IF title ILIKE '%' || keyword_record.keyword || '%' THEN
            score := score + (keyword_record.weight * 2);
        END IF;
        IF description ILIKE '%' || keyword_record.keyword || '%' THEN
            score := score + keyword_record.weight;
        END IF;
    END LOOP;

    RETURN LEAST(score, 100); -- Cap at 100
END;
$$ LANGUAGE plpgsql;

-- Grant permissions (adjust user as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bidai_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bidai_user;
