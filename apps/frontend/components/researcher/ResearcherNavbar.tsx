"use client";
import { Shield } from 'lucide-react';
import Link from 'next/link';

export default function ResearcherNavbar() {
  return (
    <nav className="sticky top-0 z-[100] bg-med-green text-white border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-serif text-xl font-bold tracking-tight">
          <Shield size={24} className="text-white" />
          <span>MedIQ</span>
          <span className="text-sm font-normal opacity-70 ml-2">/ Researcher Portal</span>
        </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-sm font-semibold opacity-90 hover:opacity-100 transition-all">
            Features
          </a>
          <a href="#api-docs" className="text-sm font-semibold opacity-90 hover:opacity-100 transition-all">
            API Docs
          </a>
          <a href="#get-started" className="text-sm font-semibold opacity-90 hover:opacity-100 transition-all">
            Get Started
          </a>
        </div>

        {/* Auth Buttons */}
        <div className="flex items-center gap-4">
          <Link href="/researcher/login">
            <button className="text-white text-sm font-bold hover:opacity-80 transition-all">
              Log In
            </button>
          </Link>
          <Link href="/researcher/signup">
            <button className="bg-white text-med-green px-5 py-2 rounded-xl text-sm font-bold shadow-lg shadow-black/10 hover:bg-slate-50 transition-all">
              Sign Up Free
            </button>
          </Link>
        </div>
      </div>
    </nav>
  );
}
