
import { useState, useCallback, useEffect } from 'react';
import { edaApi } from '@/lib/eda-api';
import * as T from '@/types/eda';
import { ResearchSession, SessionCreate } from '@/types/session';

export type EdaViewType =
    | 'summary' | 'unique' | 'missing' | 'histogram' | 'boxplot'
    | 'percentiles' | 'correlation' | 'scatter' | 'groupby'
    | 'segment' | 'trend' | 'outliers' | 'report' | null;

export function useEda() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [viewType, setViewType] = useState<EdaViewType>(null);
    const [data, setData] = useState<any>(null);

    // Session State
    const [sessions, setSessions] = useState<ResearchSession[]>([]);
    const [activeSession, setActiveSession] = useState<ResearchSession | null>(null);

    const fetchSessions = useCallback(async () => {
        setLoading(true);
        try {
            const res = await edaApi.listSessions();
            setSessions(res.sessions);
            if (res.sessions.length > 0 && !activeSession) {
                setActiveSession(res.sessions[0] || null);
            }
        } catch (err) {
            setError('Failed to load sessions');
        } finally {
            setLoading(false);
        }
    }, [activeSession]);

    const createSession = async (sessionData: SessionCreate) => {
        setLoading(true);
        try {
            const newSession = await edaApi.createSession(sessionData);
            setSessions(prev => [newSession, ...prev]);
            setActiveSession(newSession);
            return newSession;
        } catch (err) {
            setError('Failed to create session');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const wrapApi = async (fn: () => Promise<any>, type: EdaViewType) => {
        if (!activeSession) {
            setError('Please select an active research session first');
            return;
        }
        setLoading(true);
        setError(null);
        try {
            const res = await fn();
            setData(res);
            setViewType(type);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Analysis failed');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return {
        loading,
        error,
        viewType,
        data,
        sessions,
        activeSession,
        setActiveSession,
        fetchSessions,
        createSession,
        actions: {
            fetchSummary: (id: string, cols: string[]) => wrapApi(() => edaApi.getSummaryStats(id, cols), 'summary'),
            fetchUnique: (id: string, col: string) => wrapApi(() => edaApi.getUniqueValues(id, col), 'unique'),
            fetchMissing: (id: string, cols: string[]) => wrapApi(() => edaApi.getMissingAnalysis(id, cols), 'missing'),
            fetchHistogram: (id: string, col: string, bins?: number) => wrapApi(() => edaApi.getHistogram(id, col, bins), 'histogram'),
            fetchBoxplot: (id: string, col: string) => wrapApi(() => edaApi.getBoxplot(id, col), 'boxplot'),
            fetchPercentiles: (id: string, col: string) => wrapApi(() => edaApi.getPercentiles(id, col), 'percentiles'),
            fetchCorrelation: (id: string, cols: string[]) => wrapApi(() => edaApi.getCorrelation(id, cols), 'correlation'),
            fetchScatter: (id: string, x: string, y: string) => wrapApi(() => edaApi.getScatter(id, x, y), 'scatter'),
            fetchGroupBy: (id: string, group: string, metric: string) => wrapApi(() => edaApi.getGroupBy(id, group, metric), 'groupby'),
            fetchOutliers: (id: string, col: string) => wrapApi(() => edaApi.getOutliers(id, col), 'outliers'),
            fetchTrend: (id: string, col: string) => wrapApi(() => edaApi.getTimeTrend(id, col), 'trend'),
            fetchSegment: (id: string, rules: any[]) => wrapApi(() => edaApi.getSegment(id, rules), 'segment'),
            fetchReport: (id: string, sections: string[]) => wrapApi(() => edaApi.getReport(id, sections), 'report'),
        },
        reset: () => { setData(null); setViewType(null); setError(null); }
    };
}
