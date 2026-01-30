"use client";
import { Shield, Zap, Lock, Terminal, FileCode, BarChart3, Clock, Globe } from 'lucide-react';

export default function Features() {
  const features = [
    {
      icon: <Shield size={24} />,
      title: "Consent-Aware Access",
      description: "Automatic enforcement of patient consent policies at field level. Only access data patients have explicitly permitted for your research purpose."
    },
    {
      icon: <Terminal size={24} />,
      title: "SQL Query Rewriting",
      description: "Submit raw SQL queries that are automatically rewritten to remove denied fields. Powered by SQLGlot for precise query manipulation."
    },
    {
      icon: <Zap size={24} />,
      title: "REST API",
      description: "Simple JSON-based API for most use cases. No SQL required - just specify your purpose and desired fields."
    },
    {
      icon: <Lock size={24} />,
      title: "JWT Authentication",
      description: "Secure token-based authentication with time-limited access tokens scoped to specific research purposes."
    },
    {
      icon: <FileCode size={24} />,
      title: "FHIR Compliant",
      description: "Built on FHIR v4.0.1 standards for healthcare interoperability. Seamlessly integrate with existing FHIR systems."
    },
    {
      icon: <BarChart3 size={24} />,
      title: "Audit Logging",
      description: "Complete transparency with detailed audit trails for all data access attempts and policy evaluations."
    },
    {
      icon: <Clock size={24} />,
      title: "Real-Time Policies",
      description: "Consent policies are evaluated in real-time. Changes to patient consent are immediately reflected in access permissions."
    },
    {
      icon: <Globe size={24} />,
      title: "ABDM Aligned",
      description: "Fully aligned with India's Ayushman Bharat Digital Mission (ABDM) standards for health data exchange."
    }
  ];

  return (
    <section className="py-24 px-6 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-med-green/10 px-4 py-2 rounded-full text-sm font-bold mb-6 text-med-green">
            <Zap size={16} />
            Platform Features
          </div>
          <h2 className="text-4xl md:text-5xl font-serif text-slate-900 mb-4">
            Built for Modern Research
          </h2>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            Everything you need to access healthcare data compliantly and efficiently
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group p-6 rounded-2xl border-2 border-slate-100 hover:border-med-green/30 hover:shadow-lg transition-all bg-white"
            >
              <div className="w-14 h-14 bg-med-green/10 rounded-xl flex items-center justify-center mb-4 text-med-green group-hover:bg-med-green group-hover:text-white transition-all">
                {feature.icon}
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-slate-600 text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
