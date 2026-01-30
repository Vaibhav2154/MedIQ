import { Database, ShieldCheck, Share2, ArrowRight } from 'lucide-react';

export default function FlowDashboard() {
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
          <p className="text-[10px] text-slate-400 text-center font-bold"></p>
        </div>

        {/* Transition Arrow */}
        <div className="hidden md:flex justify-center text-slate-300">
          <ArrowRight size={48} strokeWidth={1} />
        </div>

        {/* Box 2: Consent Enforcement (The Logic) */}
        <div className="bg-med-green text-white p-8 rounded-3xl shadow-xl space-y-4 relative overflow-hidden">
          <div className="relative z-10">
            <div className="flex items-center gap-2 font-bold uppercase text-xs opacity-80 mb-4">
              <ShieldCheck size={16} /> Consent & Enforcement
            </div>
            <h3 className="text-lg font-bold italic leading-tight mb-2">Policy to Data Mapping</h3>
            <div className="bg-white/10 backdrop-blur-sm p-3 rounded-xl border border-white/20 text-[10px] font-mono leading-relaxed">
              IF purpose == 'research' AND consent == 'active' <br/>
              THEN allow access(diagnosis_data)
            </div>
          </div>
          <ShieldCheck className="absolute -right-4 -bottom-4 opacity-10" size={120} />
        </div>

        {/* Transition Arrow */}
        <div className="hidden md:flex justify-center text-slate-300">
          <ArrowRight size={48} strokeWidth={1} />
        </div>

        {/* Box 3: Authorized Output (Researcher/Analyst) */}
        <div className="bg-white border-2 border-med-green/30 p-6 rounded-3xl shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-med-green font-bold uppercase text-xs">
            <Share2 size={16} /> Analysis Ready
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Authorized data packages ready for secure consumption by the Researcher Portal.
          </p>
          <div className="flex gap-1">
             <div className="w-full h-2 bg-med-green rounded-full opacity-20" />
             <div className="w-full h-2 bg-med-green rounded-full opacity-40" />
             <div className="w-full h-2 bg-med-green rounded-full opacity-100" />
          </div>
        </div>

      </div>
    </div>
  );
}