"use client";
import { ArrowRight, Database, Shield, Zap } from 'lucide-react';
import Link from 'next/link';

export default function ResearcherHero() {
  return (
    <section className="bg-med-green text-white pt-24 pb-32 px-6 rounded-b-[40px] relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute top-20 left-10 w-64 h-64 bg-white rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-white rounded-full blur-3xl" />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left Column - Content */}
          <div>
            <div className="inline-flex items-center gap-2 bg-white/10 px-4 py-2 rounded-full text-sm font-bold mb-6 border border-white/20">
              <Shield size={16} className="text-green-300" />
              Consent-Aware Research Platform
            </div>

            <h1 className="text-5xl md:text-6xl font-serif leading-tight mb-6">
              Access Healthcare Data
              <br />
              <span className="text-green-200">The Right Way</span>
            </h1>

            <p className="text-xl opacity-90 mb-8 leading-relaxed">
              Self-service portal for researchers to access consent-aware patient data
              for research purposes. Built on FHIR standards with automatic consent enforcement.
            </p>

            <div className="flex flex-wrap gap-4 mb-12">
              <Link href="#get-started">
                <button className="bg-white text-med-green px-8 py-4 rounded-2xl font-bold flex items-center gap-2 shadow-xl hover:scale-105 transition-all">
                  Get Started <ArrowRight size={20} />
                </button>
              </Link>
              <Link href="#api-docs">
                <button className="bg-transparent border-2 border-white/30 text-white px-8 py-4 rounded-2xl font-bold hover:bg-white/10 transition-all">
                  View API Docs
                </button>
              </Link>
            </div>

            {/* Trust Badges */}
            <div className="flex flex-wrap gap-6 items-center opacity-80">
              <div className="flex items-center gap-2 text-sm">
                <Shield size={16} />
                <span>ABDM Compliant</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <Database size={16} />
                <span>FHIR v4.0.1</span>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <Zap size={16} />
                <span>Real-time Consent</span>
              </div>
            </div>
          </div>

          {/* Right Column - Feature Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20 hover:bg-white/15 transition-all">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4">
                <Shield className="text-white" size={24} />
              </div>
              <h3 className="font-bold text-lg mb-2">Consent-First</h3>
              <p className="text-sm opacity-80">Automatic policy enforcement at field level</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20 hover:bg-white/15 transition-all mt-8">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4">
                <Zap className="text-white" size={24} />
              </div>
              <h3 className="font-bold text-lg mb-2">SQL Rewriting</h3>
              <p className="text-sm opacity-80">Queries auto-filtered for compliance</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20 hover:bg-white/15 transition-all">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4">
                <Database className="text-white" size={24} />
              </div>
              <h3 className="font-bold text-lg mb-2">REST API</h3>
              <p className="text-sm opacity-80">Simple JSON-based data access</p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm p-6 rounded-2xl border border-white/20 hover:bg-white/15 transition-all mt-8">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4">
                <ArrowRight className="text-white" size={24} />
              </div>
              <h3 className="font-bold text-lg mb-2">Audit Trail</h3>
              <p className="text-sm opacity-80">Complete access transparency</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
