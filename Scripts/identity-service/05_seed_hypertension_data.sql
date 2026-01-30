-- Seed Hypertension Medical Data (Optimized for 125 patients)
-- Uses generate_series and CTEs for efficient bulk inserts

-- Create encounters for all hypertension patients (3 encounters per patient = 375 total)
WITH org AS (
    SELECT id as org_id FROM organizations WHERE name = 'Fortis Healthcare' LIMIT 1
),
patient_list AS (
    SELECT id as patient_id, ROW_NUMBER() OVER (ORDER BY abha_id) as patient_num
    FROM patients WHERE abha_id LIKE '91-3456%'
),
encounter_types AS (
    SELECT * FROM (VALUES 
        (1, 'outpatient', 'Elevated blood pressure screening', '8 months', '1 hour'),
        (2, 'outpatient', 'Hypertension follow-up', '4 months', '45 minutes'),
        (3, 'outpatient', 'Routine blood pressure check', '3 weeks', '30 minutes')
    ) AS t(enc_num, enc_type, reason, time_ago, duration)
)
INSERT INTO encounters (id, patient_id, organization_id, encounter_type, reason, start_at, end_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    p.patient_id,
    o.org_id,
    e.enc_type,
    e.reason,
    NOW() - e.time_ago::interval,
    NOW() - e.time_ago::interval + e.duration::interval,
    NOW(),
    NOW()
FROM patient_list p
CROSS JOIN encounter_types e
CROSS JOIN org o;

-- Create observations
WITH encounter_data AS (
    SELECT 
        e.id as encounter_id, 
        e.patient_id, 
        e.start_at,
        ROW_NUMBER() OVER (PARTITION BY e.patient_id ORDER BY e.start_at) as enc_seq,
        (hashtext(e.patient_id::text) % 100) as patient_var
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-3456%'
)
INSERT INTO observations (id, patient_id, encounter_id, category, code, value, unit, effective_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    ed.patient_id,
    ed.encounter_id,
    obs.category,
    obs.code,
    CASE obs.code
        WHEN 'blood_pressure_systolic' THEN (155 - (ed.enc_seq * 10) + (ed.patient_var % 15))::text
        WHEN 'blood_pressure_diastolic' THEN (95 - (ed.enc_seq * 5) + (ed.patient_var % 10))::text
        WHEN 'heart_rate' THEN (78 - ed.enc_seq + (ed.patient_var % 8))::text
        WHEN 'weight' THEN (78 - ed.enc_seq + (ed.patient_var % 10))::text
        WHEN 'bmi' THEN (28 - (ed.enc_seq * 0.2) + ((ed.patient_var % 10) * 0.1))::text
        WHEN 'cholesterol_total' THEN (220 - (ed.enc_seq * 15) + (ed.patient_var % 20))::text
        WHEN 'ldl_cholesterol' THEN (140 - (ed.enc_seq * 12) + (ed.patient_var % 15))::text
        WHEN 'hdl_cholesterol' THEN (45 - (ed.patient_var % 5))::text
    END,
    obs.unit,
    ed.start_at,
    NOW(),
    NOW()
FROM encounter_data ed
CROSS JOIN (VALUES 
    ('vitals', 'blood_pressure_systolic', 'mmHg'),
    ('vitals', 'blood_pressure_diastolic', 'mmHg'),
    ('vitals', 'heart_rate', 'bpm'),
    ('vitals', 'weight', 'kg'),
    ('vitals', 'bmi', 'kg/m2'),
    ('laboratory', 'cholesterol_total', 'mg/dL'),
    ('laboratory', 'ldl_cholesterol', 'mg/dL'),
    ('laboratory', 'hdl_cholesterol', 'mg/dL')
) AS obs(category, code, unit)
WHERE ed.enc_seq = 1 OR obs.code NOT IN ('cholesterol_total', 'ldl_cholesterol', 'hdl_cholesterol');

-- Create diagnoses
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, 
        e.patient_id,
        (hashtext(e.patient_id::text) % 100) as patient_var
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-3456%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO diagnoses (id, patient_id, encounter_id, code, description, clinical_status, recorded_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    patient_id,
    encounter_id,
    CASE WHEN patient_var % 10 <= 7 THEN 'I10' ELSE 'I15' END,
    CASE WHEN patient_var % 10 <= 7 THEN 'Essential (primary) hypertension' ELSE 'Secondary hypertension' END,
    'active',
    NOW() - INTERVAL '8 months',
    NOW(),
    NOW()
FROM first_encounters;

-- Add complications
WITH recent_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, 
        e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-3456%'
    ORDER BY e.patient_id, e.start_at DESC
)
INSERT INTO diagnoses (id, patient_id, encounter_id, code, description, clinical_status, recorded_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    patient_id,
    encounter_id,
    'I11',
    'Hypertensive heart disease',
    'active',
    NOW() - INTERVAL '3 weeks',
    NOW(),
    NOW()
FROM recent_encounters
WHERE patient_num % 6 = 0;

-- Create medications
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, 
        e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-3456%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    patient_id,
    encounter_id,
    CASE 
        WHEN patient_num % 3 = 0 THEN 'Lisinopril'
        WHEN patient_num % 3 = 1 THEN 'Metoprolol'
        ELSE 'Amlodipine'
    END,
    CASE 
        WHEN patient_num % 3 = 0 THEN '10'
        WHEN patient_num % 3 = 1 THEN '50'
        ELSE '5'
    END,
    'mg',
    CASE WHEN patient_num % 3 = 1 THEN 'twice_daily' ELSE 'once_daily' END,
    'oral',
    NOW() - INTERVAL '8 months',
    NOW(),
    NOW()
FROM first_encounters;

-- Add diuretics for some patients
WITH follow_up_encounters AS (
    SELECT e.id as encounter_id, e.patient_id,
           ROW_NUMBER() OVER (PARTITION BY e.patient_id ORDER BY e.start_at) as enc_num
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-3456%'
),
second_encounters AS (
    SELECT encounter_id, patient_id,
           ROW_NUMBER() OVER (ORDER BY patient_id) as patient_num
    FROM follow_up_encounters WHERE enc_num = 2
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    patient_id,
    encounter_id,
    'Hydrochlorothiazide',
    '25',
    'mg',
    'once_daily',
    'oral',
    NOW() - INTERVAL '4 months',
    NOW(),
    NOW()
FROM second_encounters
WHERE patient_num % 5 = 0;

-- Display summary
SELECT 
    'Hypertension Patients' as category,
    COUNT(DISTINCT p.id) as patients,
    COUNT(DISTINCT e.id) as encounters,
    COUNT(DISTINCT o.id) as observations,
    COUNT(DISTINCT d.id) as diagnoses,
    COUNT(DISTINCT m.id) as medications
FROM patients p
LEFT JOIN encounters e ON p.id = e.patient_id
LEFT JOIN observations o ON p.id = o.patient_id
LEFT JOIN diagnoses d ON p.id = d.patient_id
LEFT JOIN medications m ON p.id = m.patient_id
WHERE p.abha_id LIKE '91-3456%';
