"""
BID-AI Database Models
SQLAlchemy ORM models for the BID-AI system
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, Integer, String, Text, TIMESTAMP, Boolean,
    DECIMAL, ARRAY, ForeignKey, Time, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR

Base = declarative_base()


class Municipality(Base):
    __tablename__ = 'municipalities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    region = Column(String(100))

    # Portal information
    portal_name = Column(String(255))
    portal_url = Column(Text)
    portal_type = Column(String(100))
    account_required = Column(Boolean, default=False)

    # Credentials (encrypted)
    username_encrypted = Column(Text)
    password_encrypted = Column(Text)

    # Calendar
    calendar_color = Column(String(7))
    google_calendar_id = Column(String(255))

    # Status
    monitoring_status = Column(String(50), default='active')
    priority = Column(Integer, default=5)

    # Assignment
    agent_team_assigned = Column(String(100))

    # Metadata
    notes = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    opportunities = relationship("Opportunity", back_populates="municipality")

    def __repr__(self):
        return f"<Municipality(name='{self.name}', region='{self.region}')>"


class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(255), nullable=False, unique=True)
    category = Column(String(100))
    weight = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"<Keyword(keyword='{self.keyword}', weight={self.weight})>"


class Opportunity(Base):
    __tablename__ = 'opportunities'

    id = Column(Integer, primary_key=True)

    # Source
    source_portal = Column(String(100), nullable=False)
    source_url = Column(Text, nullable=False)
    external_id = Column(String(255))

    # Details
    title = Column(Text, nullable=False)
    description = Column(Text)
    opportunity_type = Column(String(50))
    category = Column(String(100))

    # Issuer
    municipality_id = Column(Integer, ForeignKey('municipalities.id'))
    issuing_department = Column(String(255))
    contact_name = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))

    # Timeline
    posted_date = Column(TIMESTAMP)
    closing_date = Column(TIMESTAMP, nullable=False)
    closing_time = Column(Time)
    mandatory_site_visit = Column(Boolean, default=False)
    site_visit_date = Column(TIMESTAMP)

    # Financials
    estimated_value = Column(DECIMAL(12, 2))
    estimated_value_min = Column(DECIMAL(12, 2))
    estimated_value_max = Column(DECIMAL(12, 2))
    currency = Column(String(3), default='CAD')

    # BID-AI Intelligence
    tier = Column(String(10))
    tier_rationale = Column(Text)
    keywords_matched = Column(ARRAY(Text))
    relevance_score = Column(Integer)

    # Status
    status = Column(String(50), default='discovered')
    assigned_to = Column(String(100))

    # Metadata
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_scraped_at = Column(TIMESTAMP)

    # Full-text search
    search_vector = Column(TSVECTOR)

    # Relationships
    municipality = relationship("Municipality", back_populates="opportunities")
    bids = relationship("Bid", back_populates="opportunity", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="opportunity", cascade="all, delete-orphan")
    calendar_event = relationship("CalendarEvent", back_populates="opportunity", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_opportunities_closing_date', 'closing_date'),
        Index('idx_opportunities_status', 'status'),
        Index('idx_opportunities_tier', 'tier'),
        Index('idx_opportunities_municipality', 'municipality_id'),
    )

    def __repr__(self):
        return f"<Opportunity(id={self.id}, title='{self.title[:50]}...', tier='{self.tier}')>"

    def is_active(self) -> bool:
        """Check if opportunity is still open"""
        return self.closing_date > datetime.utcnow()

    def days_until_closing(self) -> int:
        """Calculate days remaining until closing"""
        delta = self.closing_date - datetime.utcnow()
        return delta.days


class Partner(Base):
    __tablename__ = 'partners'

    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)

    # Contact
    primary_contact = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    website = Column(String(255))

    # Capabilities
    specialties = Column(ARRAY(Text))
    capacity_rating = Column(Integer)
    geographic_coverage = Column(ARRAY(Text))

    # Relationship
    relationship_type = Column(String(100))
    preferred_partner = Column(Boolean, default=False)

    # Performance
    opportunities_referred = Column(Integer, default=0)
    opportunities_won = Column(Integer, default=0)
    total_referral_fees = Column(DECIMAL(12, 2), default=0)

    # Status
    status = Column(String(50), default='active')
    notes = Column(Text)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bids = relationship("Bid", back_populates="partner")

    def __repr__(self):
        return f"<Partner(name='{self.company_name}', status='{self.status}')>"


class Bid(Base):
    __tablename__ = 'bids'

    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id', ondelete='CASCADE'))

    # Strategy
    bid_tier = Column(String(10))
    strategy = Column(Text)

    # Pricing
    our_bid_amount = Column(DECIMAL(12, 2))
    cost_estimate = Column(DECIMAL(12, 2))
    margin_percentage = Column(DECIMAL(5, 2))

    # Partners
    partner_company_id = Column(Integer, ForeignKey('partners.id'))
    our_role = Column(String(100))
    partner_role = Column(String(100))

    # Submission
    submitted_date = Column(TIMESTAMP)
    submitted_by = Column(String(255))
    submission_confirmation = Column(Text)

    # Outcome
    outcome = Column(String(50))
    award_date = Column(TIMESTAMP)
    awarded_to = Column(String(255))
    award_amount = Column(DECIMAL(12, 2))

    # Deal Flow
    referral_fee = Column(DECIMAL(12, 2))
    referral_fee_type = Column(String(50))
    referral_status = Column(String(50))

    # Documents
    documents = Column(JSONB)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    opportunity = relationship("Opportunity", back_populates="bids")
    partner = relationship("Partner", back_populates="bids")

    def __repr__(self):
        return f"<Bid(id={self.id}, opportunity_id={self.opportunity_id}, outcome='{self.outcome}')>"


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id', ondelete='CASCADE'))

    filename = Column(String(255), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)

    # Storage
    storage_path = Column(Text)
    download_url = Column(Text)

    # Classification
    document_type = Column(String(100))

    downloaded = Column(Boolean, default=False)
    downloaded_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    opportunity = relationship("Opportunity", back_populates="documents")

    def __repr__(self):
        return f"<Document(filename='{self.filename}', type='{self.document_type}')>"


class ActivityLog(Base):
    __tablename__ = 'activity_log'

    id = Column(Integer, primary_key=True)

    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(Integer)

    actor = Column(String(255))
    details = Column(JSONB)

    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_activity_log_timestamp', 'timestamp'),
        Index('idx_activity_log_entity', 'entity_type', 'entity_id'),
    )

    def __repr__(self):
        return f"<ActivityLog(action='{self.action}', actor='{self.actor}')>"


class ScraperRun(Base):
    __tablename__ = 'scraper_runs'

    id = Column(Integer, primary_key=True)

    source_portal = Column(String(100), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP)

    # Results
    opportunities_found = Column(Integer, default=0)
    opportunities_new = Column(Integer, default=0)
    opportunities_updated = Column(Integer, default=0)

    # Status
    status = Column(String(50))
    error_message = Column(Text)

    # Performance
    duration_seconds = Column(Integer)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_scraper_runs_portal', 'source_portal', 'start_time'),
    )

    def __repr__(self):
        return f"<ScraperRun(portal='{self.source_portal}', status='{self.status}')>"


class CalendarEvent(Base):
    __tablename__ = 'calendar_events'

    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id', ondelete='CASCADE'), unique=True)

    google_event_id = Column(String(255), unique=True)
    calendar_id = Column(String(255))

    event_created = Column(Boolean, default=False)
    event_updated_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    opportunity = relationship("Opportunity", back_populates="calendar_event")

    def __repr__(self):
        return f"<CalendarEvent(opportunity_id={self.opportunity_id}, created={self.event_created})>"
