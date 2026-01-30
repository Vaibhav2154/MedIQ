"use client";
import { useState } from 'react';
import { Code, Terminal, Zap } from 'lucide-react';

export default function APIShowcase() {
  const [activeTab, setActiveTab] = useState<'signup' | 'request' | 'query'>('signup');

  const codeExamples = {
    signup: `// 1. Sign up as a researcher
curl -X POST http://localhost:8005/api/v1/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "researcher@university.edu",
    "password": "SecurePass123",
    "full_name": "Dr. Jane Smith",
    "institution": "MIT Research Lab",
    "research_interests": "Diabetes research"
  }'

// Response: 201 Created
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "researcher": { ... }
}`,
    request: `// 2. Request data access
curl -X POST http://localhost:8005/api/v1/data/request-access \\
  -H "Authorization: Bearer <token>" \\
  -H "Content-Type: application/json" \\
  -d '{
    "purpose": "diabetes_research",
    "justification": "Studying diabetes patterns",
    "requested_fields": ["patient_id", "age", "diagnosis"]
  }'

// Response: 201 Created
{
  "status": "approved",
  "access_token": "data-access-token...",
  "permitted_fields": ["patient_id", "age", "diagnosis"],
  "expires_at": "2026-02-06T12:00:00Z"
}`,
    query: `// 3. Query consent-aware data
curl -X POST http://localhost:8005/api/v1/data/query \\
  -H "Authorization: Bearer <token>" \\
  -H "Content-Type: application/json" \\
  -d '{
    "purpose": "diabetes_research",
    "filters": {"age_min": 18, "age_max": 65},
    "limit": 100
  }'

// Response: 200 OK
{
  "data": [
    {"patient_id": "p123", "age": 45, "diagnosis": "Type 2 Diabetes"},
    {"patient_id": "p456", "age": 52, "diagnosis": "Type 1 Diabetes"}
  ],
  "count": 2,
  "consent_filtered": true
}`
  };

  const tabs = [
    { id: 'signup' as const, label: '1. Sign Up', icon: <Code size={16} /> },
    { id: 'request' as const, label: '2. Request Access', icon: <Terminal size={16} /> },
    { id: 'query' as const, label: '3. Query Data', icon: <Zap size={16} /> }
  ];

  return (
    <section id="api-docs" className="py-24 px-6 bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-white/10 px-4 py-2 rounded-full text-sm font-bold mb-6">
            <Terminal size={16} />
            Developer-Friendly API
          </div>
          <h2 className="text-4xl md:text-5xl font-serif mb-4">
            Get Started in 3 API Calls
          </h2>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto">
            Simple REST API with comprehensive documentation and code examples
          </p>
        </div>

        {/* Tabs */}
        <div className="flex flex-wrap justify-center gap-4 mb-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all ${activeTab === tab.id
                  ? 'bg-med-green text-white shadow-lg'
                  : 'bg-white/10 text-slate-400 hover:bg-white/20'
                }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </div>

        {/* Code Display */}
        <div className="bg-slate-950 rounded-2xl p-8 border border-slate-800 shadow-2xl">
          <div className="flex items-center gap-2 mb-4 pb-4 border-b border-slate-800">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <div className="w-3 h-3 rounded-full bg-green-500" />
            </div>
            <span className="text-slate-500 text-sm ml-4 font-mono">terminal</span>
          </div>
          <pre className="text-sm text-green-400 font-mono overflow-x-auto">
            <code>{codeExamples[activeTab]}</code>
          </pre>
        </div>

        {/* CTA */}
        <div className="text-center mt-12">
          <a href="http://localhost:8005/docs" target="_blank" rel="noopener noreferrer">
            <button className="bg-white text-slate-900 px-10 py-4 rounded-2xl font-bold hover:bg-slate-100 transition-all shadow-lg inline-flex items-center gap-2">
              <Terminal size={20} />
              View Full API Documentation
            </button>
          </a>
        </div>
      </div>
    </section>
  );
}
