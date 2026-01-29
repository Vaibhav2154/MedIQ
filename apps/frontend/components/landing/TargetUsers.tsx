import { Building2, Microscope, Globe, Activity } from 'lucide-react';

export default function TargetUsers() {
  const users = [
    { name: "Hospitals", icon: <Building2 />, desc: "Automate patient consent for surgical and diagnostic data sharing." },
    { name: "Research Orgs", icon: <Microscope />, desc: "Safely access de-identified health data with verifiable digital audits." },
    { name: "Health-Tech Platforms", icon: <Globe />, desc: "Integrate consent-as-a-service into your existing health apps." },
    { name: "Clinical Trials", icon: <Activity />, desc: "Enforce time-bound data access for specific trial parameters." }
  ];

  return (
    <section className="py-24 max-w-7xl mx-auto px-6">
      <h2 className="text-3xl font-serif text-center mb-16 text-slate-900">
        Built for the architects of modern healthcare.
      </h2>
      <div className="grid md:grid-cols-4 gap-8">
        {users.map((user) => (
          <div key={user.name} className="p-8 bg-white border border-slate-100 rounded-[32px] hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-med-light text-med-green rounded-2xl flex items-center justify-center mb-6">
              {user.icon}
            </div>
            <h4 className="text-xl font-bold mb-3">{user.name}</h4>
            <p className="text-slate-500 text-sm leading-relaxed">{user.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}