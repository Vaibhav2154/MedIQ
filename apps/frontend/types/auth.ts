
export interface ResearcherProfile {
    id: string;
    email: string;
    full_name: string;
    institution?: string;
    research_interests?: string;
    credentials?: string;
    is_active: boolean;
    is_verified: boolean;
    created_at: string;
    last_login?: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
    expires_in: number;
    researcher: ResearcherProfile;
}

export interface ResearcherLogin {
    email: string;
    password: string;
}

export interface ResearcherSignup {
    email: string;
    password: string;
    full_name: string;
    institution?: string;
    research_interests?: string;
    credentials?: string;
}
