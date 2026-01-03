'use client';

import { Sidebar } from '@/components/shared/Sidebar';
import {
  TrendingUp,
  Clock,
  Send,
  Trophy,
  Target,
  AlertTriangle,
  CheckCircle2,
  Bot,
  Building2,
  Calendar,
  ArrowRight,
  Zap
} from 'lucide-react';

// Mock data
const stats = {
  activeBids: 12,
  activeBidsTrend: '+2 today',
  pendingDecision: 5,
  submittedAwaiting: 3,
  wonThisQuarter: 4,
  wonValue: '$245K',
  winRate: '34%',
  winRateTrend: '+5% YoY',
};

const upcomingDeadlines = [
  { id: 1, name: 'Surrey Transit Signs', municipality: 'Surrey', daysLeft: 2, value: '$180K', urgency: 'critical' },
  { id: 2, name: 'Vancouver Park Wayfinding', municipality: 'Vancouver', daysLeft: 5, value: '$85K', urgency: 'warning' },
  { id: 3, name: 'Burnaby Civic Signage', municipality: 'Burnaby', daysLeft: 10, value: '$95K', urgency: 'normal' },
];

const pipelineData = {
  discovery: 8,
  analysis: 4,
  draft: 6,
  review: 3,
  submit: 5,
  awarded: 4,
};

const activityLog = [
  { time: '10:34 AM', icon: '🤖', message: 'Approved proposal for Surrey Transit Signs - Ready to submit' },
  { time: '10:12 AM', icon: '📋', message: 'New opportunity detected: Richmond City Hall Wayfinding' },
  { time: '09:45 AM', icon: '✅', message: 'Submitted bid: Vancouver Park Regulatory Signs' },
  { time: '09:30 AM', icon: '🔍', message: 'Analyzed: Coquitlam Trail Signage - Recommend GO' },
];

const teamStatus = [
  { name: 'Vancouver', active: 8, color: '#F4B400' },
  { name: 'Surrey', active: 6, color: '#AB47BC' },
  { name: 'Burnaby', active: 4, color: '#00ACC1' },
  { name: 'Metro Van', active: 3, color: '#4285F4' },
  { name: 'Richmond', active: 2, color: '#FF7043' },
  { name: 'Langley', active: 2, color: '#FFA726' },
];

export default function CEODashboard() {
  return (
    <div className="flex h-screen bg-[#0a0a0a]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        {/* Header */}
        <header className="sticky top-0 z-10 bg-[#0a0a0a]/80 backdrop-blur-sm border-b border-[#262626]">
          <div className="flex items-center justify-between px-6 py-4">
            <div>
              <h1 className="text-2xl font-bold text-white">CEO Dashboard</h1>
              <p className="text-sm text-gray-500">ALL-PRO SIGNS & WESTCOAST CNC</p>
            </div>
            <div className="flex items-center gap-4">
              <button className="flex items-center gap-2 px-4 py-2 bg-[#1a1a1a] border border-[#262626] rounded-lg text-sm text-gray-300 hover:bg-[#262626] transition-colors">
                <Calendar className="w-4 h-4" />
                December 2025
              </button>
              <div className="relative">
                <button className="p-2 bg-[#1a1a1a] border border-[#262626] rounded-lg text-gray-300 hover:bg-[#262626] transition-colors">
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs flex items-center justify-center text-white">3</span>
                  🔔
                </button>
              </div>
            </div>
          </div>
        </header>

        <div className="p-6 space-y-6">
          {/* Stats Row */}
          <div className="grid grid-cols-5 gap-4">
            <StatCard
              icon={<Zap className="w-5 h-5 text-blue-400" />}
              label="Active Bids"
              value={stats.activeBids}
              trend={stats.activeBidsTrend}
              trendUp={true}
            />
            <StatCard
              icon={<Clock className="w-5 h-5 text-amber-400" />}
              label="Pending Decision"
              value={stats.pendingDecision}
            />
            <StatCard
              icon={<Send className="w-5 h-5 text-purple-400" />}
              label="Submitted Awaiting"
              value={stats.submittedAwaiting}
            />
            <StatCard
              icon={<Trophy className="w-5 h-5 text-green-400" />}
              label="Won This Quarter"
              value={stats.wonValue}
              subtitle={`${stats.wonThisQuarter} wins`}
            />
            <StatCard
              icon={<Target className="w-5 h-5 text-cyan-400" />}
              label="Win Rate"
              value={stats.winRate}
              trend={stats.winRateTrend}
              trendUp={true}
            />
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-2 gap-6">
            {/* Upcoming Deadlines */}
            <div className="bg-[#141414] border border-[#262626] rounded-lg">
              <div className="px-4 py-3 border-b border-[#262626] flex items-center justify-between">
                <h2 className="font-semibold text-white">Upcoming Deadlines</h2>
                <span className="text-xs text-gray-500">Next 14 days</span>
              </div>
              <div className="p-4 space-y-3">
                {upcomingDeadlines.map((bid) => (
                  <DeadlineItem key={bid.id} bid={bid} />
                ))}
                <button className="w-full py-2 text-sm text-blue-400 hover:text-blue-300 flex items-center justify-center gap-1">
                  View All <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Bid Pipeline */}
            <div className="bg-[#141414] border border-[#262626] rounded-lg">
              <div className="px-4 py-3 border-b border-[#262626]">
                <h2 className="font-semibold text-white">Bid Pipeline</h2>
              </div>
              <div className="p-4">
                <div className="flex items-end justify-between h-32 gap-2">
                  <PipelineBar label="Discovery" count={pipelineData.discovery} color="bg-blue-500" />
                  <PipelineBar label="Analysis" count={pipelineData.analysis} color="bg-purple-500" />
                  <PipelineBar label="Draft" count={pipelineData.draft} color="bg-amber-500" />
                  <PipelineBar label="Review" count={pipelineData.review} color="bg-orange-500" />
                  <PipelineBar label="Submit" count={pipelineData.submit} color="bg-green-500" />
                  <PipelineBar label="Awarded" count={pipelineData.awarded} color="bg-emerald-500" />
                </div>
              </div>
            </div>
          </div>

          {/* Second Row */}
          <div className="grid grid-cols-2 gap-6">
            {/* Agent Team Status */}
            <div className="bg-[#141414] border border-[#262626] rounded-lg">
              <div className="px-4 py-3 border-b border-[#262626] flex items-center justify-between">
                <h2 className="font-semibold text-white">Agent Team Status</h2>
                <span className="text-xs text-green-400 flex items-center gap-1">
                  <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                  24 teams online
                </span>
              </div>
              <div className="p-4 space-y-3">
                {teamStatus.map((team) => (
                  <TeamStatusBar key={team.name} team={team} />
                ))}
                <p className="text-xs text-gray-500 text-center pt-2">+18 more teams</p>
              </div>
            </div>

            {/* Activity Log */}
            <div className="bg-[#141414] border border-[#262626] rounded-lg">
              <div className="px-4 py-3 border-b border-[#262626] flex items-center justify-between">
                <h2 className="font-semibold text-white">BID MASTER Activity</h2>
                <Bot className="w-4 h-4 text-purple-400" />
              </div>
              <div className="p-4 space-y-3">
                {activityLog.map((item, idx) => (
                  <div key={idx} className="flex gap-3 text-sm">
                    <span className="text-gray-500 w-16 flex-shrink-0">{item.time}</span>
                    <span className="flex-shrink-0">{item.icon}</span>
                    <span className="text-gray-300">{item.message}</span>
                  </div>
                ))}
                <button className="w-full py-2 text-sm text-blue-400 hover:text-blue-300 flex items-center justify-center gap-1">
                  View Full Log <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          {/* Deal Flow Summary */}
          <div className="bg-[#141414] border border-[#262626] rounded-lg">
            <div className="px-4 py-3 border-b border-[#262626]">
              <h2 className="font-semibold text-white">Deal Flow Classification - December 2025</h2>
            </div>
            <div className="p-4">
              <div className="grid grid-cols-5 gap-4">
                <DealFlowCard category="FULFILL" count={12} color="bg-green-500" desc="Direct bids" />
                <DealFlowCard category="PARTNER" count={4} color="bg-purple-500" desc="Joint ventures" />
                <DealFlowCard category="ASSIGN" count={6} color="bg-blue-500" desc="Referrals" />
                <DealFlowCard category="BROKER" count={2} color="bg-amber-500" desc="Consulting" />
                <DealFlowCard category="ARCHIVE" count={4} color="bg-gray-500" desc="Not pursued" />
              </div>
              <div className="mt-4 pt-4 border-t border-[#262626] flex items-center justify-between text-sm">
                <span className="text-gray-400">28 opportunities detected this month</span>
                <div className="flex items-center gap-6">
                  <span className="text-gray-300">Revenue: <span className="text-green-400 font-semibold">$246,000</span></span>
                  <span className="text-gray-500">Direct: $185K | Partner: $45K | Referral: $12.5K | Consulting: $3.5K</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

// Component: Stat Card
function StatCard({ icon, label, value, trend, trendUp, subtitle }: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  trend?: string;
  trendUp?: boolean;
  subtitle?: string;
}) {
  return (
    <div className="bg-[#141414] border border-[#262626] rounded-lg p-4">
      <div className="flex items-center gap-2 mb-2">
        {icon}
        <span className="text-sm text-gray-400">{label}</span>
      </div>
      <div className="text-3xl font-bold text-white">{value}</div>
      {trend && (
        <div className={`text-xs mt-1 ${trendUp ? 'text-green-400' : 'text-red-400'}`}>
          {trend}
        </div>
      )}
      {subtitle && (
        <div className="text-xs text-gray-500 mt-1">{subtitle}</div>
      )}
    </div>
  );
}

// Component: Deadline Item
function DeadlineItem({ bid }: { bid: typeof upcomingDeadlines[0] }) {
  const urgencyStyles = {
    critical: 'bg-red-500/20 border-red-500/30 text-red-400',
    warning: 'bg-amber-500/20 border-amber-500/30 text-amber-400',
    normal: 'bg-gray-500/20 border-gray-500/30 text-gray-400',
  };

  const urgencyIcon = {
    critical: <AlertTriangle className="w-4 h-4" />,
    warning: <Clock className="w-4 h-4" />,
    normal: <CheckCircle2 className="w-4 h-4" />,
  };

  return (
    <div className={`p-3 rounded-lg border ${urgencyStyles[bid.urgency as keyof typeof urgencyStyles]}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {urgencyIcon[bid.urgency as keyof typeof urgencyIcon]}
          <div>
            <div className="font-medium text-white text-sm">{bid.name}</div>
            <div className="text-xs text-gray-500">{bid.municipality} • {bid.value}</div>
          </div>
        </div>
        <div className="text-right">
          <div className={`font-bold ${bid.urgency === 'critical' ? 'text-red-400' : 'text-gray-300'}`}>
            {bid.daysLeft} days
          </div>
        </div>
      </div>
    </div>
  );
}

// Component: Pipeline Bar
function PipelineBar({ label, count, color }: { label: string; count: number; color: string }) {
  const maxCount = 10;
  const height = (count / maxCount) * 100;

  return (
    <div className="flex flex-col items-center flex-1">
      <div className="w-full h-24 bg-[#1a1a1a] rounded-t-lg relative flex items-end">
        <div
          className={`w-full ${color} rounded-t-lg transition-all duration-500`}
          style={{ height: `${height}%` }}
        />
      </div>
      <div className="text-lg font-bold text-white mt-2">{count}</div>
      <div className="text-xs text-gray-500">{label}</div>
    </div>
  );
}

// Component: Team Status Bar
function TeamStatusBar({ team }: { team: typeof teamStatus[0] }) {
  const maxActive = 10;
  const width = (team.active / maxActive) * 100;

  return (
    <div className="flex items-center gap-3">
      <div className="w-20 text-sm text-gray-300">{team.name}</div>
      <div className="flex-1 h-2 bg-[#1a1a1a] rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${width}%`, backgroundColor: team.color }}
        />
      </div>
      <div className="w-16 text-sm text-gray-400 text-right">{team.active} active</div>
    </div>
  );
}

// Component: Deal Flow Card
function DealFlowCard({ category, count, color, desc }: {
  category: string;
  count: number;
  color: string;
  desc: string;
}) {
  return (
    <div className="text-center">
      <div className={`w-12 h-12 ${color} rounded-full mx-auto flex items-center justify-center text-white font-bold text-lg`}>
        {count}
      </div>
      <div className="mt-2 font-medium text-white text-sm">{category}</div>
      <div className="text-xs text-gray-500">{desc}</div>
    </div>
  );
}
