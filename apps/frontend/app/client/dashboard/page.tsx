"use client";

import { Database, ShieldCheck, Share2, ArrowRight, ToggleRight, ToggleLeft, AlertTriangle, CheckCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function FlowDashboard() {
  const [policies, setPolicies] = useState({
    research: false,
    commercial: false
  });

  // Load policies from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('consent_policies');
    if (saved) {
      setPolicies(JSON.parse(saved));
    }
  }, []);

  // Save policies to localStorage
  const togglePolicy = (key: 'research' | 'commercial') => {
    const newPolicies = { ...policies, [key]: !policies[key] };
    setPolicies(newPolicies);
    localStorage.setItem('consent_policies', JSON.stringify(newPolicies));
  };

  const isFullyBlocked = !policies.research && !policies.commercial;
  const isPartiallyOpen = policies.research || policies.commercial;
  const isFullyOpen = policies.research && policies.commercial;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-12">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-black text-slate-900 uppercase tracking-tighter">Enforcement Flow Monitor</h1>
        <p className="text-slate-500 font-medium italic">Visualizing the path from Client Database to Authorized Access</p>
      </div>

      {/* This grid mirrors your hand-drawn diagram boxes */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">

        {/* Box 1: Client Database */}
        <div className="bg-white border-2 border-slate-200 p-6 rounded-3xl shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-blue-600 font-bold uppercase text-xs">
            <Database size={16} /> Data Stored
          </div>
          <div className="space-y-2">
            <div className="h-12 bg-slate-50 rounded-xl border border-dashed border-slate-200 flex items-center px-4 text-xs font-mono text-slate-400">Health Records (Encounters)</div>
            <div className="h-12 bg-slate-50 rounded-xl border border-dashed border-slate-200 flex items-center px-4 text-xs font-mono text-slate-400">Doctor Records (Diagnoses)</div>
          </div>
          <p className="text-[10px] text-slate-400 text-center font-bold">Encrypted at Rest</p>
        </div>

        {/* Transition Arrow */}
        <div className={`hidden md:flex justify-center transition-colors duration-500 ${isFullyBlocked ? 'text-red-200' : 'text-slate-300'}`}>
          <ArrowRight size={48} strokeWidth={1} />
        </div>

        {/* Box 2: Consent Enforcement (The Logic) */}
        <div className={`bg-med-green text-white p-8 rounded-3xl shadow-xl space-y-6 relative overflow-hidden transition-all duration-500 ${isFullyBlocked ? 'bg-slate-900' : 'bg-med-green'}`}>
          <div className="relative z-10">
            <div className="flex items-center gap-2 font-bold uppercase text-xs opacity-80 mb-4">
              <ShieldCheck size={16} /> Consent & Enforcement
            </div>

            <div className="space-y-4">
              <div
                className="flex items-center justify-between p-3 bg-white/10 rounded-xl cursor-pointer hover:bg-white/20 transition-all"
                onClick={() => togglePolicy('research')}
              >
                <span className="text-sm font-bold">Research Access</span>
                {policies.research ? <ToggleRight className="text-emerald-300 w-6 h-6" /> : <ToggleLeft className="text-slate-400 w-6 h-6" />}
              </div>
              <div
                className="flex items-center justify-between p-3 bg-white/10 rounded-xl cursor-pointer hover:bg-white/20 transition-all"
                onClick={() => togglePolicy('commercial')}
              >
                <span className="text-sm font-bold">Commercial Access</span>
                {policies.commercial ? <ToggleRight className="text-emerald-300 w-6 h-6" /> : <ToggleLeft className="text-slate-400 w-6 h-6" />}
              </div>
            </div>

            <div className="mt-6 bg-black/20 backdrop-blur-sm p-3 rounded-xl border border-white/10 text-[10px] font-mono leading-relaxed">
              <span className="opacity-50">POLICY_STATE:</span> <br />
              RESEARCH: {policies.research ? <span className="text-emerald-300">GRANTED</span> : <span className="text-red-300">REVOKED</span>}<br />
              COMMERCIAL: {policies.commercial ? <span className="text-emerald-300">GRANTED</span> : <span className="text-red-300">REVOKED</span>}
            </div>
          </div>
          <ShieldCheck className="absolute -right-4 -bottom-4 opacity-10" size={120} />
        </div>

        {/* Transition Arrow */}
        <div className={`hidden md:flex justify-center transition-colors duration-500 ${isFullyBlocked ? 'text-red-200' : isFullyOpen ? 'text-emerald-500' : 'text-yellow-400'}`}>
          <ArrowRight size={48} strokeWidth={1} />
        </div>

        {/* Box 3: Authorized Output (Researcher/Analyst) */}
        <div className={`bg-white border-2 p-6 rounded-3xl shadow-sm space-y-4 transition-colors duration-500 ${isFullyBlocked ? 'border-dashed border-red-200 bg-red-50/50' : 'border-med-green/30'}`}>
          <div className={`flex items-center gap-2 font-bold uppercase text-xs ${isFullyBlocked ? 'text-red-500' : 'text-med-green'}`}>
            <Share2 size={16} /> Analysis Ready
          </div>

          {isFullyBlocked ? (
            <div className="flex flex-col items-center justify-center py-4 text-center">
              <AlertTriangle className="text-red-400 mb-2" />
              <p className="text-xs text-red-600 font-bold">Data Access Blocked</p>
              <p className="text-[10px] text-red-400 mt-1">No consent policies active</p>
            </div>
          ) : (
            <>
              <p className="text-xs text-slate-600 leading-relaxed">
                Authorized data packages ready for secure consumption by the Researcher Portal.
              </p>
              <div className="flex gap-1">
                <div className="w-full h-2 bg-med-green rounded-full opacity-20" />
                <div className="w-full h-2 bg-med-green rounded-full opacity-40" />
                <div className="w-full h-2 bg-med-green rounded-full opacity-100" />
              </div>
            </>
          )}
        </div>

      </div>
    </div>
  );
}