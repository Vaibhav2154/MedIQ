import Link from "next/link";
import { Shield, ArrowRight } from "lucide-react";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl shadow-xl border border-slate-100">
        <div className="text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-med-green/10 rounded-xl text-med-green">
              <Shield size={32} />
            </div>
          </div>
          <h2 className="text-3xl font-serif font-bold text-slate-900">Welcome Back</h2>
          <p className="mt-2 text-sm text-slate-500">Access your MedTrust dashboard</p>
        </div>

        <form className="mt-8 space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-slate-700">Email Address</label>
              <input
                type="email"
                required
                className="w-full mt-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-med-green focus:border-transparent outline-none transition-all"
                placeholder="doctor@hospital.com"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700">Password</label>
              <input
                type="password"
                required
                className="w-full mt-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-med-green focus:border-transparent outline-none transition-all"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button className="w-full py-4 bg-med-green text-white rounded-xl font-bold flex items-center justify-center gap-2 hover:bg-opacity-90 transition-all shadow-lg shadow-med-green/20">
            Sign In <ArrowRight size={18} />
          </button>
        </form>

        <p className="text-center text-sm text-slate-500">
          Don't have an account?{" "}
          <Link href="/client/signup" className="font-bold text-med-green hover:underline">
            Create an account
          </Link>
        </p>
      </div>
    </div>
  );
}