CREATE TABLE users (
    pk SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    user_name VARCHAR(50),
);

CREATE TABLE accounts (
    pk SERIAL PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL,
    account_type VARCHAR(100) NOT NULL,
    account_provider VARCHAR(100) NOT NULL,
    user_pk INTEGER NOT NULL,
    UNIQUE (account_provider, account_id)
);

CREATE TABLE emails (
    pk SERIAL PRIMARY KEY,
    email_address VARCHAR(100) UNIQUE NOT NULL,
    email_is_primary BOOLEAN NOT NULL,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    user_pk INTEGER NOT NULL,
    FOREIGN KEY (user_pk) REFERENCES users(pk) ON DELETE CASCADE
);

CREATE UNIQUE INDEX ON emails (user_pk) WHERE email_is_primary = TRUE;