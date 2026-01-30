
import axios from 'axios';
import * as T from '@/types/eda';
import { ResearchSession, SessionCreate, SessionUpdate, SessionListResponse } from '@/types/session';
import { ResearcherLogin, ResearcherSignup, TokenResponse } from '@/types/auth';

const API_BASE_URL = 'http://localhost:8003';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const edaApi = {
    // Authentication
    login: async (credentials: ResearcherLogin): Promise<TokenResponse> => {
        const res = await api.post('/api/v1/auth/login', credentials);
        return res.data;
    },
    signup: async (data: ResearcherSignup): Promise<TokenResponse> => {
        const res = await api.post('/api/v1/auth/signup', data);
        return res.data;
    },

    // Session Management
    listSessions: async (status?: string): Promise<SessionListResponse> => {
        const res = await api.get('/api/v1/sessions', { params: { status_filter: status } });
        return res.data;
    },
    createSession: async (data: SessionCreate): Promise<ResearchSession> => {
        const res = await api.post('/api/v1/sessions', data);
        return res.data;
    },
    getSession: async (id: string): Promise<ResearchSession> => {
        const res = await api.get(`/api/v1/sessions/${id}`);
        return res.data;
    },
    updateSession: async (id: string, data: SessionUpdate): Promise<ResearchSession> => {
        const res = await api.put(`/api/v1/sessions/${id}`, data);
        return res.data;
    },

    // EDA Endpoints
    getSummaryStats: async (datasetId: string, columns: string[]): Promise<T.SummaryStats[]> => {
        const res = await api.post('/api/v1/eda/summary-stats', { dataset_id: datasetId, columns });
        return res.data;
    },
    getUniqueValues: async (datasetId: string, column: string): Promise<T.UniqueValuesOutput> => {
        const res = await api.post('/api/v1/eda/unique-values', { dataset_id: datasetId, column });
        return res.data;
    },
    getMissingAnalysis: async (datasetId: string, columns: string[]): Promise<T.MissingAnalysisOutput[]> => {
        const res = await api.post('/api/v1/eda/missing-analysis', { dataset_id: datasetId, columns });
        return res.data;
    },
    getHistogram: async (datasetId: string, column: string, bins: number = 10): Promise<T.HistogramOutput> => {
        const res = await api.post('/api/v1/eda/histogram', { dataset_id: datasetId, column, bins });
        return res.data;
    },
    getBoxplot: async (datasetId: string, column: string): Promise<T.BoxPlotOutput> => {
        const res = await api.post('/api/v1/eda/boxplot', { dataset_id: datasetId, column });
        return res.data;
    },
    getPercentiles: async (datasetId: string, column: string, percentiles: number[] = [25, 50, 75, 90]): Promise<T.PercentilesOutput> => {
        const res = await api.post('/api/v1/eda/percentiles', { dataset_id: datasetId, column, percentiles });
        return res.data;
    },
    getCorrelation: async (datasetId: string, columns: string[]): Promise<T.CorrelationOutput> => {
        const res = await api.post('/api/v1/eda/correlation', { dataset_id: datasetId, columns });
        return res.data;
    },
    getScatter: async (datasetId: string, x: string, y: string): Promise<T.ScatterOutput> => {
        const res = await api.post('/api/v1/eda/scatter', { dataset_id: datasetId, x, y });
        return res.data;
    },
    getGroupBy: async (datasetId: string, group_column: string, metric_column: string): Promise<T.GroupByOutput> => {
        const res = await api.post('/api/v1/eda/group-by', { dataset_id: datasetId, group_column, metric_column });
        return res.data;
    },
    getSegment: async (datasetId: string, rules: any[]): Promise<T.SegmentationOutput> => {
        const res = await api.post('/api/v1/eda/segment', { dataset_id: datasetId, rules });
        return res.data;
    },
    getTimeTrend: async (datasetId: string, column: string, time_unit: string = "month"): Promise<T.TimeTrendOutput> => {
        const res = await api.post('/api/v1/eda/time-trend', { dataset_id: datasetId, column, time_unit });
        return res.data;
    },
    getOutliers: async (datasetId: string, column: string): Promise<T.OutlierOutput> => {
        const res = await api.post('/api/v1/eda/outliers', { dataset_id: datasetId, column });
        return res.data;
    },
    getReport: async (datasetId: string, sections: string[]): Promise<T.ReportOutput> => {
        const res = await api.post('/api/v1/eda/report', { dataset_id: datasetId, sections });
        return res.data;
    }
};
