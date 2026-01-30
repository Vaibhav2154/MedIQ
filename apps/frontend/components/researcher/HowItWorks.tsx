"use client";
import { UserPlus, Key, Database, CheckCircle } from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      icon: <UserPlus size={28} />,
      title: "Sign Up",
      description: "Create your researcher account with institutional credentials",
      step: "01"
    },
    {
      icon: <Key size={28} />,
      title: "Authenticate",
      description: "Get JWT access token for secure API access",
      step: "02"
    },
    {
      icon: <Database size={28} />,
      title: "Request Data",
      description: "Specify research purpose and required fields",
      step: "03"
    },
    {
      icon: <CheckCircle size={28} />,
      title: "Query Data",
      description: "Access consent-filtered data via REST API or SQL",
      step: "04"
    }
  ];

  return (
    <section className="py-24 px-6 bg-slate-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-serif text-slate-900 mb-4">
            How It Works
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Get started in minutes with our self-service researcher portal
          </p>
        </div>

        <div className="grid md:grid-cols-4 gap-8 relative">
          {/* Connection Lines */}
          <div className="hidden md:block absolute top-16 left-0 right-0 h-0.5 bg-gradient-to-r from-med-green via-green-400 to-med-green opacity-20" />

          {steps.map((step, index) => (
            <div key={index} className="relative">
              {/* Step Card */}
              <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border border-slate-100 relative z-10">
                {/* Step Number */}
                <div className="absolute -top-4 -right-4 w-12 h-12 bg-med-green text-white rounded-full flex items-center justify-center font-bold text-lg shadow-lg">
                  {step.step}
                </div>

                {/* Icon */}
                <div className="w-16 h-16 bg-med-green/10 rounded-2xl flex items-center justify-center mb-6 text-med-green">
                  {step.icon}
                </div>

                {/* Content */}
                <h3 className="text-xl font-bold text-slate-900 mb-3">
                  {step.title}
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="text-center mt-16">
          <a href="#get-started">
            <button className="bg-med-green text-white px-10 py-4 rounded-2xl font-bold hover:bg-med-green/90 transition-all shadow-lg">
              Start Building Now
            </button>
          </a>
        </div>
      </div>
    </section>
  );
}
