'use client';

import { useState, useEffect } from 'react';
import {
  CheckCircle2,
  Circle,
  ExternalLink,
  ChevronDown,
  ChevronRight,
  AlertTriangle,
  Clock,
  Shield,
  Building2,
  FileText,
  DollarSign,
  Users,
  Briefcase,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChecklistItem {
  id: string;
  label: string;
  description: string;
  link?: string;
  linkLabel?: string;
  estimatedTime?: string;
  cost?: string;
}

interface ChecklistCategory {
  id: string;
  title: string;
  icon: React.ReactNode;
  description: string;
  items: ChecklistItem[];
}

const checklistData: ChecklistCategory[] = [
  {
    id: 'registration',
    title: '1. Registration & Business Setup',
    icon: <Building2 className="w-5 h-5" />,
    description: 'Essential registrations to get started',
    items: [
      {
        id: 'bceid',
        label: 'Obtain Business BCeID',
        description: 'Required for BC Bid login. Allow several weeks for processing.',
        link: 'https://www.bceid.ca/',
        linkLabel: 'BCeID Portal',
        estimatedTime: '2-4 weeks',
      },
      {
        id: 'business-registration',
        label: 'Register Business with BC Registries',
        description: 'Sole proprietorships and partnerships must register.',
        link: 'https://www.bcregistry.gov.bc.ca/',
        linkLabel: 'BC Registries',
        estimatedTime: '1-2 days',
        cost: '$40 (sole prop) + $30 (name)',
      },
      {
        id: 'bcbid-account',
        label: 'Create BC Bid Account',
        description: 'Register on BC Bid portal. First registrant becomes Supplier Admin.',
        link: 'https://www.bcbid.gov.bc.ca/',
        linkLabel: 'BC Bid Portal',
        estimatedTime: '1-3 days',
      },
      {
        id: 'commodity-codes',
        label: 'Subscribe to UNSPSC Commodity Codes',
        description: 'Select relevant codes to receive opportunity notifications.',
        link: 'https://www2.gov.bc.ca/gov/content/bc-procurement-resources/bc-bid-resources/bc-bid-user-guides/bc-bid-supplier-guide',
        linkLabel: 'Supplier Guide',
        estimatedTime: '30 minutes',
      },
    ],
  },
  {
    id: 'compliance',
    title: '2. Compliance Requirements',
    icon: <Shield className="w-5 h-5" />,
    description: 'Mandatory compliance for BC government contracts',
    items: [
      {
        id: 'worksafebc',
        label: 'Register with WorkSafeBC',
        description: 'Obtain clearance letter confirming registration and premiums paid.',
        link: 'https://www.worksafebc.com/',
        linkLabel: 'WorkSafeBC',
        estimatedTime: '1-2 weeks',
      },
      {
        id: 'worksafebc-clearance',
        label: 'Obtain WorkSafeBC Clearance Letter',
        description: 'Required before commencement of work. Renew annually.',
        link: 'https://www.worksafebc.com/en/insurance/need-coverage/clearance-letters',
        linkLabel: 'Clearance Letters',
        estimatedTime: '1-3 days',
      },
      {
        id: 'tax-verification',
        label: 'Prepare Tax Verification Letter Access',
        description: 'Required for contracts $100K+. Obtain from eTaxBC portal.',
        link: 'https://www2.gov.bc.ca/gov/content/taxes/etaxbc',
        linkLabel: 'eTaxBC Portal',
        estimatedTime: 'Instant (online)',
      },
    ],
  },
  {
    id: 'insurance',
    title: '3. Insurance Requirements',
    icon: <FileText className="w-5 h-5" />,
    description: 'Standard insurance coverage for government contracts',
    items: [
      {
        id: 'cgl',
        label: 'Commercial General Liability (CGL) Insurance',
        description: 'Minimum $2,000,000 per occurrence. Include Blanket Contractual Liability.',
        estimatedTime: '1-2 weeks',
        cost: 'Varies by coverage',
      },
      {
        id: 'auto-liability',
        label: 'Automobile Liability Insurance',
        description: 'Minimum $5,000,000 if services require vehicle use.',
        estimatedTime: '1-2 weeks',
        cost: 'Varies by coverage',
      },
      {
        id: 'eo-insurance',
        label: 'Errors & Omissions Insurance (Professional Services)',
        description: 'Required for professional/consulting services contracts.',
        estimatedTime: '1-2 weeks',
        cost: 'Varies by coverage',
      },
      {
        id: 'insurance-certificates',
        label: 'Prepare Insurance Certificates',
        description: 'Have current certificates ready for upload to BC Bid.',
        estimatedTime: '1-3 days',
      },
    ],
  },
  {
    id: 'bonding',
    title: '4. Bonding (Construction Projects)',
    icon: <DollarSign className="w-5 h-5" />,
    description: 'Required for construction contracts over threshold values',
    items: [
      {
        id: 'surety-relationship',
        label: 'Establish Surety Company Relationship',
        description: 'Required for bid bonds, performance bonds, and payment bonds.',
        link: 'https://bccassn.com/',
        linkLabel: 'BC Construction Association',
        estimatedTime: '2-4 weeks',
      },
      {
        id: 'financial-statements',
        label: 'Prepare 3 Years of Financial Statements',
        description: 'Reviewed or audited statements required for surety underwriting.',
        estimatedTime: 'Varies',
      },
      {
        id: 'bonding-capacity',
        label: 'Confirm Bonding Capacity',
        description: 'Ensure capacity supports project sizes you plan to bid on.',
        estimatedTime: '1-2 weeks',
      },
    ],
  },
  {
    id: 'documents',
    title: '5. Bid Document Preparation',
    icon: <Briefcase className="w-5 h-5" />,
    description: 'Standard documents to have ready for submissions',
    items: [
      {
        id: 'company-profile',
        label: 'Prepare Company Profile',
        description: 'Standard company overview, capabilities, and experience.',
        estimatedTime: '2-4 hours',
      },
      {
        id: 'past-projects',
        label: 'Document Past Project Experience',
        description: 'Portfolio of relevant completed projects with references.',
        estimatedTime: '4-8 hours',
      },
      {
        id: 'key-personnel',
        label: 'Prepare Key Personnel Resumes',
        description: 'Resumes of key team members who will work on projects.',
        estimatedTime: '2-4 hours',
      },
      {
        id: 'references',
        label: 'Gather Client References',
        description: 'Contact info for 3+ clients who can provide references.',
        estimatedTime: '1-2 hours',
      },
    ],
  },
  {
    id: 'optional',
    title: '6. Optional / Specialized',
    icon: <Users className="w-5 h-5" />,
    description: 'Additional certifications and programs',
    items: [
      {
        id: 'gold-seal',
        label: 'Gold Seal Certification (Construction)',
        description: 'Recommended for Site Superintendents on projects over $5M.',
        link: 'https://www.goldsealcertification.com/',
        linkLabel: 'Gold Seal Program',
        estimatedTime: 'Several months',
      },
      {
        id: 'indigenous-procurement',
        label: 'Indigenous Procurement Initiative Registration',
        description: 'Program still developing. Contact for current opportunities.',
        link: 'mailto:ipi@gov.bc.ca',
        linkLabel: 'Contact IPI',
      },
      {
        id: 'bcspi',
        label: 'BC Social Procurement Initiative',
        description: 'Local government procurement opportunities.',
        link: 'https://bcspi.ca/',
        linkLabel: 'BCSPI Website',
      },
    ],
  },
];

const STORAGE_KEY = 'bcbid-checklist-state';

export function BCBidChecklist() {
  const [checkedItems, setCheckedItems] = useState<Record<string, boolean>>({});
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({
    registration: true,
    compliance: true,
    insurance: true,
    bonding: true,
    documents: true,
    optional: false,
  });

  // Load state from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        setCheckedItems(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to load checklist state:', e);
      }
    }
  }, []);

  // Save state to localStorage on change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(checkedItems));
  }, [checkedItems]);

  const toggleItem = (itemId: string) => {
    setCheckedItems((prev) => ({
      ...prev,
      [itemId]: !prev[itemId],
    }));
  };

  const toggleCategory = (categoryId: string) => {
    setExpandedCategories((prev) => ({
      ...prev,
      [categoryId]: !prev[categoryId],
    }));
  };

  const getCategoryProgress = (category: ChecklistCategory) => {
    const completed = category.items.filter((item) => checkedItems[item.id]).length;
    return { completed, total: category.items.length };
  };

  const getTotalProgress = () => {
    const allItems = checklistData.flatMap((cat) => cat.items);
    const completed = allItems.filter((item) => checkedItems[item.id]).length;
    return { completed, total: allItems.length };
  };

  const totalProgress = getTotalProgress();
  const progressPercent = Math.round((totalProgress.completed / totalProgress.total) * 100);

  return (
    <div className="space-y-6">
      {/* Overall Progress */}
      <div className="bg-[#141414] border border-[#262626] rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-white">BC Bid Readiness</h2>
            <p className="text-sm text-gray-400">Complete all requirements to start bidding</p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-white">{progressPercent}%</div>
            <div className="text-sm text-gray-400">
              {totalProgress.completed} of {totalProgress.total} items
            </div>
          </div>
        </div>
        <div className="w-full h-3 bg-[#1a1a1a] rounded-full overflow-hidden">
          <div
            className={cn(
              'h-full rounded-full transition-all duration-500',
              progressPercent === 100 ? 'bg-green-500' : 'bg-blue-500'
            )}
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        {progressPercent === 100 && (
          <div className="mt-4 flex items-center gap-2 text-green-400">
            <CheckCircle2 className="w-5 h-5" />
            <span className="font-medium">Ready to bid on BC Bid!</span>
          </div>
        )}
      </div>

      {/* Quick Links */}
      <div className="bg-[#141414] border border-[#262626] rounded-lg p-4">
        <h3 className="text-sm font-semibold text-white mb-3">Quick Links</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <QuickLink href="https://www.bcbid.gov.bc.ca/" label="BC Bid Portal" />
          <QuickLink href="https://www.bceid.ca/" label="BCeID" />
          <QuickLink href="https://www.worksafebc.com/" label="WorkSafeBC" />
          <QuickLink href="https://www.bcregistry.gov.bc.ca/" label="BC Registries" />
        </div>
      </div>

      {/* Checklist Categories */}
      <div className="space-y-4">
        {checklistData.map((category) => {
          const progress = getCategoryProgress(category);
          const isExpanded = expandedCategories[category.id];
          const isComplete = progress.completed === progress.total;

          return (
            <div
              key={category.id}
              className="bg-[#141414] border border-[#262626] rounded-lg overflow-hidden"
            >
              {/* Category Header */}
              <button
                onClick={() => toggleCategory(category.id)}
                className="w-full px-4 py-3 flex items-center justify-between hover:bg-[#1a1a1a] transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={cn(
                      'p-2 rounded-lg',
                      isComplete ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'
                    )}
                  >
                    {category.icon}
                  </div>
                  <div className="text-left">
                    <h3 className="font-semibold text-white">{category.title}</h3>
                    <p className="text-xs text-gray-500">{category.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <span
                      className={cn(
                        'text-sm font-medium',
                        isComplete ? 'text-green-400' : 'text-gray-400'
                      )}
                    >
                      {progress.completed}/{progress.total}
                    </span>
                    {isComplete && <CheckCircle2 className="w-4 h-4 text-green-400" />}
                  </div>
                  {isExpanded ? (
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  ) : (
                    <ChevronRight className="w-5 h-5 text-gray-400" />
                  )}
                </div>
              </button>

              {/* Category Items */}
              {isExpanded && (
                <div className="border-t border-[#262626] divide-y divide-[#262626]">
                  {category.items.map((item) => (
                    <ChecklistItemRow
                      key={item.id}
                      item={item}
                      checked={checkedItems[item.id] || false}
                      onToggle={() => toggleItem(item.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Help Section */}
      <div className="bg-[#141414] border border-[#262626] rounded-lg p-4">
        <h3 className="text-sm font-semibold text-white mb-3">Need Help?</h3>
        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2 text-gray-400">
            <span className="font-medium text-gray-300">BC Bid Help Desk:</span>
            <a href="mailto:bcbid@gov.bc.ca" className="text-blue-400 hover:underline">
              bcbid@gov.bc.ca
            </a>
            <span>|</span>
            <span>250-387-7301</span>
          </div>
          <div className="flex items-center gap-2 text-gray-400">
            <span className="font-medium text-gray-300">BC Registries:</span>
            <span>1-877-370-1033</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function ChecklistItemRow({
  item,
  checked,
  onToggle,
}: {
  item: ChecklistItem;
  checked: boolean;
  onToggle: () => void;
}) {
  return (
    <div
      className={cn(
        'px-4 py-3 flex items-start gap-3 transition-colors',
        checked ? 'bg-green-500/5' : 'hover:bg-[#1a1a1a]'
      )}
    >
      <button
        onClick={onToggle}
        className="mt-0.5 flex-shrink-0 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
      >
        {checked ? (
          <CheckCircle2 className="w-5 h-5 text-green-400" />
        ) : (
          <Circle className="w-5 h-5 text-gray-500 hover:text-gray-400" />
        )}
      </button>
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h4
              className={cn(
                'font-medium text-sm',
                checked ? 'text-gray-500 line-through' : 'text-white'
              )}
            >
              {item.label}
            </h4>
            <p className="text-xs text-gray-500 mt-0.5">{item.description}</p>
          </div>
          {item.link && (
            <a
              href={item.link}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 flex-shrink-0"
            >
              {item.linkLabel || 'Link'}
              <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>
        {(item.estimatedTime || item.cost) && (
          <div className="flex items-center gap-4 mt-2">
            {item.estimatedTime && (
              <div className="flex items-center gap-1 text-xs text-gray-500">
                <Clock className="w-3 h-3" />
                {item.estimatedTime}
              </div>
            )}
            {item.cost && (
              <div className="flex items-center gap-1 text-xs text-amber-500">
                <DollarSign className="w-3 h-3" />
                {item.cost}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function QuickLink({ href, label }: { href: string; label: string }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center justify-center gap-2 px-3 py-2 bg-[#1a1a1a] border border-[#262626] rounded-lg text-sm text-gray-300 hover:bg-[#262626] hover:text-white transition-colors"
    >
      {label}
      <ExternalLink className="w-3 h-3" />
    </a>
  );
}
