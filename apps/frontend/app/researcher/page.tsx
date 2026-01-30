import ResearcherNavbar from "@/components/researcher/ResearcherNavbar";
import ResearcherHero from "@/components/researcher/ResearcherHero";
import HowItWorks from "@/components/researcher/HowItWorks";
import Features from "@/components/researcher/Features";
import APIShowcase from "@/components/researcher/APIShowcase";
import UseCases from "@/components/researcher/UseCases";
import GetStarted from "@/components/researcher/GetStarted";

export default function ResearcherPage() {
  return (
    <main className="min-h-screen bg-slate-50">
      <ResearcherNavbar />
      <ResearcherHero />
      <HowItWorks />
      <Features />
      <APIShowcase />
      <UseCases />
      <GetStarted />

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-12 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-slate-400 text-sm">
            © 2026 MedIQ. Built for researchers, powered by consent.
          </p>
          <div className="flex justify-center gap-6 mt-4 text-sm">
            <a href="#" className="text-slate-400 hover:text-white transition-all">Privacy Policy</a>
            <a href="#" className="text-slate-400 hover:text-white transition-all">Terms of Service</a>
            <a href="http://localhost:8005/docs" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition-all">
              API Documentation
            </a>
          </div>
        </div>
      </footer>
    </main>
  );
}
