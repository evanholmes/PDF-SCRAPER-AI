'use client';

import { Sidebar } from '@/components/shared/Sidebar';
import { BCBidChecklist } from '@/components/BCBidChecklist';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function BCBidChecklistPage() {
  return (
    <div className="flex h-screen bg-[#0a0a0a]">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        {/* Header */}
        <header className="sticky top-0 z-10 bg-[#0a0a0a]/80 backdrop-blur-sm border-b border-[#262626]">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center gap-4">
              <Link
                href="/"
                className="p-2 text-gray-400 hover:text-white hover:bg-[#1a1a1a] rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-white">BC Bid Requirements Checklist</h1>
                <p className="text-sm text-gray-500">Complete all items to be ready to bid on BC government contracts</p>
              </div>
            </div>
          </div>
        </header>

        <div className="p-6 max-w-4xl">
          <BCBidChecklist />
        </div>
      </main>
    </div>
  );
}
