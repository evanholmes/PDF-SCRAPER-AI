--
-- PostgreSQL database dump
--

\restrict mF61fKV12ROXLo9AkMRrWgzaFkrR1UiCLh9vNIullHZI3E6clykGs33oN1vMvJl

-- Dumped from database version 18.1 (Postgres.app)
-- Dumped by pg_dump version 18.1 (Postgres.app)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.opportunities DROP CONSTRAINT IF EXISTS opportunities_municipality_id_fkey;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_opportunity_id_fkey;
ALTER TABLE IF EXISTS ONLY public.calendar_events DROP CONSTRAINT IF EXISTS calendar_events_opportunity_id_fkey;
ALTER TABLE IF EXISTS ONLY public.bids DROP CONSTRAINT IF EXISTS bids_partner_company_id_fkey;
ALTER TABLE IF EXISTS ONLY public.bids DROP CONSTRAINT IF EXISTS bids_opportunity_id_fkey;
DROP INDEX IF EXISTS public.idx_scraper_runs_portal;
DROP INDEX IF EXISTS public.idx_opportunities_tier;
DROP INDEX IF EXISTS public.idx_opportunities_status;
DROP INDEX IF EXISTS public.idx_opportunities_municipality;
DROP INDEX IF EXISTS public.idx_opportunities_closing_date;
DROP INDEX IF EXISTS public.idx_activity_log_timestamp;
DROP INDEX IF EXISTS public.idx_activity_log_entity;
ALTER TABLE IF EXISTS ONLY public.scraper_runs DROP CONSTRAINT IF EXISTS scraper_runs_pkey;
ALTER TABLE IF EXISTS ONLY public.partners DROP CONSTRAINT IF EXISTS partners_pkey;
ALTER TABLE IF EXISTS ONLY public.opportunities DROP CONSTRAINT IF EXISTS opportunities_pkey;
ALTER TABLE IF EXISTS ONLY public.municipalities DROP CONSTRAINT IF EXISTS municipalities_pkey;
ALTER TABLE IF EXISTS ONLY public.municipalities DROP CONSTRAINT IF EXISTS municipalities_name_key;
ALTER TABLE IF EXISTS ONLY public.keywords DROP CONSTRAINT IF EXISTS keywords_pkey;
ALTER TABLE IF EXISTS ONLY public.keywords DROP CONSTRAINT IF EXISTS keywords_keyword_key;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_pkey;
ALTER TABLE IF EXISTS ONLY public.calendar_events DROP CONSTRAINT IF EXISTS calendar_events_pkey;
ALTER TABLE IF EXISTS ONLY public.calendar_events DROP CONSTRAINT IF EXISTS calendar_events_opportunity_id_key;
ALTER TABLE IF EXISTS ONLY public.calendar_events DROP CONSTRAINT IF EXISTS calendar_events_google_event_id_key;
ALTER TABLE IF EXISTS ONLY public.bids DROP CONSTRAINT IF EXISTS bids_pkey;
ALTER TABLE IF EXISTS ONLY public.activity_log DROP CONSTRAINT IF EXISTS activity_log_pkey;
ALTER TABLE IF EXISTS public.scraper_runs ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.partners ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.opportunities ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.municipalities ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.keywords ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.documents ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.calendar_events ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.bids ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.activity_log ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.scraper_runs_id_seq;
DROP TABLE IF EXISTS public.scraper_runs;
DROP SEQUENCE IF EXISTS public.partners_id_seq;
DROP TABLE IF EXISTS public.partners;
DROP SEQUENCE IF EXISTS public.opportunities_id_seq;
DROP TABLE IF EXISTS public.opportunities;
DROP SEQUENCE IF EXISTS public.municipalities_id_seq;
DROP TABLE IF EXISTS public.municipalities;
DROP SEQUENCE IF EXISTS public.keywords_id_seq;
DROP TABLE IF EXISTS public.keywords;
DROP SEQUENCE IF EXISTS public.documents_id_seq;
DROP TABLE IF EXISTS public.documents;
DROP SEQUENCE IF EXISTS public.calendar_events_id_seq;
DROP TABLE IF EXISTS public.calendar_events;
DROP SEQUENCE IF EXISTS public.bids_id_seq;
DROP TABLE IF EXISTS public.bids;
DROP SEQUENCE IF EXISTS public.activity_log_id_seq;
DROP TABLE IF EXISTS public.activity_log;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_log; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.activity_log (
    id integer NOT NULL,
    action character varying(100) NOT NULL,
    entity_type character varying(50),
    entity_id integer,
    actor character varying(255),
    details jsonb,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.activity_log OWNER TO evanholmes;

--
-- Name: activity_log_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.activity_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_log_id_seq OWNER TO evanholmes;

--
-- Name: activity_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.activity_log_id_seq OWNED BY public.activity_log.id;


--
-- Name: bids; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.bids (
    id integer NOT NULL,
    opportunity_id integer,
    bid_tier character varying(10),
    strategy text,
    our_bid_amount numeric(12,2),
    cost_estimate numeric(12,2),
    margin_percentage numeric(5,2),
    partner_company_id integer,
    our_role character varying(100),
    partner_role character varying(100),
    submitted_date timestamp without time zone,
    submitted_by character varying(255),
    submission_confirmation text,
    outcome character varying(50),
    award_date timestamp without time zone,
    awarded_to character varying(255),
    award_amount numeric(12,2),
    referral_fee numeric(12,2),
    referral_fee_type character varying(50),
    referral_status character varying(50),
    documents jsonb,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.bids OWNER TO evanholmes;

--
-- Name: bids_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.bids_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bids_id_seq OWNER TO evanholmes;

--
-- Name: bids_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.bids_id_seq OWNED BY public.bids.id;


--
-- Name: calendar_events; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.calendar_events (
    id integer NOT NULL,
    opportunity_id integer,
    google_event_id character varying(255),
    calendar_id character varying(255),
    event_created boolean,
    event_updated_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public.calendar_events OWNER TO evanholmes;

--
-- Name: calendar_events_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.calendar_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.calendar_events_id_seq OWNER TO evanholmes;

--
-- Name: calendar_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.calendar_events_id_seq OWNED BY public.calendar_events.id;


--
-- Name: documents; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    opportunity_id integer,
    filename character varying(255) NOT NULL,
    file_type character varying(50),
    file_size integer,
    storage_path text,
    download_url text,
    document_type character varying(100),
    downloaded boolean,
    downloaded_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public.documents OWNER TO evanholmes;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_id_seq OWNER TO evanholmes;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: keywords; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.keywords (
    id integer NOT NULL,
    keyword character varying(255) NOT NULL,
    category character varying(100),
    weight integer,
    is_active boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.keywords OWNER TO evanholmes;

--
-- Name: keywords_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.keywords_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.keywords_id_seq OWNER TO evanholmes;

--
-- Name: keywords_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.keywords_id_seq OWNED BY public.keywords.id;


--
-- Name: municipalities; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.municipalities (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    region character varying(100),
    portal_name character varying(255),
    portal_url text,
    portal_type character varying(100),
    account_required boolean,
    username_encrypted text,
    password_encrypted text,
    calendar_color character varying(7),
    google_calendar_id character varying(255),
    monitoring_status character varying(50),
    priority integer,
    agent_team_assigned character varying(100),
    notes text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.municipalities OWNER TO evanholmes;

--
-- Name: municipalities_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.municipalities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.municipalities_id_seq OWNER TO evanholmes;

--
-- Name: municipalities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.municipalities_id_seq OWNED BY public.municipalities.id;


--
-- Name: opportunities; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.opportunities (
    id integer NOT NULL,
    source_portal character varying(100) NOT NULL,
    source_url text NOT NULL,
    external_id character varying(255),
    title text NOT NULL,
    description text,
    opportunity_type character varying(50),
    category character varying(100),
    municipality_id integer,
    issuing_department character varying(255),
    contact_name character varying(255),
    contact_email character varying(255),
    contact_phone character varying(50),
    posted_date timestamp without time zone,
    closing_date timestamp without time zone NOT NULL,
    closing_time time without time zone,
    mandatory_site_visit boolean,
    site_visit_date timestamp without time zone,
    estimated_value numeric(12,2),
    estimated_value_min numeric(12,2),
    estimated_value_max numeric(12,2),
    currency character varying(3),
    tier character varying(10),
    tier_rationale text,
    keywords_matched text[],
    relevance_score integer,
    status character varying(50),
    assigned_to character varying(100),
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_scraped_at timestamp without time zone,
    search_vector tsvector
);


ALTER TABLE public.opportunities OWNER TO evanholmes;

--
-- Name: opportunities_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.opportunities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.opportunities_id_seq OWNER TO evanholmes;

--
-- Name: opportunities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.opportunities_id_seq OWNED BY public.opportunities.id;


--
-- Name: partners; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.partners (
    id integer NOT NULL,
    company_name character varying(255) NOT NULL,
    primary_contact character varying(255),
    email character varying(255),
    phone character varying(50),
    address text,
    website character varying(255),
    specialties text[],
    capacity_rating integer,
    geographic_coverage text[],
    relationship_type character varying(100),
    preferred_partner boolean,
    opportunities_referred integer,
    opportunities_won integer,
    total_referral_fees numeric(12,2),
    status character varying(50),
    notes text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.partners OWNER TO evanholmes;

--
-- Name: partners_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.partners_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.partners_id_seq OWNER TO evanholmes;

--
-- Name: partners_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.partners_id_seq OWNED BY public.partners.id;


--
-- Name: scraper_runs; Type: TABLE; Schema: public; Owner: evanholmes
--

CREATE TABLE public.scraper_runs (
    id integer NOT NULL,
    source_portal character varying(100) NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone,
    opportunities_found integer,
    opportunities_new integer,
    opportunities_updated integer,
    status character varying(50),
    error_message text,
    duration_seconds integer,
    created_at timestamp without time zone
);


ALTER TABLE public.scraper_runs OWNER TO evanholmes;

--
-- Name: scraper_runs_id_seq; Type: SEQUENCE; Schema: public; Owner: evanholmes
--

CREATE SEQUENCE public.scraper_runs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scraper_runs_id_seq OWNER TO evanholmes;

--
-- Name: scraper_runs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: evanholmes
--

ALTER SEQUENCE public.scraper_runs_id_seq OWNED BY public.scraper_runs.id;


--
-- Name: activity_log id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.activity_log ALTER COLUMN id SET DEFAULT nextval('public.activity_log_id_seq'::regclass);


--
-- Name: bids id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.bids ALTER COLUMN id SET DEFAULT nextval('public.bids_id_seq'::regclass);


--
-- Name: calendar_events id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.calendar_events ALTER COLUMN id SET DEFAULT nextval('public.calendar_events_id_seq'::regclass);


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: keywords id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.keywords ALTER COLUMN id SET DEFAULT nextval('public.keywords_id_seq'::regclass);


--
-- Name: municipalities id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.municipalities ALTER COLUMN id SET DEFAULT nextval('public.municipalities_id_seq'::regclass);


--
-- Name: opportunities id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.opportunities ALTER COLUMN id SET DEFAULT nextval('public.opportunities_id_seq'::regclass);


--
-- Name: partners id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.partners ALTER COLUMN id SET DEFAULT nextval('public.partners_id_seq'::regclass);


--
-- Name: scraper_runs id; Type: DEFAULT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.scraper_runs ALTER COLUMN id SET DEFAULT nextval('public.scraper_runs_id_seq'::regclass);


--
-- Data for Name: activity_log; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.activity_log (id, action, entity_type, entity_id, actor, details, "timestamp") FROM stdin;
\.


--
-- Data for Name: bids; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.bids (id, opportunity_id, bid_tier, strategy, our_bid_amount, cost_estimate, margin_percentage, partner_company_id, our_role, partner_role, submitted_date, submitted_by, submission_confirmation, outcome, award_date, awarded_to, award_amount, referral_fee, referral_fee_type, referral_status, documents, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: calendar_events; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.calendar_events (id, opportunity_id, google_event_id, calendar_id, event_created, event_updated_at, created_at) FROM stdin;
\.


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.documents (id, opportunity_id, filename, file_type, file_size, storage_path, download_url, document_type, downloaded, downloaded_at, created_at) FROM stdin;
\.


--
-- Data for Name: keywords; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.keywords (id, keyword, category, weight, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: municipalities; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.municipalities (id, name, region, portal_name, portal_url, portal_type, account_required, username_encrypted, password_encrypted, calendar_color, google_calendar_id, monitoring_status, priority, agent_team_assigned, notes, created_at, updated_at) FROM stdin;
1	Metro Vancouver	Regional District	Bids and Tenders	https://metrovancouver.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#4285F4	\N	Active	5	Team Metro	Regional district - covers multiple municipalities	2025-12-29 08:15:01.554409	2025-12-29 08:15:01.554411
2	Fraser Valley Regional District	Regional District	Tenders & RFPs	https://www.fvrd.ca/EN/main/government/tenders-rfps.html	Direct Website	f	\N	\N	#0F9D58	\N	Active	5	Team FVRD	Regional district for Fraser Valley	2025-12-29 08:15:01.554412	2025-12-29 08:15:01.554413
3	Port of Vancouver	Port Authority	RFPs and Procurement	https://www.portvancouver.com/business-and-projects/rfps-and-procurement	Direct Website	f	\N	\N	#DB4437	\N	Active	5	Team Port	Major port authority - large contracts	2025-12-29 08:15:01.554413	2025-12-29 08:15:01.554414
4	City of Vancouver	Metro Vancouver	VendorLink	https://vancouver.vendorlink.ca/	VendorLink Platform	t	\N	\N	#F4B400	\N	Active	5	Team Vancouver	Largest city - high volume of opportunities	2025-12-29 08:15:01.554414	2025-12-29 08:15:01.554415
5	City of Surrey	Metro Vancouver	Tenders RFQs RFPs	https://www.surrey.ca/business-economy/tenders-rfqs-rfps	Direct Website	f	\N	\N	#AB47BC	\N	Active	5	Team Surrey	Second largest city in BC	2025-12-29 08:15:01.554415	2025-12-29 08:15:01.554416
6	City of Burnaby	Metro Vancouver	Bids and Tenders	https://burnaby.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#00ACC1	\N	Pending Setup	5	Team Burnaby	Major municipality	2025-12-29 08:15:01.554416	2025-12-29 08:15:01.554417
7	City of Richmond	Metro Vancouver	Purchasing & Tenders	https://www.richmond.ca/busdev/tenders/tenders.htm	Direct Website	f	\N	\N	#FF7043	\N	Pending Setup	5	Team Richmond	Airport city - significant opportunities	2025-12-29 08:15:01.554417	2025-12-29 08:15:01.554418
8	City of Coquitlam	Metro Vancouver	Bids and Tenders	https://coquitlam.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#9CCC65	\N	Pending Setup	5	Team Coquitlam	Tri-Cities area	2025-12-29 08:15:01.554418	2025-12-29 08:15:01.554419
9	City of New Westminster	Metro Vancouver	Bids and Tenders	https://newwestcity.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#26A69A	\N	Pending Setup	5	Team New West	Historic city	2025-12-29 08:15:01.554419	2025-12-29 08:15:01.55442
10	City of Delta	Metro Vancouver	Purchasing	https://www.delta.ca/your-government/doing-business-with-delta	Direct Website	f	\N	\N	#5C6BC0	\N	Pending Setup	5	Team Delta	Agricultural and industrial mix	2025-12-29 08:15:01.55442	2025-12-29 08:15:01.554421
11	City of North Vancouver	Metro Vancouver	Bids and Tenders	https://cnv.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#EF5350	\N	Pending Setup	5	Team CNV	North Shore	2025-12-29 08:15:01.554421	2025-12-29 08:15:01.554421
12	District of North Vancouver	Metro Vancouver	Purchasing	https://www.dnv.org/business-development/purchasing	Direct Website	f	\N	\N	#EC407A	\N	Pending Setup	5	Team DNV	North Shore district	2025-12-29 08:15:01.554422	2025-12-29 08:15:01.554422
13	City of West Vancouver	Metro Vancouver	Bids and Tenders	https://westvancouver.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#7E57C2	\N	Pending Setup	5	Team West Van	Affluent municipality	2025-12-29 08:15:01.554423	2025-12-29 08:15:01.554423
14	City of Port Coquitlam	Metro Vancouver	Purchasing	https://www.portcoquitlam.ca/city-hall/doing-business-with-the-city/	Direct Website	f	\N	\N	#42A5F5	\N	Pending Setup	5	Team PoCo	Tri-Cities area	2025-12-29 08:15:01.554424	2025-12-29 08:15:01.554424
15	City of Port Moody	Metro Vancouver	Bids and Tenders	https://portmoody.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#66BB6A	\N	Pending Setup	5	Team Port Moody	Tri-Cities area	2025-12-29 08:15:01.554425	2025-12-29 08:15:01.554425
16	City of Langley	Fraser Valley	Bids and Tenders	https://langleycity.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#FFCA28	\N	Pending Setup	5	Team Langley City	Growing city	2025-12-29 08:15:01.554425	2025-12-29 08:15:01.554426
17	Township of Langley	Fraser Valley	Bids and Tenders	https://tol.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#FFA726	\N	Pending Setup	5	Team TOL	Large township - rapid growth	2025-12-29 08:15:01.554426	2025-12-29 08:15:01.554427
18	City of Abbotsford	Fraser Valley	Bids and Tenders	https://abbotsford.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#8D6E63	\N	Pending Setup	5	Team Abbotsford	Largest Fraser Valley city	2025-12-29 08:15:01.554427	2025-12-29 08:15:01.554428
19	City of Chilliwack	Fraser Valley	Purchasing	https://www.chilliwack.com/main/page.cfm?id=574	Direct Website	f	\N	\N	#78909C	\N	Pending Setup	5	Team Chilliwack	Growing Fraser Valley city	2025-12-29 08:15:01.554428	2025-12-29 08:15:01.554428
20	City of Mission	Fraser Valley	Purchasing	https://www.mission.ca/municipal-hall/purchasing/	Direct Website	f	\N	\N	#A1887F	\N	Pending Setup	5	Team Mission	Fraser Valley community	2025-12-29 08:15:01.554429	2025-12-29 08:15:01.554429
21	District of Maple Ridge	Fraser Valley	Bids and Tenders	https://mapleridge.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#90A4AE	\N	Pending Setup	5	Team Maple Ridge	Growing community	2025-12-29 08:15:01.55443	2025-12-29 08:15:01.55443
22	City of Pitt Meadows	Fraser Valley	Purchasing	https://www.pittmeadows.ca/city-services/purchasing	Direct Website	f	\N	\N	#BCAAA4	\N	Pending Setup	5	Team Pitt Meadows	Small but growing	2025-12-29 08:15:01.554431	2025-12-29 08:15:01.554431
23	District of Hope	Fraser Valley	Purchasing	https://www.hope.ca/	Direct Website	f	\N	\N	#B0BEC5	\N	Pending Setup	5	Team Hope	Eastern Fraser Valley gateway	2025-12-29 08:15:01.554432	2025-12-29 08:15:01.554432
24	Village of Harrison Hot Springs	Fraser Valley	Purchasing	https://harrisonhotsprings.ca/	Direct Website	f	\N	\N	#D7CCC8	\N	Pending Setup	5	Team Harrison	Tourism-focused small municipality	2025-12-29 08:15:01.554432	2025-12-29 08:15:01.554433
25	City of White Rock	Metro Vancouver	Bids and Tenders	https://whiterockcity.bidsandtenders.ca/Module/Tenders	BidsAndTenders Platform	t	\N	\N	#80DEEA	\N	Pending Setup	5	Team White Rock	Waterfront city	2025-12-29 08:15:01.554433	2025-12-29 08:15:01.554434
26	TransLink	Regional	Procurement	https://www.translink.ca/about-us/doing-business-with-translink/procurement	Custom Portal	t	\N	\N	#C62828	\N	Priority	5	Team TransLink	Regional transit authority - large signage contracts	2025-12-29 08:15:01.554434	2025-12-29 08:15:01.554435
27	BC Hydro	Provincial	Procurement	https://www.bchydro.com/work-with-us/suppliers.html	Custom Portal	t	\N	\N	#1565C0	\N	Research	5	Team BC Hydro	Provincial utility - potential signage work	2025-12-29 08:15:01.554435	2025-12-29 08:15:01.554435
28	Vancouver Airport Authority (YVR)	Regional	Procurement	https://www.yvr.ca/en/business/procurement	Custom Portal	t	\N	\N	#6A1B9A	\N	Priority	5	Team YVR	Major facility - significant signage needs	2025-12-29 08:15:01.554436	2025-12-29 08:15:01.554436
29	BC Ferries	Provincial	Procurement	https://www.bcferries.com/about/procurement	Custom Portal	f	\N	\N	#00838F	\N	Research	5	Team BC Ferries	Provincial ferry service	2025-12-29 08:15:01.554437	2025-12-29 08:15:01.554437
30	University of British Columbia	Education	Procurement	https://procurement.ubc.ca/	Custom Portal	t	\N	\N	#2E7D32	\N	Research	5	Team UBC	Major institution - wayfinding signage	2025-12-29 08:15:01.554438	2025-12-29 08:15:01.554438
31	Simon Fraser University	Education	Procurement	https://www.sfu.ca/finance/departments/supply-management.html	Custom Portal	t	\N	\N	#F57F17	\N	Research	5	Team SFU	Major institution	2025-12-29 08:15:01.554438	2025-12-29 08:15:01.554439
\.


--
-- Data for Name: opportunities; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.opportunities (id, source_portal, source_url, external_id, title, description, opportunity_type, category, municipality_id, issuing_department, contact_name, contact_email, contact_phone, posted_date, closing_date, closing_time, mandatory_site_visit, site_visit_date, estimated_value, estimated_value_min, estimated_value_max, currency, tier, tier_rationale, keywords_matched, relevance_score, status, assigned_to, created_at, updated_at, last_scraped_at, search_vector) FROM stdin;
\.


--
-- Data for Name: partners; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.partners (id, company_name, primary_contact, email, phone, address, website, specialties, capacity_rating, geographic_coverage, relationship_type, preferred_partner, opportunities_referred, opportunities_won, total_referral_fees, status, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: scraper_runs; Type: TABLE DATA; Schema: public; Owner: evanholmes
--

COPY public.scraper_runs (id, source_portal, start_time, end_time, opportunities_found, opportunities_new, opportunities_updated, status, error_message, duration_seconds, created_at) FROM stdin;
\.


--
-- Name: activity_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.activity_log_id_seq', 1, false);


--
-- Name: bids_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.bids_id_seq', 1, false);


--
-- Name: calendar_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.calendar_events_id_seq', 1, false);


--
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.documents_id_seq', 1, false);


--
-- Name: keywords_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.keywords_id_seq', 1, false);


--
-- Name: municipalities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.municipalities_id_seq', 31, true);


--
-- Name: opportunities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.opportunities_id_seq', 1, false);


--
-- Name: partners_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.partners_id_seq', 1, false);


--
-- Name: scraper_runs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: evanholmes
--

SELECT pg_catalog.setval('public.scraper_runs_id_seq', 1, false);


--
-- Name: activity_log activity_log_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.activity_log
    ADD CONSTRAINT activity_log_pkey PRIMARY KEY (id);


--
-- Name: bids bids_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.bids
    ADD CONSTRAINT bids_pkey PRIMARY KEY (id);


--
-- Name: calendar_events calendar_events_google_event_id_key; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.calendar_events
    ADD CONSTRAINT calendar_events_google_event_id_key UNIQUE (google_event_id);


--
-- Name: calendar_events calendar_events_opportunity_id_key; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.calendar_events
    ADD CONSTRAINT calendar_events_opportunity_id_key UNIQUE (opportunity_id);


--
-- Name: calendar_events calendar_events_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.calendar_events
    ADD CONSTRAINT calendar_events_pkey PRIMARY KEY (id);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: keywords keywords_keyword_key; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT keywords_keyword_key UNIQUE (keyword);


--
-- Name: keywords keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT keywords_pkey PRIMARY KEY (id);


--
-- Name: municipalities municipalities_name_key; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.municipalities
    ADD CONSTRAINT municipalities_name_key UNIQUE (name);


--
-- Name: municipalities municipalities_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.municipalities
    ADD CONSTRAINT municipalities_pkey PRIMARY KEY (id);


--
-- Name: opportunities opportunities_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.opportunities
    ADD CONSTRAINT opportunities_pkey PRIMARY KEY (id);


--
-- Name: partners partners_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.partners
    ADD CONSTRAINT partners_pkey PRIMARY KEY (id);


--
-- Name: scraper_runs scraper_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.scraper_runs
    ADD CONSTRAINT scraper_runs_pkey PRIMARY KEY (id);


--
-- Name: idx_activity_log_entity; Type: INDEX; Schema: public; Owner: evanholmes
--

CREATE INDEX idx_activity_log_entity ON public.activity_log USING btree (entity_type, entity_id);


--
-- Name: idx_activity_log_timestamp; Type: INDEX; Schema: public; Owner: evanholmes
--

CREATE INDEX idx_activity_log_timestamp ON public.activity_log USING btree ("timestamp");


--
-- Name: idx_opportunities_closing_date; Type: INDEX; Schema: public; Owner: evanholmes
--

CREATE INDEX idx_opportunities_closing_date ON public.opportunities USING btree (closing_date);


--
-- Name: idx_opportunities_municipality; Type: INDEX; Schema: public; Owner: evanholmes
--

CREATE INDEX idx_opportunities_municipality ON public.opportunities USING btree (municipality_id);


--
-- Name: idx_opportunities_status; Type: INDEX; Schema: public; Owner: evanholmes
--

CREATE INDEX idx_opportunities_status ON public.opportunities USING btree (status);


--
-- Name: idx_opportunities_tier; Type: INDEX; Schema: public; Owner: evanholmes
--

CREATE INDEX idx_opportunities_tier ON public.opportunities USING btree (tier);


--
-- Name: idx_scraper_runs_portal; Type: INDEX; Schema: public; Owner: evanholmes
--

CREATE INDEX idx_scraper_runs_portal ON public.scraper_runs USING btree (source_portal, start_time);


--
-- Name: bids bids_opportunity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.bids
    ADD CONSTRAINT bids_opportunity_id_fkey FOREIGN KEY (opportunity_id) REFERENCES public.opportunities(id) ON DELETE CASCADE;


--
-- Name: bids bids_partner_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.bids
    ADD CONSTRAINT bids_partner_company_id_fkey FOREIGN KEY (partner_company_id) REFERENCES public.partners(id);


--
-- Name: calendar_events calendar_events_opportunity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.calendar_events
    ADD CONSTRAINT calendar_events_opportunity_id_fkey FOREIGN KEY (opportunity_id) REFERENCES public.opportunities(id) ON DELETE CASCADE;


--
-- Name: documents documents_opportunity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_opportunity_id_fkey FOREIGN KEY (opportunity_id) REFERENCES public.opportunities(id) ON DELETE CASCADE;


--
-- Name: opportunities opportunities_municipality_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: evanholmes
--

ALTER TABLE ONLY public.opportunities
    ADD CONSTRAINT opportunities_municipality_id_fkey FOREIGN KEY (municipality_id) REFERENCES public.municipalities(id);


--
-- PostgreSQL database dump complete
--

\unrestrict mF61fKV12ROXLo9AkMRrWgzaFkrR1UiCLh9vNIullHZI3E6clykGs33oN1vMvJl

