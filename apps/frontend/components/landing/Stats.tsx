export default function Stats() {
  const stats = [
    { label: "ABDM Compliant Facilities", value: "2k+" },
    { label: "Patient ABHAs Created", value: "1.4 Cr" },
    { label: "EHR Linked with ABHA", value: "1.5 Cr" },
    { label: "Doctors Onboarded", value: "44k" },
  ];

  return (
    <section className="bg-med-green py-20 px-6">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-white text-center text-3xl font-serif mb-16 opacity-90">
          Transforming Healthcare Access Across India
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat) => (
            <div key={stat.label} className="text-center border-l border-white/20 first:border-l-0">
              <div className="text-white text-4xl md:text-5xl font-bold mb-2">{stat.value}</div>
              <div className="text-white/70 text-sm font-medium uppercase tracking-wider px-4">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}