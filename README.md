# MedIQ



### Planned folder structure

```

consent-execution-platform/
│
├── apps/
│   ├── backend/
│   │   ├── identity-service/
│   │   ├── consent-ingestion/
│   │   ├── consent-intelligence/
│   │   ├── policy-engine/
│   │   ├── data-router/
│   │   ├── audit-service/
│   │   └── research-sandbox/
│   │
│   ├── frontend/
│   │   └── nextjs-app/
│   │
│   └── api-gateway/          
│       ├── nginx/
│       │   ├── nginx.conf
│       │   └── routes.conf
│       ├── Dockerfile
│       └── README.md
│
├── packages/
├── infra/
├── docs/
├── docker-compose.yml
└── README.md
```


mermaid
```

graph TD
    subgraph Client Portal
        C[Client User] -->|1. Login| C_Login[Login Page]
        C_Login -->|Success| C_Dash[Client Dashboard]
        
        C_Dash -->|2. Toggle Consent| Policy{Consent Policy}
        Policy -->|Update| LS[(LocalStorage)]
        
        C_Dash -->|3. View Logs| C_Enforce[Enforcement Monitor]
        LS -->|Read Policy| C_Enforce
        C_Enforce -->|Display| Logs[Audit Logs: Allowed/Blocked]
    end

    subgraph Researcher Portal
        R[Researcher User] -->|4. Login| R_Login[Login Page]
        R_Login -->|Success| R_EDA[EDA Dashboard]
        
        R_EDA -->|5. Request Data| Enforcer{Enforcement Engine}
        LS -->|Read Policy| Enforcer
        
        Enforcer -->|Policy: GRANTED| Data[View Health Data / Charts]
        Enforcer -->|Policy: REVOKED| Block[Access Denied Overlay]
    end

    %% Styles
    classDef client fill:#e0f2fe,stroke:#3b82f6,stroke-width:2px;
    classDef researcher fill:#f0fdf4,stroke:#22c55e,stroke-width:2px;
    classDef storage fill:#fef3c7,stroke:#d97706,stroke-width:2px;
    classDef logic fill:#f3e8ff,stroke:#a855f7,stroke-width:2px;
    classDef block fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b;
    classDef allow fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#166534;

    class C,C_Login,C_Dash,C_Enforce client;
    class R,R_Login,R_EDA researcher;
    class LS storage;
    class Policy,Enforcer logic;
    class Block block;
    class Data allow;
```