"use client";
import { ArrowRight, BookOpen, Code, MessageCircle } from 'lucide-react';
import Link from 'next/link';

export default function GetStarted() {
  return (
    <section id="get-started" className="py-24 px-6 bg-med-green text-white relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-0 left-0 w-full h-full"
          style={{
            backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
            backgroundSize: '40px 40px'
          }}
        />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-serif mb-4">
            Ready to Start Researching?
          </h2>
          <p className="text-xl opacity-90 max-w-2xl mx-auto">
            Join researchers worldwide using MedIQ for consent-aware healthcare data access
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {/* Card 1 */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all">
            <div className="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center mb-6">
              <Code className="text-white" size={28} />
            </div>
            <h3 className="text-2xl font-bold mb-3">Create Account</h3>
            <p className="opacity-90 mb-6 leading-relaxed">
              Sign up with your institutional email and get instant API access
            </p>
            <Link href="/researcher/signup">
              <button className="bg-white text-med-green px-6 py-3 rounded-xl font-bold hover:bg-slate-100 transition-all inline-flex items-center gap-2">
                Sign Up Free <ArrowRight size={18} />
              </button>
            </Link>
          </div>

          {/* Card 2 */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all">
            <div className="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center mb-6">
              <BookOpen className="text-white" size={28} />
            </div>
            <h3 className="text-2xl font-bold mb-3">Read Docs</h3>
            <p className="opacity-90 mb-6 leading-relaxed">
              Comprehensive guides, API reference, and code examples
            </p>
            <a href="http://localhost:8005/docs" target="_blank" rel="noopener noreferrer">
              <button className="bg-transparent border-2 border-white/30 text-white px-6 py-3 rounded-xl font-bold hover:bg-white/10 transition-all inline-flex items-center gap-2">
                View Documentation <ArrowRight size={18} />
              </button>
            </a>
          </div>

          {/* Card 3 */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all">
            <div className="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center mb-6">
              <MessageCircle className="text-white" size={28} />
            </div>
            <h3 className="text-2xl font-bold mb-3">Get Support</h3>
            <p className="opacity-90 mb-6 leading-relaxed">
              Need help? Our team is here to assist with integration
            </p>
            <a href="mailto:support@mediq.health">
              <button className="bg-transparent border-2 border-white/30 text-white px-6 py-3 rounded-xl font-bold hover:bg-white/10 transition-all inline-flex items-center gap-2">
                Contact Us <ArrowRight size={18} />
              </button>
            </a>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 pt-12 border-t border-white/20">
          <div className="text-center">
            <div className="text-4xl font-bold mb-2">15min</div>
            <div className="text-sm opacity-80">Average Setup Time</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold mb-2">99.9%</div>
            <div className="text-sm opacity-80">API Uptime</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold mb-2">100%</div>
            <div className="text-sm opacity-80">FHIR Compliant</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold mb-2">24/7</div>
            <div className="text-sm opacity-80">Support Available</div>
          </div>
        </div>
      </div>
    </section>
  );
}
