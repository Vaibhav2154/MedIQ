export default function Pipeline() {
  return (
    <section className="py-24 bg-slate-900 text-white overflow-hidden">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-16">
          <h2 className="text-4xl font-serif mb-4">The Consent Lifecycle</h2>
          <p className="text-slate-400">From raw document to machine-enforceable policy.</p>
        </div>
        
        <div className="flex flex-col md:flex-row items-center gap-4">
          <PipelineStep step="01" label="Ingestion" desc="PDF/Voice/Digital" />
          <div className="h-0.5 w-12 bg-med-green hidden md:block" />
          <PipelineStep step="02" label="AI Mapping" desc="Permission Extraction" />
          <div className="h-0.5 w-12 bg-med-green hidden md:block" />
          <PipelineStep step="03" label="Validation" desc="FHIR Compliance" />
          <div className="h-0.5 w-12 bg-med-green hidden md:block" />
          <PipelineStep active step="04" label="Enforcement" desc="Live Data Request" />
        </div>
      </div>
    </section>
  );
}

function PipelineStep({ step, label, desc, active = false }: any) {
  return (
    <div className={`flex-1 p-8 rounded-3xl border ${active ? 'border-med-green bg-med-green/10' : 'border-white/10'}`}>
      <span className="text-xs font-mono text-med-green mb-4 block">{step}</span>
      <h4 className="text-xl font-bold mb-2">{label}</h4>
      <p className="text-sm text-slate-400">{desc}</p>
    </div>
  );
}