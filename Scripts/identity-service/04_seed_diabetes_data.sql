-- Seed Diabetes Medical Data (Optimized for 125 patients)
-- Uses generate_series and CTEs for efficient bulk inserts

-- Create encounters for all diabetes patients (3 encounters per patient = 375 total)
WITH org AS (
    SELECT id as org_id FROM organizations WHERE name = 'Apollo Hospitals' LIMIT 1
),
patient_list AS (
    SELECT id as patient_id, ROW_NUMBER() OVER (ORDER BY abha_id) as patient_num
    FROM patients WHERE abha_id LIKE '91-2345%'
),
encounter_types AS (
    SELECT * FROM (VALUES 
        (1, 'outpatient', 'Routine checkup - elevated blood sugar', '6 months', '1 hour'),
        (2, 'outpatient', 'Diabetes follow-up', '3 months', '45 minutes'),
        (3, 'outpatient', 'Routine diabetes monitoring', '2 weeks', '30 minutes')
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

-- Create observations (varying by encounter)
WITH encounter_data AS (
    SELECT 
        e.id as encounter_id, 
        e.patient_id, 
        e.start_at,
        ROW_NUMBER() OVER (PARTITION BY e.patient_id ORDER BY e.start_at) as enc_seq,
        (hashtext(e.patient_id::text) % 100) as patient_var
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-2345%'
)
INSERT INTO observations (id, patient_id, encounter_id, category, code, value, unit, effective_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    ed.patient_id,
    ed.encounter_id,
    obs.category,
    obs.code,
    CASE obs.code
        WHEN 'blood_glucose_fasting' THEN (180 - (ed.enc_seq * 15) + (ed.patient_var % 20))::text
        WHEN 'hba1c' THEN (7.5 - (ed.enc_seq * 0.3) + ((ed.patient_var % 10) * 0.1))::text
        WHEN 'blood_pressure_systolic' THEN (135 - (ed.enc_seq * 5) + (ed.patient_var % 15))::text
        WHEN 'blood_pressure_diastolic' THEN (85 - (ed.enc_seq * 2) + (ed.patient_var % 8))::text
        WHEN 'bmi' THEN (27 - (ed.enc_seq * 0.3) + ((ed.patient_var % 10) * 0.2))::text
        WHEN 'weight' THEN (75 - ed.enc_seq + (ed.patient_var % 10))::text
    END,
    obs.unit,
    ed.start_at,
    NOW(),
    NOW()
FROM encounter_data ed
CROSS JOIN (VALUES 
    ('vitals', 'blood_glucose_fasting', 'mg/dL'),
    ('laboratory', 'hba1c', '%'),
    ('vitals', 'blood_pressure_systolic', 'mmHg'),
    ('vitals', 'blood_pressure_diastolic', 'mmHg'),
    ('vitals', 'bmi', 'kg/m2'),
    ('vitals', 'weight', 'kg')
) AS obs(category, code, unit);

-- Create diagnoses (1 per patient at first encounter)
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, 
        e.patient_id,
        (hashtext(e.patient_id::text) % 100) as patient_var
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-2345%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO diagnoses (id, patient_id, encounter_id, code, description, clinical_status, recorded_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    patient_id,
    encounter_id,
    CASE WHEN patient_var % 10 <= 6 THEN 'E11' ELSE 'E10' END,
    CASE WHEN patient_var % 10 <= 6 THEN 'Type 2 diabetes mellitus' ELSE 'Type 1 diabetes mellitus' END,
    'active',
    NOW() - INTERVAL '6 months',
    NOW(),
    NOW()
FROM first_encounters;

-- Add complications for some patients (at recent encounter)
WITH recent_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, 
        e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-2345%'
    ORDER BY e.patient_id, e.start_at DESC
)
INSERT INTO diagnoses (id, patient_id, encounter_id, code, description, clinical_status, recorded_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    patient_id,
    encounter_id,
    CASE 
        WHEN patient_num % 3 = 0 THEN 'E11.9'
        WHEN patient_num % 4 = 0 THEN 'E11.40'
    END,
    CASE 
        WHEN patient_num % 3 = 0 THEN 'Type 2 diabetes mellitus without complications'
        WHEN patient_num % 4 = 0 THEN 'Type 2 diabetes mellitus with diabetic neuropathy'
    END,
    'active',
    NOW() - INTERVAL '2 weeks',
    NOW(),
    NOW()
FROM recent_encounters
WHERE patient_num % 3 = 0 OR patient_num % 4 = 0;

-- Create medications (1 per patient at first encounter)
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, 
        e.patient_id,
        (hashtext(e.patient_id::text) % 100) as patient_var
    FROM encounters e
    JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-2345%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, created_at, updated_at)
SELECT 
    gen_random_uuid(),
    patient_id,
    encounter_id,
    CASE WHEN patient_var % 10 <= 6 THEN 'Metformin' ELSE 'Insulin Glargine' END,
    CASE WHEN patient_var % 10 <= 6 THEN '500' ELSE '20' END,
    CASE WHEN patient_var % 10 <= 6 THEN 'mg' ELSE 'units' END,
    CASE WHEN patient_var % 10 <= 6 THEN 'twice_daily' ELSE 'once_daily' END,
    CASE WHEN patient_var % 10 <= 6 THEN 'oral' ELSE 'subcutaneous' END,
    NOW() - INTERVAL '6 months',
    NOW(),
    NOW()
FROM first_encounters;

-- Display summary
SELECT 
    'Diabetes Patients' as category,
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
WHERE p.abha_id LIKE '91-2345%';
