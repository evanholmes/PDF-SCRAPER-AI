"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Bot,
  Building2,
  GitBranch,
  Calendar,
  FileText,
  Users,
  Settings,
  ChevronLeft,
  ChevronRight,
  Zap,
  ClipboardCheck,
} from "lucide-react";

const navigation = [
  { name: "CEO Dashboard", href: "/", icon: LayoutDashboard },
  { name: "BC Bid Checklist", href: "/bc-bid-checklist", icon: ClipboardCheck },
  { name: "BID MASTER", href: "/bid-master", icon: Bot },
  { name: "Municipalities", href: "/municipalities", icon: Building2 },
  { name: "Deal Flow", href: "/deal-flow", icon: GitBranch },
  { name: "Calendar", href: "/calendar", icon: Calendar },
  { name: "Proposals", href: "/proposals", icon: FileText },
  { name: "Partners", href: "/partners", icon: Users },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <div
      className={cn(
        "flex flex-col bg-[#0f0f0f] border-r border-[#262626] transition-all duration-300",
        collapsed ? "w-16" : "w-64",
      )}
    >
      {/* Logo */}
      <div className="flex items-center h-16 px-4 border-b border-[#262626]">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <Zap className="w-5 h-5 text-white" />
          </div>
          {!collapsed && (
            <div>
              <h1 className="font-bold text-white">BID-AI</h1>
              <p className="text-[10px] text-gray-500">The Bid Master</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4">
        <ul className="space-y-1 px-2">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors",
                    isActive
                      ? "bg-blue-500/10 text-blue-400"
                      : "text-gray-400 hover:text-white hover:bg-[#1a1a1a]",
                  )}
                >
                  <item.icon className="w-5 h-5 flex-shrink-0" />
                  {!collapsed && <span>{item.name}</span>}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Collapse Toggle */}
      <div className="p-4 border-t border-[#262626]">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex items-center justify-center w-full py-2 text-gray-400 hover:text-white transition-colors"
        >
          {collapsed ? (
            <ChevronRight className="w-5 h-5" />
          ) : (
            <>
              <ChevronLeft className="w-5 h-5 mr-2" />
              <span className="text-sm">Collapse</span>
            </>
          )}
        </button>
      </div>

      {/* Company Badge */}
      {!collapsed && (
        <div className="p-4 border-t border-[#262626]">
          <div className="text-xs text-gray-500 text-center">
            <p className="font-medium text-gray-400">ALL-PRO SIGNS</p>
            <p>&amp; WESTCOAST CNC</p>
          </div>
        </div>
      )}
    </div>
  );
}
