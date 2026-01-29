"use client";
import { useState } from 'react';
import Link from 'next/link';
import { 
  ChevronDown, Shield, Zap, Lock, Terminal, Building2, 
  Microscope, Database, Cpu, BookOpen, CheckCircle, 
  FileText, ArrowRight 
} from 'lucide-react';

export default function Navbar() {
  const [activeMenu, setActiveMenu] = useState<string | null>(null);

  const navigation = [
    { 
      name: 'Platform', 
      items: [
        { title: 'Consent Engine', desc: 'AI-powered policy extraction', icon: <Zap size={16}/> },
        { title: 'Policy Enforcement', desc: 'Machine-readable digital rules', icon: <Lock size={16}/> },
        { title: 'Audit & Compliance', desc: 'Real-time verifiable trails', icon: <Shield size={16}/> },
        { title: 'Research Gateway', desc: 'Safe access for investigators', icon: <Terminal size={16}/> }
      ] 
    },
    { 
      name: 'Solutions', 
      items: [
        { title: 'For Hospitals', desc: 'Automate data exchange', icon: <Building2 size={16}/> },
        { title: 'For Researchers', desc: 'Compliant data sourcing', icon: <Microscope size={16}/> },
        { title: 'Health Platforms', desc: 'Infrastructure integration', icon: <Database size={16}/> }
      ] 
    },
    { 
      name: 'Standards', 
      items: [
        { title: 'ABDM Alignment', desc: 'M3 & UHI', icon: <CheckCircle size={16}/> },
        { title: 'FHIR v4.0.1', desc: 'Interoperable standards', icon: <FileText size={16}/> }
      ] 
    }
  ];

  return (
    <nav className="sticky top-0 z-[100] bg-med-green text-white border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-serif text-xl font-bold tracking-tight">
          <Shield size={24} className="text-white" /> 
          <span>MedIQ</span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-8">
          {navigation.map((menu) => (
            <div 
              key={menu.name} 
              className="relative py-5"
              onMouseEnter={() => setActiveMenu(menu.name)}
              onMouseLeave={() => setActiveMenu(null)}
            >
              <button className="flex items-center gap-1 text-sm font-semibold opacity-90 hover:opacity-100 transition-all">
                {menu.name} <ChevronDown size={14} className={`transition-transform ${activeMenu === menu.name ? 'rotate-180' : ''}`} />
              </button>

              {activeMenu === menu.name && (
                <div className="absolute top-14 left-0 w-72 bg-white rounded-2xl shadow-2xl p-3 text-slate-900 border border-slate-100">
                  <div className="absolute -top-1.5 left-6 w-3 h-3 bg-white rotate-45 border-t border-l border-slate-100" />
                  <div className="flex flex-col gap-1 relative z-10">
                    {menu.items.map((item) => (
                      <Link key={item.title} href="#" className="p-3 hover:bg-slate-50 rounded-xl transition-all group">
                        <div className="flex items-center gap-3">
                          <div className="text-med-green group-hover:scale-110 transition-transform">{item.icon}</div>
                          <div>
                            <p className="font-bold text-sm leading-none mb-1">{item.title}</p>
                            <p className="text-[11px] text-slate-500">{item.desc}</p>
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Auth Buttons */}
        <div className="flex items-center gap-4">
          <Link href="/login">
            <button className="bg-white text-med-green px-5 py-2 rounded-xl text-sm font-bold shadow-lg shadow-black/10 hover:bg-slate-50 transition-all flex items-center gap-2">
              Login
            </button>
          </Link>
        </div>
      </div>
    </nav>
  );
}