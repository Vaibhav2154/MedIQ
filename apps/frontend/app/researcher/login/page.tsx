
"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { edaApi } from '@/lib/eda-api';
import { Shield, Loader2, Lock, Mail, ArrowRight, AlertCircle, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function ResearcherLoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const response = await edaApi.login({ email, password });
            localStorage.setItem('token', response.access_token);
            localStorage.setItem('researcher', JSON.stringify(response.researcher));
            router.push('/researcher/eda');
        } catch (err: any) {
            setError(err.response?.data?.detail || "Authentication failed. Please check your credentials.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
            {/* Simple Navbar */}
            <nav className="h-16 bg-white border-b border-slate-200 px-8 flex items-center justify-between sticky top-0 z-40">
                <Link href="/" className="flex items-center gap-2 group cursor-pointer">
                    <Shield className="text-med-green w-6 h-6" />
                    <span className="font-bold text-xl tracking-tight text-slate-900 italic">MedIQ</span>
                </Link>
                <Link href="/researcher" className="text-sm font-bold text-slate-500 hover:text-med-green transition-colors">
                    Back to Portal
                </Link>
            </nav>

            <main className="flex-1 flex items-center justify-center p-6 relative overflow-hidden">
                {/* Decorative Background Elements */}
                <div className="absolute top-1/4 -left-20 w-80 h-80 bg-med-green/5 rounded-full blur-3xl" />
                <div className="absolute bottom-1/4 -right-20 w-80 h-80 bg-med-green/5 rounded-full blur-3xl" />

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="w-full max-w-md relative z-10"
                >
                    <Card className="border-slate-200 shadow-2xl rounded-3xl overflow-hidden bg-white">
                        <div className="h-2 bg-med-green w-full" />
                        <CardHeader className="pt-10 pb-6 text-center">
                            <div className="w-16 h-16 bg-med-green/10 text-med-green rounded-2xl flex items-center justify-center mx-auto mb-6">
                                <Lock className="w-8 h-8" />
                            </div>
                            <CardTitle className="text-3xl font-black text-slate-900 tracking-tight">Researcher Login</CardTitle>
                            <CardDescription className="text-slate-500 mt-2">
                                Access the MedIQ Secure Research Workspace
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="px-8 pb-10">
                            {error && (
                                <motion.div
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    className="mb-6 p-4 bg-red-50 border border-red-100 rounded-2xl flex items-start gap-3 text-red-600 text-sm"
                                >
                                    <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                                    <p>{error}</p>
                                </motion.div>
                            )}

                            <form onSubmit={handleLogin} className="space-y-5">
                                <div className="space-y-2">
                                    <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Email Address</label>
                                    <div className="relative group">
                                        <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 group-focus-within:text-med-green transition-colors" />
                                        <Input
                                            type="email"
                                            placeholder="researcher@institution.edu"
                                            className="pl-12 h-14 bg-slate-50 border-slate-200 rounded-2xl focus:ring-1 focus:ring-med-green outline-none"
                                            value={email}
                                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Password</label>
                                    <div className="relative group">
                                        <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 group-focus-within:text-med-green transition-colors" />
                                        <Input
                                            type="password"
                                            placeholder="••••••••"
                                            className="pl-12 h-14 bg-slate-50 border-slate-200 rounded-2xl focus:ring-1 focus:ring-med-green outline-none"
                                            value={password}
                                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="pt-4">
                                    <Button
                                        type="submit"
                                        disabled={loading}
                                        className="w-full h-14 bg-med-green hover:bg-med-green/90 text-white rounded-2xl text-base font-bold shadow-lg shadow-med-green/20 transition-all flex items-center justify-center gap-2 group"
                                    >
                                        {loading ? (
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                        ) : (
                                            <>
                                                Sign In <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                            </>
                                        )}
                                    </Button>
                                </div>
                            </form>

                            <div className="mt-8 pt-6 border-t border-slate-100 text-center">
                                <p className="text-sm text-slate-500">
                                    Don't have an account?{" "}
                                    <Link href="/researcher/signup" className="text-med-green font-bold hover:underline">
                                        Request Access
                                    </Link>
                                </p>
                            </div>
                        </CardContent>
                    </Card>

                    <div className="mt-8 flex items-center justify-center gap-6 text-[10px] text-slate-400 font-bold uppercase tracking-widest">
                        <div className="flex items-center gap-1.5">
                            <Shield className="w-3.5 h-3.5" /> HIPAA Compliant
                        </div>
                        <div className="flex items-center gap-1.5">
                            <CheckCircle className="w-3.5 h-3.5" /> SOC-2 Certified
                        </div>
                    </div>
                </motion.div>
            </main>
        </div>
    );
}
