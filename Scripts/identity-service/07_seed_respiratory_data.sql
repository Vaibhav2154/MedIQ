-- Seed Respiratory Disease Medical Data (Optimized for 125 patients)
-- Uses generate_series and CTEs for efficient bulk inserts

-- Create encounters (3 per patient = 375 total)
WITH org AS (
    SELECT id as org_id FROM organizations WHERE name = 'Max Healthcare' LIMIT 1
),
patient_list AS (
    SELECT id as patient_id FROM patients WHERE abha_id LIKE '91-5678%'
),
encounter_types AS (
    SELECT * FROM (VALUES 
        (1, 'outpatient', 'Persistent cough and breathing difficulty', '10 months', '1 hour'),
        (2, 'outpatient', 'Respiratory follow-up', '5 months', '45 minutes'),
        (3, 'outpatient', 'Routine pulmonary assessment', '2 weeks', '30 minutes')
    ) AS t(enc_num, enc_type, reason, time_ago, duration)
)
INSERT INTO encounters (id, patient_id, organization_id, encounter_type, reason, start_at, end_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), p.patient_id, o.org_id, e.enc_type, e.reason,
    NOW() - e.time_ago::interval,
    NOW() - e.time_ago::interval + e.duration::interval,
    NOW(), NOW()
FROM patient_list p CROSS JOIN encounter_types e CROSS JOIN org o;

-- Create observations
WITH encounter_data AS (
    SELECT e.id as encounter_id, e.patient_id, e.start_at,
           ROW_NUMBER() OVER (PARTITION BY e.patient_id ORDER BY e.start_at) as enc_seq,
           (hashtext(e.patient_id::text) % 100) as patient_var
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-5678%'
)
INSERT INTO observations (id, patient_id, encounter_id, category, code, value, unit, effective_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), ed.patient_id, ed.encounter_id, obs.category, obs.code,
    CASE obs.code
        WHEN 'oxygen_saturation' THEN (92 + (ed.enc_seq * 1) - (ed.patient_var % 5))::text
        WHEN 'respiratory_rate' THEN (20 - ed.enc_seq + (ed.patient_var % 6))::text
        WHEN 'heart_rate' THEN (85 - (ed.enc_seq * 3) + (ed.patient_var % 8))::text
        WHEN 'fev1' THEN (65 + (ed.enc_seq * 2) - (ed.patient_var % 8))::text
        WHEN 'fvc' THEN (70 + (ed.enc_seq * 1) - (ed.patient_var % 6))::text
        WHEN 'fev1_fvc_ratio' THEN (0.65 + (ed.enc_seq * 0.02))::text
        WHEN 'chest_xray' THEN 'Hyperinflation with flattened diaphragm'
    END,
    obs.unit, ed.start_at, NOW(), NOW()
FROM encounter_data ed
CROSS JOIN (VALUES 
    ('vitals', 'oxygen_saturation', '%'),
    ('vitals', 'respiratory_rate', 'breaths/min'),
    ('vitals', 'heart_rate', 'bpm'),
    ('laboratory', 'fev1', '% predicted'),
    ('laboratory', 'fvc', '% predicted'),
    ('laboratory', 'fev1_fvc_ratio', 'ratio'),
    ('imaging', 'chest_xray', '')
) AS obs(category, code, unit)
WHERE ed.enc_seq = 1 OR obs.category != 'imaging';

-- Create diagnoses
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-5678%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO diagnoses (id, patient_id, encounter_id, code, description, clinical_status, recorded_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), patient_id, encounter_id,
    CASE 
        WHEN patient_num % 3 = 0 THEN 'J45.9'
        WHEN patient_num % 3 = 1 THEN 'J44.9'
        ELSE 'J18.9'
    END,
    CASE 
        WHEN patient_num % 3 = 0 THEN 'Asthma, unspecified'
        WHEN patient_num % 3 = 1 THEN 'Chronic obstructive pulmonary disease, unspecified'
        ELSE 'Pneumonia, unspecified organism'
    END,
    'active', NOW() - INTERVAL '10 months', NOW(), NOW()
FROM first_encounters;

-- Add COPD exacerbations
WITH recent_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-5678%'
    ORDER BY e.patient_id, e.start_at DESC
)
INSERT INTO diagnoses (id, patient_id, encounter_id, code, description, clinical_status, recorded_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), patient_id, encounter_id,
    'J44.1',
    'Chronic obstructive pulmonary disease with acute exacerbation',
    'active', NOW() - INTERVAL '2 weeks', NOW(), NOW()
FROM recent_encounters
WHERE patient_num % 3 = 1 AND patient_num % 9 = 0;

-- Create medications
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-5678%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, end_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), patient_id, encounter_id,
    CASE 
        WHEN patient_num % 3 = 0 THEN 'Fluticasone/Salmeterol'
        WHEN patient_num % 3 = 1 THEN 'Tiotropium'
        ELSE 'Azithromycin'
    END,
    CASE 
        WHEN patient_num % 3 = 0 THEN '250/50'
        WHEN patient_num % 3 = 1 THEN '18'
        ELSE '500'
    END,
    CASE WHEN patient_num % 3 = 2 THEN 'mg' ELSE 'mcg' END,
    CASE WHEN patient_num % 3 = 2 THEN 'once_daily' ELSE 'twice_daily' END,
    CASE WHEN patient_num % 3 = 2 THEN 'oral' ELSE 'inhalation' END,
    NOW() - INTERVAL '10 months',
    CASE WHEN patient_num % 3 = 2 THEN NOW() - INTERVAL '10 months' + INTERVAL '5 days' ELSE NULL END,
    NOW(), NOW()
FROM first_encounters;

-- Add rescue inhalers
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-5678%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), patient_id, encounter_id,
    CASE WHEN patient_num % 3 = 0 THEN 'Albuterol' ELSE 'Formoterol' END,
    CASE WHEN patient_num % 3 = 0 THEN '90' ELSE '12' END,
    'mcg',
    CASE WHEN patient_num % 3 = 0 THEN 'as_needed' ELSE 'twice_daily' END,
    'inhalation',
    NOW() - INTERVAL '10 months', NOW(), NOW()
FROM first_encounters
WHERE patient_num % 3 != 2;

-- Display summary
SELECT 
    'Respiratory Patients' as category,
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
WHERE p.abha_id LIKE '91-5678%';
