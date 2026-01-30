"use client";
import { Microscope, Heart, Brain, Activity, Pill, Stethoscope } from 'lucide-react';

export default function UseCases() {
  const useCases = [
    {
      icon: <Microscope size={32} />,
      title: "Clinical Research",
      description: "Access patient cohorts for clinical trials and observational studies with automatic consent filtering",
      color: "from-blue-500 to-blue-600"
    },
    {
      icon: <Heart size={32} />,
      title: "Epidemiology",
      description: "Study disease patterns and health outcomes across populations while respecting patient privacy",
      color: "from-red-500 to-red-600"
    },
    {
      icon: <Brain size={32} />,
      title: "AI/ML Training",
      description: "Build and train healthcare AI models on consent-aware datasets with field-level access control",
      color: "from-purple-500 to-purple-600"
    },
    {
      icon: <Activity size={32} />,
      title: "Public Health",
      description: "Monitor health trends and conduct surveillance studies with aggregated, de-identified data",
      color: "from-green-500 to-green-600"
    },
    {
      icon: <Pill size={32} />,
      title: "Drug Development",
      description: "Accelerate pharmaceutical research with real-world evidence from electronic health records",
      color: "from-orange-500 to-orange-600"
    },
    {
      icon: <Stethoscope size={32} />,
      title: "Quality Improvement",
      description: "Analyze treatment outcomes and healthcare delivery metrics to improve patient care",
      color: "from-teal-500 to-teal-600"
    }
  ];

  return (
    <section className="py-24 px-6 bg-gradient-to-br from-slate-50 to-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-serif text-slate-900 mb-4">
            Trusted by Researchers Worldwide
          </h2>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            Supporting diverse research needs across healthcare domains
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {useCases.map((useCase, index) => (
            <div
              key={index}
              className="group relative bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all border border-slate-100 overflow-hidden"
            >
              {/* Gradient Background */}
              <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${useCase.color} opacity-10 rounded-full blur-3xl group-hover:opacity-20 transition-all`} />

              {/* Icon */}
              <div className={`relative w-16 h-16 bg-gradient-to-br ${useCase.color} rounded-2xl flex items-center justify-center mb-6 text-white shadow-lg`}>
                {useCase.icon}
              </div>

              {/* Content */}
              <h3 className="text-xl font-bold text-slate-900 mb-3 relative">
                {useCase.title}
              </h3>
              <p className="text-slate-600 leading-relaxed relative">
                {useCase.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
