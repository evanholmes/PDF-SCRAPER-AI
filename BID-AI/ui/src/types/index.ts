// Core Types for BID-AI System

export type Tier = 1 | 2 | 3;

export type DealFlowCategory =
  | "fulfill"
  | "partner"
  | "assign"
  | "broker"
  | "archive";

export type BidStatus =
  | "discovery"
  | "analysis"
  | "decision"
  | "drafting"
  | "review"
  | "submitted"
  | "awarded"
  | "lost"
  | "no-bid";

export type AgentStatus = "active" | "working" | "idle" | "error";

export interface Municipality {
  id: string;
  name: string;
  shortName: string;
  region: "metro-vancouver" | "fraser-valley" | "special-agency";
  tier: Tier;
  teamId: string;
  calendarColor: string;
  portalUrl: string;
  portalType: "bidsandtenders" | "vendorlink" | "direct" | "custom";
  accountRequired: boolean;
  status: "active" | "pending" | "research";
}

export interface Bid {
  id: string;
  externalId: string; // e.g., "VAN-2025-127"
  title: string;
  municipality: Municipality;
  status: BidStatus;
  dealFlowCategory: DealFlowCategory;

  // Dates
  postedDate: Date;
  qaDeadline?: Date;
  submissionDeadline: Date;
  awardExpected?: Date;

  // Values
  estimatedValue?: number;
  actualValue?: number;

  // Assessment
  relevanceScore: number;
  capabilityScore: number;
  winProbability?: number;

  // Classification
  materialsFit: number; // 0-100
  equipmentFit: number; // 0-100
  capacityFit: number; // 0-100

  // Relationships
  assignedTeam: string;
  partnerId?: string;

  // Documents
  portalLink: string;
  documentsDownloaded: boolean;

  // Notes
  notes: string[];
}

export interface AgentTeam {
  id: string;
  municipality: Municipality;
  agents: {
    scout: AgentInstance;
    analyst: AgentInstance;
    writer: AgentInstance;
    compliance: AgentInstance;
  };
  activeBids: number;
  lastScan: Date;
}

export interface AgentInstance {
  type: "scout" | "analyst" | "writer" | "compliance";
  status: AgentStatus;
  currentTask?: string;
  lastActivity: Date;
}

export interface Partner {
  id: string;
  companyName: string;
  contactName: string;
  contactEmail: string;
  contactPhone: string;
  specialties: string[];
  relationshipStatus: "prospect" | "active" | "preferred";
  dealsReferred: number;
  dealsCompleted: number;
  revenueGenerated: number;
}

export interface DealFlowMetrics {
  period: string;
  opportunitiesDetected: number;
  classified: {
    fulfill: number;
    partner: number;
    assign: number;
    broker: number;
    archive: number;
  };
  bidsSubmitted: number;
  wins: number;
  losses: number;
  pending: number;
  revenue: {
    direct: number;
    partner: number;
    referral: number;
    consulting: number;
  };
}

export interface DashboardStats {
  activeBids: number;
  activeBidsTrend: number;
  pendingDecision: number;
  submittedAwaiting: number;
  wonThisQuarter: number;
  wonThisQuarterValue: number;
  winRate: number;
  winRateTrend: number;
}

export interface ActivityLogEntry {
  id: string;
  timestamp: Date;
  type: "opportunity" | "analysis" | "submission" | "decision" | "alert";
  icon: string;
  message: string;
  bidId?: string;
  municipalityId?: string;
}
