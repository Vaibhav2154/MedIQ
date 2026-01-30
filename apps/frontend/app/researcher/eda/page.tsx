
"use client";

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    ScatterChart, Scatter, LineChart, Line, AreaChart, Area
} from 'recharts';
import { useEda, EdaViewType } from '@/hooks/use-eda';
import {
    Loader2, Activity, PieChart, TrendingUp, Grid,
    Binary, Search, AlertCircle, Calendar, FileText,
    Layers, Zap, Database, Settings2, Share2, ChevronRight,
    FlaskConical, Plus, LogOut, Info, Shield, CheckCircle,
    Lock as LockIcon
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';

// Mock Config for Demo (In real app, columns would be fetched from dataset metadata)
// Note: The actual health tables (patients, observations, medications) don't have numeric columns
// suitable for statistical analysis. In a real scenario, you would add numeric fields like age, 
// blood pressure, glucose levels, etc. For now, using empty arrays to prevent errors.
const DATASETS = [
    {
        id: "sample-health-metrics",
        name: "Sample Health Metrics",
        columns: ["patient_age", "systolic_bp", "diastolic_bp", "heart_rate", "glucose_level", "cholesterol", "bmi", "temperature"]
    },
    { id: "patients-dataset", name: "Patient Demographics", columns: [] },
    { id: "observations-dataset", name: "Clinical Observations", columns: [] },
    { id: "medications-dataset", name: "Medication Records", columns: [] }
];

const FEATURES = [
    { id: "summary", label: "Summary Stats", icon: Activity, description: "Descriptive statistics for numeric fields" },
    { id: "unique", label: "Unique Values", icon: Binary, description: "Cardonality and top value distribution" },
    { id: "missing", label: "Missing Data", icon: Search, description: "Null value and sparsity analysis" },
    { id: "histogram", label: "Distribution", icon: PieChart, description: "Frequency analysis and density" },
    { id: "correlation", label: "Correlations", icon: Grid, description: "Relationship matrix between features" },
    { id: "scatter", label: "Scatter Plot", icon: Layers, description: "Bivariate relationship visualization" },
    { id: "trend", label: "Time Trends", icon: TrendingUp, description: "Temporal variance analysis" },
    { id: "outliers", label: "Outliers", icon: AlertCircle, description: "Anomalous data point detection" },
    { id: "groupby", label: "Group Analysis", icon: Database, description: "Aggregated cohort analysis" },
];

export default function EdaDashboard() {
    const router = useRouter();
    const {
        loading, error, viewType, data, actions, reset,
        sessions, activeSession, setActiveSession, fetchSessions, createSession
    } = useEda();

    const [selectedDataset, setSelectedDataset] = useState(DATASETS[0]);
    const [selectedColumn, setSelectedColumn] = useState(DATASETS[0]?.columns?.[0] || "");
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

    // Auth Guard
    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/researcher/login');
        }
    }, [router]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('researcher');
        router.push('/researcher/login');
    };

    // New Session Form State
    const [newSession, setNewSession] = useState({ title: "", purpose: "", requested_fields: ["age", "bp"] });

    useEffect(() => {
        fetchSessions();
    }, [fetchSessions]);

    const handleFeatureClick = (id: string) => {
        if (!activeSession || !selectedDataset?.id) return;

        switch (id) {
            case 'summary': actions.fetchSummary(selectedDataset.id, selectedDataset.columns); break;
            case 'unique': actions.fetchUnique(selectedDataset.id, selectedColumn); break;
            case 'missing': actions.fetchMissing(selectedDataset.id, selectedDataset.columns); break;
            case 'histogram': actions.fetchHistogram(selectedDataset.id, selectedColumn, 10); break;
            case 'correlation': actions.fetchCorrelation(selectedDataset.id, selectedDataset.columns); break;
            case 'scatter': actions.fetchScatter(selectedDataset.id, selectedDataset.columns[0] || "", selectedDataset.columns[1] || selectedDataset.columns[0] || ""); break;
            case 'trend': actions.fetchTrend(selectedDataset.id, selectedColumn); break;
            case 'outliers': actions.fetchOutliers(selectedDataset.id, selectedColumn); break;
            case 'groupby': actions.fetchGroupBy(selectedDataset.id, "gender", "age"); break;
            case 'boxplot': actions.fetchBoxplot(selectedDataset.id, selectedColumn); break;
            case 'percentiles': actions.fetchPercentiles(selectedDataset.id, selectedColumn); break;
            case 'report': actions.fetchReport(selectedDataset.id, ["summary", "missing"]); break;
        }
    };

    const handleCreateSession = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await createSession(newSession);
            setIsCreateModalOpen(false);
            setNewSession({ title: "", purpose: "", requested_fields: ["age", "bp"] });
        } catch (err) {
            // Error handled by hook
        }
    };

    const renderContent = () => {
        if (!activeSession) {
            return (
                <div className="flex flex-col items-center justify-center h-full text-center p-8 bg-white rounded-2xl border-2 border-dashed border-slate-200">
                    <div className="w-16 h-16 bg-med-green/10 text-med-green rounded-full flex items-center justify-center mb-4">
                        <LockIcon className="w-8 h-8" />
                    </div>
                    <h2 className="text-2xl font-bold text-slate-900 mb-2">No Active Session</h2>
                    <p className="text-slate-500 max-w-md mb-6">
                        In accordance with MedIQ security protocols, all research activities must be performed within a verified session context for auditing.
                    </p>
                    <Button onClick={() => setIsCreateModalOpen(true)} className="bg-med-green hover:bg-med-green/90 text-white rounded-xl px-8">
                        <Plus className="w-4 h-4 mr-2" /> Start New Session
                    </Button>
                </div>
            );
        }

        if (!data) return (
            <div className="flex flex-col items-center justify-center h-full text-center p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-5xl">
                    {FEATURES.map((feature) => (
                        <Card
                            key={feature.id}
                            className="group cursor-pointer hover:border-med-green hover:shadow-lg transition-all border-slate-200 shadow-sm"
                            onClick={() => handleFeatureClick(feature.id)}
                        >
                            <CardContent className="p-6">
                                <div className="flex items-center gap-4 mb-4">
                                    <div className="p-3 bg-slate-100 text-slate-600 group-hover:bg-med-green/10 group-hover:text-med-green rounded-xl transition-colors">
                                        <feature.icon className="w-6 h-6" />
                                    </div>
                                    <h3 className="font-bold text-slate-900 uppercase tracking-wide text-sm">{feature.label}</h3>
                                </div>
                                <p className="text-xs text-slate-500 leading-relaxed leading-relaxed">{feature.description}</p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        );

        // Analysis Result View (Styled professionally)
        return (
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden h-full flex flex-col">
                <div className="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-med-green/10 text-med-green rounded-lg">
                            <Activity className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className="font-bold text-slate-900 leading-none">Analysis Output</h3>
                            <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">Module: {viewType}</p>
                        </div>
                    </div>
                    <Button variant="ghost" size="sm" onClick={() => reset()} className="text-slate-500 hover:text-med-green">
                        Reset Workspace
                    </Button>
                </div>
                <div className="flex-1 p-6 overflow-auto">
                    {viewType === 'histogram' && (
                        <div className="h-full">
                            <ResponsiveContainer width="100%" height={400}>
                                <BarChart data={data.bins}>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                    <XAxis dataKey="range" stroke="#64748b" fontSize={12} />
                                    <YAxis stroke="#64748b" fontSize={12} />
                                    <Tooltip
                                        contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                                    />
                                    <Bar dataKey="count" fill="#1a6b4f" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    )}

                    {viewType === 'summary' && (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {data.map((stat: any) => (
                                <div key={stat.column} className="p-4 rounded-xl border border-slate-200 bg-slate-50 group hover:border-med-green/30 transition-colors">
                                    <div className="flex justify-between items-start mb-4">
                                        <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">{stat.column}</span>
                                        <div className="w-1.5 h-1.5 rounded-full bg-med-green"></div>
                                    </div>
                                    <div className="text-3xl font-black text-slate-900 mb-1">{stat.mean?.toFixed(1) || "-"}</div>
                                    <div className="text-[10px] text-slate-500 uppercase mb-4">Arithmetic Mean</div>
                                    <div className="space-y-2 border-t border-slate-200 pt-3">
                                        <div className="flex justify-between text-xs text-slate-600">
                                            <span>Minimum</span> <span className="font-mono">{stat.min}</span>
                                        </div>
                                        <div className="flex justify-between text-xs text-slate-600">
                                            <span>Maximum</span> <span className="font-mono">{stat.max}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Simple fallbacks for complex charts for now */}
                    {(viewType !== 'histogram' && viewType !== 'summary') && (
                        <pre className="p-6 bg-slate-950 text-emerald-400 rounded-xl font-mono text-xs overflow-auto h-full shadow-inner">
                            {JSON.stringify(data, null, 2)}
                        </pre>
                    )}
                </div>
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
            {/* Header / Context Bar */}
            <header className="h-16 bg-white border-b border-slate-200 px-8 flex items-center justify-between sticky top-0 z-40">
                <div className="flex items-center gap-6">
                    <div className="flex items-center gap-2 group cursor-pointer">
                        <Shield className="text-med-green w-6 h-6" />
                        <span className="font-bold text-xl tracking-tight text-slate-900 italic">MedIQ</span>
                    </div>
                    <div className="h-4 w-px bg-slate-200"></div>
                    <div className="flex items-center gap-3">
                        <FlaskConical className="w-5 h-5 text-slate-400" />
                        <h1 className="font-semibold text-slate-700">Exploratory Data Engine</h1>
                    </div>
                </div>

                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-lg border border-slate-200">
                        {activeSession ? (
                            <>
                                <CheckCircle className="w-4 h-4 text-med-green" />
                                <span className="text-xs font-bold text-slate-600 truncate max-w-[150px] uppercase tracking-wider">{activeSession.title}</span>
                            </>
                        ) : (
                            <>
                                <div className="w-2 h-2 rounded-full bg-slate-300"></div>
                                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">No active session</span>
                            </>
                        )}
                    </div>
                    <Button variant="outline" size="sm" onClick={() => setIsCreateModalOpen(true)} className="border-slate-200 text-slate-600 hover:text-med-green hover:border-med-green/50">
                        <Plus className="w-4 h-4 mr-2" /> Session
                    </Button>
                    <div className="h-4 w-px bg-slate-200 mx-1"></div>
                    <Button variant="ghost" size="sm" onClick={handleLogout} className="text-slate-400 hover:text-red-600">
                        <LogOut className="w-4 h-4" />
                    </Button>
                </div>
            </header>

            <div className="flex-1 flex overflow-hidden">
                {/* Sidebar: Session History & Selector */}
                <aside className="w-72 bg-white border-r border-slate-200 flex flex-col shrink-0">
                    <div className="p-4 border-b border-slate-100 space-y-4">
                        <div className="space-y-4">
                            <div>
                                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Primary Dataset</label>
                                <select
                                    className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-sm text-slate-900 font-medium focus:ring-1 focus:ring-med-green/20 outline-none"
                                    value={selectedDataset?.id || ""}
                                    onChange={(e) => setSelectedDataset(DATASETS.find(d => d.id === e.target.value) || DATASETS[0])}
                                >
                                    {DATASETS.map(ds => <option key={ds.id} value={ds.id}>{ds.name}</option>)}
                                </select>
                            </div>
                            <div>
                                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block mb-2">Target Metric</label>
                                <div className="flex flex-wrap gap-1.5">
                                    {selectedDataset?.columns?.map(c => (
                                        <button
                                            key={c}
                                            onClick={() => setSelectedColumn(c)}
                                            className={`px-2 py-1 rounded-md text-[10px] font-bold border transition-all ${selectedColumn === c
                                                ? 'bg-med-green text-white border-med-green shadow-sm'
                                                : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50'
                                                }`}
                                        >
                                            {c.toUpperCase()}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="flex-1 overflow-auto p-4 custom-scrollbar">
                        <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-4">Research Workspace</h4>
                        <div className="space-y-2">
                            {sessions.map((s) => (
                                <div
                                    key={s.id}
                                    onClick={() => setActiveSession(s)}
                                    className={`p-3 rounded-xl border cursor-pointer transition-all ${activeSession?.id === s.id
                                        ? 'bg-med-green/5 border-med-green shadow-sm'
                                        : 'bg-white border-slate-100 hover:bg-slate-50 hover:border-slate-200'
                                        }`}
                                >
                                    <div className="flex items-center justify-between mb-1">
                                        <span className={`text-[10px] font-bold uppercase ${activeSession?.id === s.id ? 'text-med-green' : 'text-slate-400'}`}>
                                            {s.status}
                                        </span>
                                        <ChevronRight className={`w-3 h-3 ${activeSession?.id === s.id ? 'text-med-green' : 'text-slate-300'}`} />
                                    </div>
                                    <h5 className="text-sm font-bold text-slate-900 truncate mb-1">{s.title}</h5>
                                    <p className="text-[10px] text-slate-500 truncate">{s.purpose}</p>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="p-4 border-t border-slate-100 italic text-[10px] text-slate-400 font-mono text-center">
                        MedIQ Secure Interface v1.4.2
                    </div>
                </aside>

                {/* Main Content Workspace */}
                <main className="flex-1 p-8 overflow-auto">
                    {error && (
                        <div className="mb-6 bg-red-50 border border-red-200 text-red-600 p-4 rounded-xl text-sm flex items-center gap-3">
                            <AlertCircle className="w-5 h-5" /> {error}
                        </div>
                    )}

                    {renderContent()}
                </main>
            </div>

            {/* Create Session Modal Overlay */}
            <AnimatePresence>
                {isCreateModalOpen && (
                    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
                        <motion.div
                            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                            className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm"
                            onClick={() => setIsCreateModalOpen(false)}
                        />
                        <motion.div
                            initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.95, opacity: 0 }}
                            className="bg-white rounded-3xl w-full max-w-xl shadow-2xl relative z-10 overflow-hidden"
                        >
                            <div className="p-8 border-b border-slate-100 bg-slate-50/50">
                                <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Create Research Session</h1>
                                <p className="text-slate-500 text-sm mt-1">Specify session objectives and required data fields.</p>
                            </div>
                            <form onSubmit={handleCreateSession} className="p-8 space-y-6">
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-slate-600 uppercase tracking-widest">Session Title</label>
                                    <input
                                        type="text" required
                                        placeholder="e.g. Oncology Longitudinal Study 2024"
                                        className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-1 focus:ring-med-green outline-none text-slate-900"
                                        value={newSession.title}
                                        onChange={(e) => setNewSession({ ...newSession, title: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-slate-600 uppercase tracking-widest">Research Purpose</label>
                                    <input
                                        type="text" required
                                        placeholder="e.g. Statistical analysis of baseline biomarkers"
                                        className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-1 focus:ring-med-green outline-none text-slate-900"
                                        value={newSession.purpose}
                                        onChange={(e) => setNewSession({ ...newSession, purpose: e.target.value })}
                                    />
                                </div>
                                <div className="pt-4 flex gap-3">
                                    <Button type="button" variant="ghost" onClick={() => setIsCreateModalOpen(false)} className="flex-1 rounded-xl text-slate-500">Cancel</Button>
                                    <Button type="submit" disabled={loading} className="flex-1 bg-med-green hover:bg-med-green/90 text-white rounded-xl">
                                        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Authorize & Start"}
                                    </Button>
                                </div>
                            </form>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>

            <style jsx global>{`
                .custom-scrollbar::-webkit-scrollbar { width: 4px; }
                .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
                .custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
            `}</style>
        </div>
    );
}
