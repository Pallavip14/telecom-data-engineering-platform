-- =========================================================
-- TELECONNECT ANALYTICS
-- =========================================================


-- =========================================================
-- 1. MONTHLY RECHARGE REVENUE
-- =========================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(r.amount) AS total_recharge_revenue
FROM dw.fact_recharge r
JOIN dw.dim_date d
    ON r.date_key = d.date_key
WHERE r.status = 'SUCCESS'
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- =========================================================
-- 2. REVENUE BY PLAN
-- =========================================================

SELECT
    p.plan_name,
    p.plan_type,
    SUM(r.amount) AS total_revenue,
    COUNT(*) AS successful_recharges
FROM dw.fact_recharge r
JOIN dw.dim_customer c
    ON r.customer_key = c.customer_key
JOIN dw.dim_plan p
    ON c.plan_id = p.plan_id
WHERE r.status = 'SUCCESS'
GROUP BY
    p.plan_name,
    p.plan_type
ORDER BY
    total_revenue DESC;


-- =========================================================
-- 3. ACTIVE CUSTOMERS BY PLAN
-- =========================================================

SELECT
    p.plan_name,
    COUNT(*) AS active_customers
FROM dw.dim_customer c
JOIN dw.dim_plan p
    ON c.plan_id = p.plan_id
WHERE c.status = 'ACTIVE'
GROUP BY
    p.plan_name
ORDER BY
    active_customers DESC;


-- =========================================================
-- 4. MONTHLY DATA USAGE
-- =========================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(u.data_used_gb), 2) AS total_data_used_gb
FROM dw.fact_usage u
JOIN dw.dim_date d
    ON u.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- =========================================================
-- 5. TOP CUSTOMERS BY DATA USAGE
-- =========================================================

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    ROUND(SUM(u.data_used_gb), 2) AS total_data_used_gb
FROM dw.fact_usage u
JOIN dw.dim_customer c
    ON u.customer_key = c.customer_key
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city
ORDER BY
    total_data_used_gb DESC
LIMIT 10;


-- =========================================================
-- 6. COMPLAINTS BY CATEGORY
-- =========================================================

SELECT
    category,
    COUNT(*) AS complaint_count
FROM dw.fact_complaint
GROUP BY
    category
ORDER BY
    complaint_count DESC;


-- =========================================================
-- 7. COMPLAINTS BY PRIORITY
-- =========================================================

SELECT
    priority,
    COUNT(*) AS complaint_count
FROM dw.fact_complaint
GROUP BY
    priority
ORDER BY
    complaint_count DESC;


-- =========================================================
-- 8. MONTHLY COMPLAINT TREND
-- =========================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(*) AS complaint_count
FROM dw.fact_complaint c
JOIN dw.dim_date d
    ON c.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- =========================================================
-- 9. PAYMENT SUCCESS RATE
-- =========================================================

SELECT
    COUNT(*) AS total_payments,

    COUNT(*) FILTER (
        WHERE status = 'SUCCESS'
    ) AS successful_payments,

    ROUND(
        COUNT(*) FILTER (
            WHERE status = 'SUCCESS'
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percentage

FROM dw.fact_payment;


-- =========================================================
-- 10. NETWORK EVENTS BY CITY
-- =========================================================

SELECT
    city,
    COUNT(*) AS total_network_events,
    SUM(affected_users) AS total_affected_users,
    ROUND(AVG(duration_minutes), 2) AS avg_event_duration_minutes
FROM dw.fact_network_event
GROUP BY
    city
ORDER BY
    total_affected_users DESC;


-- =========================================================
-- 11. NETWORK EVENTS BY SEVERITY
-- =========================================================

SELECT
    severity,
    COUNT(*) AS event_count,
    SUM(affected_users) AS total_affected_users
FROM dw.fact_network_event
GROUP BY
    severity
ORDER BY
    event_count DESC;


-- =========================================================
-- 12. NETWORK EVENTS BY EVENT TYPE
-- =========================================================

SELECT
    event_type,
    COUNT(*) AS event_count,
    SUM(duration_minutes) AS total_duration_minutes,
    SUM(affected_users) AS total_affected_users
FROM dw.fact_network_event
GROUP BY
    event_type
ORDER BY
    event_count DESC;


-- =========================================================
-- 13. MONTHLY PAYMENT REVENUE
-- =========================================================

SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(p.amount) FILTER (
        WHERE p.status = 'SUCCESS'
    ) AS successful_payment_amount
FROM dw.fact_payment p
JOIN dw.dim_date d
    ON p.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;