-- Seed Patients for Identity Service
-- This script creates 625 patients distributed across disease categories (125 per category)
-- Each patient gets a unique ABHA ID in the format XX-XXXX-XXXX-XXXX
-- Optimized using generate_series for efficient bulk inserts

-- Clear existing patients (optional, comment out if you want to keep existing data)
-- TRUNCATE TABLE patients CASCADE;

-- Use generate_series for efficient bulk inserts
-- This creates 125 patients per category (625 total)

-- Diabetes Patients (125) - ABHA prefix 91-2345
INSERT INTO patients (id, abha_id, created_at, updated_at)
SELECT 
    ('d1000000-0000-0000-0000-' || lpad(i::text, 12, '0'))::uuid,
    '91-2345-' || lpad((i / 10000)::text, 4, '0') || '-' || lpad((i % 10000)::text, 4, '0'),
    NOW(),
    NOW()
FROM generate_series(1, 125) AS i;

-- Hypertension Patients (125) - ABHA prefix 91-3456
INSERT INTO patients (id, abha_id, created_at, updated_at)
SELECT 
    ('d2000000-0000-0000-0000-' || lpad(i::text, 12, '0'))::uuid,
    '91-3456-' || lpad((i / 10000)::text, 4, '0') || '-' || lpad((i % 10000)::text, 4, '0'),
    NOW(),
    NOW()
FROM generate_series(1, 125) AS i;

-- Cardiovascular Disease Patients (125) - ABHA prefix 91-4567
INSERT INTO patients (id, abha_id, created_at, updated_at)
SELECT 
    ('d3000000-0000-0000-0000-' || lpad(i::text, 12, '0'))::uuid,
    '91-4567-' || lpad((i / 10000)::text, 4, '0') || '-' || lpad((i % 10000)::text, 4, '0'),
    NOW(),
    NOW()
FROM generate_series(1, 125) AS i;

-- Respiratory Disease Patients (125) - ABHA prefix 91-5678
INSERT INTO patients (id, abha_id, created_at, updated_at)
SELECT 
    ('d4000000-0000-0000-0000-' || lpad(i::text, 12, '0'))::uuid,
    '91-5678-' || lpad((i / 10000)::text, 4, '0') || '-' || lpad((i % 10000)::text, 4, '0'),
    NOW(),
    NOW()
FROM generate_series(1, 125) AS i;

-- Cancer Patients (125) - ABHA prefix 91-6789
INSERT INTO patients (id, abha_id, created_at, updated_at)
SELECT 
    ('d5000000-0000-0000-0000-' || lpad(i::text, 12, '0'))::uuid,
    '91-6789-' || lpad((i / 10000)::text, 4, '0') || '-' || lpad((i % 10000)::text, 4, '0'),
    NOW(),
    NOW()
FROM generate_series(1, 125) AS i;

-- Display patient count
SELECT COUNT(*) as total_patients FROM patients;
SELECT 
    CASE 
        WHEN abha_id LIKE '91-2345%' THEN 'Diabetes'
        WHEN abha_id LIKE '91-3456%' THEN 'Hypertension'
        WHEN abha_id LIKE '91-4567%' THEN 'Cardiovascular'
        WHEN abha_id LIKE '91-5678%' THEN 'Respiratory'
        WHEN abha_id LIKE '91-6789%' THEN 'Cancer'
    END as category,
    COUNT(*) as count
FROM patients
GROUP BY category
ORDER BY category;
