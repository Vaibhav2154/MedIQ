"use client";
import React from 'react';
import Link from 'next/link';
import { LayoutDashboard, Database, ShieldCheck, Activity } from 'lucide-react';

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const menuItems = [
    { name: 'Dashboard', href: '/client/dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'Health Records', href: '/client/records', icon: <Database size={20} /> },
    { name: 'Enforcement Logs', href: '/client/enforcement', icon: <ShieldCheck size={20} /> },
  ];

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 p-6 flex flex-col gap-8">
        <div className="flex items-center gap-2 font-bold text-xl text-med-green">
          <Activity /> MedIQ Provider
        </div>
        <nav className="flex flex-col gap-2">
          {menuItems.map((item) => (
            <Link key={item.name} href={item.href} className="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-slate-50 text-slate-600 font-semibold transition-all">
              {item.icon} {item.name}
            </Link>
          ))}
        </nav>
      </aside>
      
      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}