-- Working!

CREATE TABLE clients (
    pk UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID, -- This is for reference but is managed by the Tenants Service
    name VARCHAR(255) NOT NULL,
    client_id VARCHAR(255) UNIQUE NOT NULL,
    client_secret TEXT NOT NULL,
    redirect_uris TEXT[] NOT NULL,
    grant_types TEXT[] NOT NULL,
    scopes TEXT[] NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
