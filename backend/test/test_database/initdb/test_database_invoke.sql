-- =======================================
-- DROP TABLES IF THEY EXIST (CLEAN START)
-- =======================================

DROP TABLE IF EXISTS financial_operations;
DROP TABLE IF EXISTS credentials;
DROP TABLE IF EXISTS users;

-- ========================
-- CREATE TABLES
-- ========================

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    telephone VARCHAR(20),
    address TEXT
);

CREATE TABLE credentials (
    credential_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE financial_operations (
    operation_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    operation_date DATE NOT NULL,
    category VARCHAR(50),
    description TEXT,
    value NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL
);

-- ========================
-- INSERT DUMMY USERS
-- ========================

INSERT INTO users (name, surname, telephone, address) VALUES
('John', 'Doe', '123456789', '123 Main St, Springfield'),
('Jane', 'Smith', '987654321', '456 Elm St, Springfield'),
('Alice', 'Brown', '555123456', '789 Oak Ave, Shelbyville'),
('Bob', 'Johnson', '666999333', '321 Pine Rd, Ogdenville');

-- ========================
-- INSERT CREDENTIALS
-- ========================

INSERT INTO credentials (user_id, username, password) VALUES
(1, 'johndoe', 'pass1'),
(2, 'janesmith', 'pass2'),
(3, 'aliceb', 'pass3'),
(4, 'bobbyj', 'pass4');

-- ========================
-- INSERT FINANCIAL OPERATIONS
-- ========================

INSERT INTO financial_operations (user_id, operation_date, category, description, value, currency) VALUES
-- John
(1, '2025-05-20', 'Groceries', 'Walmart grocery shopping', 75.20, 'USD'),
(1, '2025-05-21', 'Transport', 'Uber to downtown', 15.00, 'USD'),
(1, '2025-05-21', 'Entertainment', 'Netflix subscription', 12.99, 'USD'),

-- Jane
(2, '2025-05-18', 'Utilities', 'Electricity bill', -65.75, 'USD'),
(2, '2025-05-19', 'Dining', 'Dinner at Luigi''s', -45.00, 'USD'),
(2, '2025-05-22', 'Health', 'Pharmacy purchase', -22.10, 'USD'),

-- Alice
(3, '2025-05-17', 'Travel', 'Train ticket to Capital City', -30.00, 'USD'),
(3, '2025-05-18', 'Groceries', 'Local farmer''s market', -28.50, 'USD'),

-- Bob
(4, '2025-05-19', 'Education', 'Online course payment', -120.00, 'USD'),
(4, '2025-05-20', 'Books', 'Bought books on Amazon', -35.99, 'USD'),

(1, '2025-05-20', 'Groceries', 'Walmart grocery shopping', -75.20, 'USD'),
(1, '2025-05-21', 'Transport', 'Uber to downtown', -15.00, 'USD'),
(1, '2025-05-21', 'Entertainment', 'Netflix subscription', -12.99, 'USD'),

-- Jane
(1, '2025-05-18', 'Utilities', 'Electricity bill', 65.75, 'USD'),
(1, '2025-05-19', 'Dining', 'Dinner at Luigi''s', 45.00, 'USD'),
(1, '2025-05-22', 'Health', 'Pharmacy purchase', 22.10, 'USD'),

-- Alice
(1, '2025-05-17', 'Travel', 'Train ticket to Capital City', 30.00, 'USD'),
(1, '2025-05-18', 'Groceries', 'Local farmer''s market', 28.50, 'USD'),

-- Bob
(1, '2025-05-19', 'Education', 'Online course payment', 120.00, 'USD'),
(1, '2025-05-20', 'Books', 'Bought books on Amazon', 35.99, 'USD');
