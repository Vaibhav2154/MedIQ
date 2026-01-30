
export enum SessionStatus {
    ACTIVE = "active",
    PAUSED = "paused",
    COMPLETED = "completed",
    ARCHIVED = "archived"
}

export interface ResearchSession {
    id: string;
    researcher_id: string;
    title: string;
    purpose: string;
    description?: string;
    institution?: string;
    irb_approval_number?: string;
    start_date?: string;
    end_date?: string;
    status: SessionStatus;
    requested_fields: string[];
    data_scope?: Record<string, any>;
    session_metadata?: Record<string, any>;
    data_access_count: number;
    last_accessed_at?: string;
    created_at: string;
    updated_at: string;
}

export interface SessionCreate {
    title: string;
    purpose: string;
    description?: string;
    institution?: string;
    irb_approval_number?: string;
    requested_fields: string[];
    data_scope?: Record<string, any>;
    start_date?: string;
    end_date?: string;
    session_metadata?: Record<string, any>;
}

export interface SessionUpdate {
    title?: string;
    description?: string;
    status?: SessionStatus;
    end_date?: string;
    requested_fields?: string[];
    data_scope?: Record<string, any>;
    session_metadata?: Record<string, any>;
}

export interface SessionListResponse {
    sessions: ResearchSession[];
    total: number;
    limit: number;
    offset: number;
}
