-- =========================================================
-- TELECONNECT DATA WAREHOUSE
-- STAR SCHEMA
-- =========================================================

CREATE SCHEMA IF NOT EXISTS dw;


-- =========================================================
-- DIMENSION: CUSTOMER
-- =========================================================

CREATE TABLE IF NOT EXISTS dw.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(20),
    date_of_birth DATE,
    city VARCHAR(100),
    state VARCHAR(100),
    registration_date DATE,
    plan_id VARCHAR(20),
    status VARCHAR(20)
);


-- =========================================================
-- DIMENSION: PLAN
-- =========================================================

CREATE TABLE IF NOT EXISTS dw.dim_plan (
    plan_key SERIAL PRIMARY KEY,
    plan_id VARCHAR(20) UNIQUE NOT NULL,
    plan_name VARCHAR(100),
    plan_type VARCHAR(50),
    price NUMERIC(10, 2),
    data_gb NUMERIC(10, 2),
    validity_days INTEGER,
    voice_minutes INTEGER,
    sms_limit INTEGER,
    status VARCHAR(20)
);


-- =========================================================
-- DIMENSION: DATE
-- =========================================================

CREATE TABLE IF NOT EXISTS dw.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER,
    day INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(20)
);


-- =========================================================
-- FACT: RECHARGE
-- Grain: One row = One recharge transaction
-- =========================================================

CREATE TABLE IF NOT EXISTS dw.fact_recharge (
    recharge_key SERIAL PRIMARY KEY,
    recharge_id VARCHAR(20) UNIQUE NOT NULL,

    date_key INTEGER,
    customer_key INTEGER,

    amount NUMERIC(10, 2),
    payment_mode VARCHAR(50),
    status VARCHAR(30),

    FOREIGN KEY (date_key)
        REFERENCES dw.dim_date(date_key),

    FOREIGN KEY (customer_key)
        REFERENCES dw.dim_customer(customer_key)
);


-- =========================================================
-- FACT: USAGE
-- Grain: One row = One usage record
-- =========================================================

CREATE TABLE IF NOT EXISTS dw.fact_usage (
    usage_key SERIAL PRIMARY KEY,
    usage_id VARCHAR(20) UNIQUE NOT NULL,

    date_key INTEGER,
    customer_key INTEGER,

    data_used_gb NUMERIC(10, 2),
    voice_minutes INTEGER,
    sms_count INTEGER,

    FOREIGN KEY (date_key)
        REFERENCES dw.dim_date(date_key),

    FOREIGN KEY (customer_key)
        REFERENCES dw.dim_customer(customer_key)
);


-- =========================================================
-- FACT: PAYMENT
-- Grain: One row = One payment transaction
-- =========================================================

CREATE TABLE IF NOT EXISTS dw.fact_payment (
    payment_key SERIAL PRIMARY KEY,
    payment_id VARCHAR(20) UNIQUE NOT NULL,

    date_key INTEGER,
    customer_key INTEGER,

    amount NUMERIC(10, 2),
    payment_method VARCHAR(50),
    status VARCHAR(30),

    FOREIGN KEY (date_key)
        REFERENCES dw.dim_date(date_key),

    FOREIGN KEY (customer_key)
        REFERENCES dw.dim_customer(customer_key)
);


-- =========================================================
-- FACT: COMPLAINT
-- Grain: One row = One complaint
-- =========================================================

CREATE TABLE IF NOT EXISTS dw.fact_complaint (
    complaint_key SERIAL PRIMARY KEY,
    complaint_id VARCHAR(20) UNIQUE NOT NULL,

    date_key INTEGER,
    customer_key INTEGER,

    category VARCHAR(50),
    title VARCHAR(255),
    priority VARCHAR(20),
    status VARCHAR(30),

    FOREIGN KEY (date_key)
        REFERENCES dw.dim_date(date_key),

    FOREIGN KEY (customer_key)
        REFERENCES dw.dim_customer(customer_key)
);


-- =========================================================
-- FACT: NETWORK EVENT
-- Grain: One row = One network event
-- =========================================================

CREATE TABLE IF NOT EXISTS dw.fact_network_event (
    network_event_key SERIAL PRIMARY KEY,
    event_id VARCHAR(20) UNIQUE NOT NULL,

    date_key INTEGER,

    city VARCHAR(100),
    event_type VARCHAR(50),
    severity VARCHAR(20),
    duration_minutes INTEGER,
    affected_users INTEGER,
    status VARCHAR(30),

    FOREIGN KEY (date_key)
        REFERENCES dw.dim_date(date_key)
);


-- =========================================================
-- VERIFY TABLES
-- =========================================================

SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'dw'
ORDER BY table_name;