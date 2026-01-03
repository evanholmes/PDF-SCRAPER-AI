# Explain BID-AI Architecture

Provide a comprehensive explanation of the BID-AI system architecture, including:

## 1. High-Level Overview
- Project purpose and business model (direct bids + deal flow network)
- Multi-tier deal flow system (A/B/C/D/E tiers)
- Key stakeholders (ALL-PRO SIGNS, WESTCOAST CNC, partner network)

## 2. Agent Hierarchy
- THE BID MASTER (central orchestrator)
- Municipal Teams (Scout, Analyst, Writer, Compliance agents)
- How agents work together

## 3. Technical Stack
- Backend: Python, PostgreSQL, SQLAlchemy
- Frontend: Next.js, React, TypeScript, Tailwind
- AI: Anthropic Claude, keyword matching, classification

## 4. Data Flow
- How opportunities are discovered
- Keyword matching and scoring process
- Tier classification logic
- Database storage and retrieval

## 5. Key Components
- Database schema (9 core tables)
- Filtering engine (keyword_matcher, capability_matcher, bid_classifier)
- Dashboard (CEO view, BC Bid checklist)
- Municipality monitoring (31+ portals)

Reference docs/ARCHITECTURE.md and CLAUDE.md for detailed information.
