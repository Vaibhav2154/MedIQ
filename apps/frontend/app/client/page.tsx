import Link from "next/link";
import { ArrowRight, ShieldCheck, UserCheck, LayoutDashboard } from "lucide-react";


export default function ClientLanding() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center items-center p-6 text-center">
      <div className="bg-white p-10 rounded-3xl shadow-2xl max-w-2xl w-full border border-slate-100">
        <div className="mb-8 flex justify-center">
          <div className="bg-med-green/10 p-4 rounded-full">
            <LayoutDashboard size={48} className="text-med-green" />
          </div>
        </div>

        <h1 className="text-4xl font-serif font-bold text-slate-900 mb-4">
          Client Portal
        </h1>
        <p className="text-lg text-slate-600 mb-8 leading-relaxed">
          Securely manage your health data, view audit logs, and control access permissions through our consent-aware infrastructure.
        </p>

        <div className="grid md:grid-cols-2 gap-4 mb-8">
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 text-left">
            <div className="flex items-center gap-2 mb-2 font-bold text-slate-800">
              <ShieldCheck size={20} className="text-med-green" />
              Secure Access
            </div>
            <p className="text-sm text-slate-500">Enterprise-grade security using FHIR standards.</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 text-left">
            <div className="flex items-center gap-2 mb-2 font-bold text-slate-800">
              <UserCheck size={20} className="text-med-green" />
              Consent Control
            </div>
            <p className="text-sm text-slate-500">Granular control over who accesses your data.</p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/client/login" className="w-full sm:w-auto">
            <button className="w-full bg-med-green text-white px-8 py-3 rounded-xl font-bold hover:bg-green-800 transition-all flex items-center justify-center gap-2">
              Login to Portal <ArrowRight size={18} />
            </button>
          </Link>
          <Link href="/client/signup" className="w-full sm:w-auto">
            <button className="w-full bg-white border border-slate-200 text-slate-700 px-8 py-3 rounded-xl font-bold hover:bg-slate-50 transition-all">
              Create Account
            </button>
          </Link>
        </div>
      </div>

      <p className="mt-8 text-slate-400 text-sm">
        Protected by MedIQ Consent Engine · HIPAA Compliant
      </p>
    </div>
  );
}
