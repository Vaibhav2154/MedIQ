import { Upload, Cpu, ShieldCheck, FileSearch } from 'lucide-react';

export default function Engine() {
  const steps = [
    { icon: <Upload />, text: "Upload consent document" },
    { icon: <FileSearch />, text: "AI extracts permissions & limits" },
    { icon: <Cpu />, text: "Converts into FHIR Consent resource" },
    { icon: <ShieldCheck />, text: "Enforcement engine validates requests" }
  ];

  return (
    <section className="py-24 bg-med-light rounded-[60px] mx-6">
      <div className="max-w-7xl mx-auto px-6 text-center">
        <h2 className="text-4xl font-serif mb-16">The MedTrust Engine</h2>
        <div className="grid md:grid-cols-4 gap-8 relative">
          {/* Connector Line */}
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-med-green/20 -translate-y-8" />
          
          {steps.map((step, i) => (
            <div key={i} className="relative z-10 flex flex-col items-center">
              <div className="w-16 h-16 bg-white text-med-green rounded-2xl shadow-lg flex items-center justify-center mb-6 border border-med-green/10">
                {step.icon}
              </div>
              <p className="font-bold text-slate-800 px-4">{step.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}