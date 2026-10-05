-- =========================================================
-- TELECONNECT DATA WAREHOUSE LOAD
-- =========================================================


-- =========================================================
-- 1. LOAD CUSTOMER DIMENSION
-- =========================================================

INSERT INTO dw.dim_customer (
    customer_id,
    first_name,
    last_name,
    gender,
    date_of_birth,
    city,
    state,
    registration_date,
    plan_id,
    status
)
SELECT
    customer_id,
    first_name,
    last_name,
    gender,
    date_of_birth,
    city,
    state,
    registration_date,
    plan_id,
    status
FROM staging.customers
ON CONFLICT (customer_id) DO NOTHING;


-- =========================================================
-- 2. LOAD PLAN DIMENSION
-- =========================================================

INSERT INTO dw.dim_plan (
    plan_id,
    plan_name,
    plan_type,
    price,
    data_gb,
    validity_days,
    voice_minutes,
    sms_limit,
    status
)
SELECT
    plan_id,
    plan_name,
    plan_type,
    price,
    data_gb,
    validity_days,
    voice_minutes,
    sms_limit,
    status
FROM staging.plans
ON CONFLICT (plan_id) DO NOTHING;


-- =========================================================
-- 3. LOAD DATE DIMENSION
-- =========================================================

INSERT INTO dw.dim_date (
    date_key,
    full_date,
    year,
    month,
    month_name,
    quarter,
    day,
    day_of_week,
    day_name
)
SELECT
    TO_CHAR(date_value, 'YYYYMMDD')::INTEGER,
    date_value,
    EXTRACT(YEAR FROM date_value)::INTEGER,
    EXTRACT(MONTH FROM date_value)::INTEGER,
    TRIM(TO_CHAR(date_value, 'Month')),
    EXTRACT(QUARTER FROM date_value)::INTEGER,
    EXTRACT(DAY FROM date_value)::INTEGER,
    EXTRACT(ISODOW FROM date_value)::INTEGER,
    TRIM(TO_CHAR(date_value, 'Day'))
FROM generate_series(
    DATE '2023-09-23',
    DATE '2026-09-22',
    INTERVAL '1 day'
) AS date_series(date_value)
ON CONFLICT (date_key) DO NOTHING;


-- =========================================================
-- 4. LOAD RECHARGE FACT
-- =========================================================

INSERT INTO dw.fact_recharge (
    recharge_id,
    date_key,
    customer_key,
    amount,
    payment_mode,
    status
)
SELECT
    r.recharge_id,
    d.date_key,
    c.customer_key,
    r.amount,
    r.payment_mode,
    r.status
FROM staging.recharges r
JOIN dw.dim_customer c
    ON r.customer_id = c.customer_id
JOIN dw.dim_date d
    ON r.recharge_date = d.full_date
ON CONFLICT (recharge_id) DO NOTHING;


-- =========================================================
-- 5. LOAD USAGE FACT
-- =========================================================

INSERT INTO dw.fact_usage (
    usage_id,
    date_key,
    customer_key,
    data_used_gb,
    voice_minutes,
    sms_count
)
SELECT
    u.usage_id,
    d.date_key,
    c.customer_key,
    u.data_used_gb,
    u.voice_minutes,
    u.sms_count
FROM staging.usage u
JOIN dw.dim_customer c
    ON u.customer_id = c.customer_id
JOIN dw.dim_date d
    ON u.usage_date = d.full_date
ON CONFLICT (usage_id) DO NOTHING;


-- =========================================================
-- 6. LOAD PAYMENT FACT
-- =========================================================

INSERT INTO dw.fact_payment (
    payment_id,
    date_key,
    customer_key,
    amount,
    payment_method,
    status
)
SELECT
    p.payment_id,
    d.date_key,
    c.customer_key,
    p.amount,
    p.payment_method,
    p.status
FROM staging.payments p
JOIN dw.dim_customer c
    ON p.customer_id = c.customer_id
JOIN dw.dim_date d
    ON p.payment_date = d.full_date
ON CONFLICT (payment_id) DO NOTHING;


-- =========================================================
-- 7. LOAD COMPLAINT FACT
-- =========================================================

INSERT INTO dw.fact_complaint (
    complaint_id,
    date_key,
    customer_key,
    category,
    title,
    priority,
    status
)
SELECT
    c.complaint_id,
    d.date_key,
    dc.customer_key,
    c.category,
    c.title,
    c.priority,
    c.status
FROM staging.complaints c
JOIN dw.dim_customer dc
    ON c.customer_id = dc.customer_id
JOIN dw.dim_date d
    ON c.complaint_date = d.full_date
ON CONFLICT (complaint_id) DO NOTHING;


-- =========================================================
-- 8. LOAD NETWORK EVENT FACT
-- =========================================================

INSERT INTO dw.fact_network_event (
    event_id,
    date_key,
    city,
    event_type,
    severity,
    duration_minutes,
    affected_users,
    status
)
SELECT
    n.event_id,
    d.date_key,
    n.city,
    n.event_type,
    n.severity,
    n.duration_minutes,
    n.affected_users,
    n.status
FROM staging.network_events n
JOIN dw.dim_date d
    ON n.event_date = d.full_date
ON CONFLICT (event_id) DO NOTHING;