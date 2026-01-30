import { Search, Filter, Shield } from 'lucide-react';

export default function HealthRecordsPage() {
  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <header className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-900">Patient Health Records</h1>
        <button className="bg-med-green text-white px-4 py-2 rounded-lg font-bold text-sm">Add Record</button>
      </header>

      {/* Search Bar - Diagram: "Patient Search" */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input className="w-full pl-10 pr-4 py-3 bg-white border rounded-xl outline-none focus:ring-2 ring-med-green/20" placeholder="Search Patient UHID or Name..." />
        </div>
        <button className="px-4 py-3 bg-white border rounded-xl text-slate-600"><Filter size={20} /></button>
      </div>

      {/* Records Table - Diagram: "Medical Records" */}
      <div className="bg-white border rounded-2xl shadow-sm overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead className="bg-slate-50 text-slate-500 text-xs font-bold uppercase tracking-wider">
            <tr>
              <th className="px-6 py-4">Patient UHID</th>
              <th className="px-6 py-4">Clinical Data Type</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Consent Status</th>
              <th className="px-6 py-4">Date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {[1, 2, 3].map((i) => (
              <tr key={i} className="hover:bg-slate-50 transition-colors cursor-pointer">
                <td className="px-6 py-4 font-bold text-slate-900">UHID-99230{i}</td>
                <td className="px-6 py-4 text-sm text-slate-600">Observation: Blood Glucose</td>
                <td className="px-6 py-4 text-sm font-medium">Completed</td>
                <td className="px-6 py-4">
                   <span className="flex items-center gap-1.5 text-med-green text-xs font-bold">
                     <Shield size={14}/> Protected
                   </span>
                </td>
                <td className="px-6 py-4 text-sm text-slate-500">Jan 30, 2026</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}