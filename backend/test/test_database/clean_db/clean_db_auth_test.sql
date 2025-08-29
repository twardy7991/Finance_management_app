DROP TABLE IF EXISTS sessions;

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    user_id INTEGER UNIQUE,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    last_active TIMESTAMP NOT NULL,
    roles TEXT[],
    session_metadata JSON
);

-- INSERT INTO sessions (id, session_id, user_id, created_at, expires_at, last_active) VALUES

-- (10, 'SCKXWjK7uIgKefL3tY8C862ny-t07I1Mn5Gx5DnwfPA', 1, '2025-08-20', '2025-12-30', '2025-08-20');