import Link from "next/link";
import { User, Building2, ShieldCheck } from "lucide-react";

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 py-12 px-4">
      <div className="max-w-xl w-full space-y-8 bg-white p-10 rounded-2xl shadow-xl border border-slate-100">
        <div className="text-center">
          <h2 className="text-3xl font-serif font-bold text-slate-900">Create Account</h2>
          <p className="mt-2 text-sm text-slate-500">Join the secure medical data network</p>
        </div>


        <form className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-700">First Name</label>
              <input type="text" className="w-full mt-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-med-green" />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700">Last Name</label>
              <input type="text" className="w-full mt-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-med-green" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700">Organization Email</label>
            <input type="email" className="w-full mt-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-med-green" />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700">Password</label>
            <input type="password" placeholder="Min 8 characters" className="w-full mt-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-med-green" />
          </div>

          <div className="flex items-start gap-2 py-2">
            <input type="checkbox" className="mt-1 accent-med-green" id="terms" />
            <label htmlFor="terms" className="text-xs text-slate-500 leading-relaxed">
              I agree to the MedTrust Data Processing Agreement and HIPAA Compliance standards.
            </label>
          </div>

          <button className="w-full py-4 bg-med-green text-white rounded-xl font-bold hover:bg-opacity-90 transition-all flex items-center justify-center gap-2">
            <ShieldCheck size={20} /> Sign Up
          </button>
        </form>

        <p className="text-center text-sm text-slate-500 pt-4">
          Already have an account?{" "}
          <Link href="/login" className="font-bold text-med-green hover:underline">Sign In</Link>
        </p>
      </div>
    </div>
  );
}