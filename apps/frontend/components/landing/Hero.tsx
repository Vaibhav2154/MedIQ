import { ArrowRight, PlayCircle } from 'lucide-react';

export default function Hero() {
  return (
    <section className="h-125 bg-med-green text-white pt-16 pb-20 px-6 rounded-b-[40px]">
      <div className="max-w-6xl mx-auto text-center">
        <div className="inline-flex items-center gap-2 bg-white/10 px-4 py-2 rounded-full text-sm font-bold mb-8 border border-white/20">
          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          FHIR & ABDM Aligned Infrastructure
        </div>
        <h1 className="text-5xl md:text-3xl font-serif leading-tight mb-8">
          Consent-aware infrastructure for <br /> safe healthcare data sharing.
        </h1>
        <p className="text-xl opacity-90 mb-12 max-w-3xl mx-auto font-light leading-relaxed">
          AI-powered system to convert human consent into enforceable digital policies 
          for hospitals, research orgs, and health platforms.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <button className="bg-white text-med-green px-8 py-4 rounded-2xl font-bold flex items-center gap-2 shadow-xl hover:scale-105 transition-all">
            View Consent Engine Demo <PlayCircle size={20} />
          </button>
          <button className="bg-transparent border border-white/30 text-white px-8 py-4 rounded-2xl font-bold hover:bg-white/10 transition-all">
            For Hospitals & Researchers
          </button>
        </div>
      </div>
    </section>
  );
}