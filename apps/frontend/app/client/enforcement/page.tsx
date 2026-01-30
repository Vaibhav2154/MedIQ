import { ShieldCheck, ShieldAlert, Zap } from 'lucide-react';

export default function EnforcementPage() {
  const mockLogs = [
    { id: 1, type: "Clinical", consumer: "Central Lab", action: "ALLOWED", reason: "Direct Treatment Consent" },
    { id: 2, type: "Research", consumer: "PharmaCorp", action: "BLOCKED", reason: "Missing Research Policy" },
  ];

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-med-green/10 rounded-2xl text-med-green"><Zap /></div>
        <div>
          <h1 className="text-2xl font-bold">Enforcement Engine</h1>
          <p className="text-slate-500">Real-time mapping of Consent Policies to Clinical Data</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {mockLogs.map((log) => (
          <div key={log.id} className="bg-white border p-6 rounded-2xl flex items-center justify-between shadow-sm">
             <div className="flex gap-4 items-center">
               {log.action === "ALLOWED" ? <ShieldCheck className="text-emerald-500" /> : <ShieldAlert className="text-rose-500" />}
               <div>
                 <h4 className="font-bold text-slate-900">{log.consumer}</h4>
                 <p className="text-xs text-slate-500 uppercase font-bold tracking-widest">{log.type}</p>
               </div>
             </div>
             <div className="text-right">
               <span className={`px-3 py-1 rounded-full text-[10px] font-black ${log.action === "ALLOWED" ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
                 {log.action}
               </span>
               <p className="mt-2 text-xs font-medium text-slate-400 italic">{log.reason}</p>
             </div>
          </div>
        ))}
      </div>
    </div>
  );
}