-- =======================================
-- DROP TABLES IF THEY EXIST (CLEAN START)
-- =======================================

DROP TABLE IF EXISTS Sessions;

CREATE TABLE Sessions (
    session_id SERIAL PRIMARY KEY,
    user_id SERIAL VARCHAR(100),
    created_at DATE NOT NULL,
    expires_at DATE NOT NULL,
    last_active DATE NOT NULL,
    roles VARCHAR(100),
    metadata TEXT
)