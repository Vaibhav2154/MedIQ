export default function Problem() {
  const pains = [
    { title: "Static Consents", desc: "Consents are PDFs, not machine-enforceable digital policies." },
    { title: "Compliance Gaps", desc: "Researchers struggle to know what they are legally allowed to access." },
    { title: "Audit Void", desc: "Hospitals cannot audit or automate compliance in real-time." },
    { title: "Loss of Control", desc: "Patients lose visibility and control once data leaves the primary facility." }
  ];

  return (
    <section className="py-24 max-w-7xl mx-auto px-6">
      <div className="grid lg:grid-cols-2 gap-16 items-center">
        <div>
          <h2 className="text-4xl font-serif mb-6 text-slate-900">Healthcare data sharing <br /> is broken.</h2>
          <p className="text-slate-500 text-lg mb-8 italic">"We don't replace health apps. We make them safer."</p>
        </div>
        <div className="grid sm:grid-cols-2 gap-6">
          {pains.map((pain) => (
            <div key={pain.title} className="p-6 bg-slate-50 rounded-2xl border border-slate-100">
              <div className="w-10 h-10 bg-red-100 text-red-600 rounded-lg flex items-center justify-center mb-4 font-bold">!</div>
              <h4 className="font-bold text-slate-900 mb-2">{pain.title}</h4>
              <p className="text-sm text-slate-600 leading-relaxed">{pain.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}