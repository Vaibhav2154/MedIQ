-- Seed Cancer Medical Data (Optimized for 125 patients)
-- Uses generate_series and CTEs for efficient bulk inserts

-- Create encounters (3 per patient = 375 total)
WITH org AS (
    SELECT id as org_id FROM organizations WHERE name = 'Tata Memorial Centre' LIMIT 1
),
patient_list AS (
    SELECT id as patient_id FROM patients WHERE abha_id LIKE '91-6789%'
),
encounter_types AS (
    SELECT * FROM (VALUES 
        (1, 'outpatient', 'Abnormal screening results - biopsy consultation', '9 months', '2 hours'),
        (2, 'inpatient', 'Chemotherapy cycle 1', '6 months', '4 hours'),
        (3, 'outpatient', 'Post-treatment imaging and assessment', '3 months', '1 hour')
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
           ROW_NUMBER() OVER (ORDER BY e.patient_id, e.start_at) as global_num,
           (hashtext(e.patient_id::text) % 100) as patient_var
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-6789%'
)
INSERT INTO observations (id, patient_id, encounter_id, category, code, value, unit, effective_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), ed.patient_id, ed.encounter_id, obs.category, obs.code,
    CASE obs.code
        WHEN 'weight' THEN (65 - ed.enc_seq + (ed.patient_var % 10))::text
        WHEN 'performance_status' THEN (ed.patient_var % 3)::text
        WHEN 'hemoglobin' THEN (11 - (ed.enc_seq * 0.3) + ((ed.patient_var % 10) * 0.1))::text
        WHEN 'wbc_count' THEN (6 - (ed.enc_seq * 0.5) + ((ed.patient_var % 10) * 0.2))::text
        WHEN 'platelet_count' THEN (200 - (ed.enc_seq * 20) + (ed.patient_var % 30))::text
        WHEN 'biopsy_result' THEN 'Malignant neoplasm confirmed'
        WHEN 'ca_15_3' THEN (30 - (ed.enc_seq * 5) + (ed.patient_var % 10))::text
        WHEN 'cea' THEN (8 - (ed.enc_seq * 2) + (ed.patient_var % 5))::text
        WHEN 'psa' THEN (15 - (ed.enc_seq * 3) + (ed.patient_var % 8))::text
        WHEN 'ca_125' THEN (50 - (ed.enc_seq * 10) + (ed.patient_var % 15))::text
        WHEN 'ct_scan' THEN 'Partial response - tumor size reduced by 40%'
    END,
    obs.unit, ed.start_at, NOW(), NOW()
FROM encounter_data ed
CROSS JOIN (VALUES 
    ('vitals', 'weight', 'kg'),
    ('vitals', 'performance_status', 'ECOG'),
    ('laboratory', 'hemoglobin', 'g/dL'),
    ('laboratory', 'wbc_count', '10^9/L'),
    ('laboratory', 'platelet_count', '10^9/L'),
    ('pathology', 'biopsy_result', ''),
    ('laboratory', 'ca_15_3', 'U/mL'),
    ('laboratory', 'cea', 'ng/mL'),
    ('laboratory', 'psa', 'ng/mL'),
    ('laboratory', 'ca_125', 'U/mL'),
    ('imaging', 'ct_scan', '')
) AS obs(category, code, unit)
WHERE 
    (ed.enc_seq = 1 AND obs.code IN ('weight', 'performance_status', 'hemoglobin', 'wbc_count', 'platelet_count', 'biopsy_result'))
    OR (ed.enc_seq = 1 AND ed.global_num % 5 = 0 AND obs.code = 'ca_15_3')
    OR (ed.enc_seq = 1 AND ed.global_num % 5 IN (1,2) AND obs.code = 'cea')
    OR (ed.enc_seq = 1 AND ed.global_num % 5 = 3 AND obs.code = 'psa')
    OR (ed.enc_seq = 1 AND ed.global_num % 5 = 4 AND obs.code = 'ca_125')
    OR (ed.enc_seq = 2 AND obs.code IN ('weight', 'hemoglobin', 'wbc_count', 'platelet_count'))
    OR (ed.enc_seq = 3 AND obs.code IN ('weight', 'hemoglobin', 'ct_scan'))
    OR (ed.enc_seq = 3 AND ed.global_num % 5 = 0 AND obs.code = 'ca_15_3')
    OR (ed.enc_seq = 3 AND ed.global_num % 5 IN (1,2) AND obs.code = 'cea')
    OR (ed.enc_seq = 3 AND ed.global_num % 5 = 3 AND obs.code = 'psa')
    OR (ed.enc_seq = 3 AND ed.global_num % 5 = 4 AND obs.code = 'ca_125');

-- Create diagnoses
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-6789%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO diagnoses (id, patient_id, encounter_id, code, description, clinical_status, recorded_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), patient_id, encounter_id,
    CASE 
        WHEN patient_num % 5 = 0 THEN 'C50.9'
        WHEN patient_num % 5 = 1 THEN 'C34.9'
        WHEN patient_num % 5 = 2 THEN 'C18.9'
        WHEN patient_num % 5 = 3 THEN 'C61'
        ELSE 'C56.9'
    END,
    CASE 
        WHEN patient_num % 5 = 0 THEN 'Malignant neoplasm of breast, unspecified'
        WHEN patient_num % 5 = 1 THEN 'Malignant neoplasm of bronchus and lung, unspecified'
        WHEN patient_num % 5 = 2 THEN 'Malignant neoplasm of colon, unspecified'
        WHEN patient_num % 5 = 3 THEN 'Malignant neoplasm of prostate'
        ELSE 'Malignant neoplasm of ovary, unspecified'
    END,
    'active', NOW() - INTERVAL '9 months', NOW(), NOW()
FROM first_encounters;

-- Create chemotherapy medications
WITH chemo_encounters AS (
    SELECT e.id as encounter_id, e.patient_id,
           ROW_NUMBER() OVER (PARTITION BY e.patient_id ORDER BY e.start_at) as enc_num,
           ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-6789%'
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), ce.patient_id, ce.encounter_id, med.name, med.dose, med.unit, med.frequency, med.route,
    NOW() - INTERVAL '6 months', NOW(), NOW()
FROM chemo_encounters ce
CROSS JOIN LATERAL (
    SELECT * FROM (VALUES 
        ('Doxorubicin', '60', 'mg/m2', 'q21days', 'intravenous'),
        ('Cyclophosphamide', '600', 'mg/m2', 'q21days', 'intravenous')
    ) AS t(name, dose, unit, frequency, route)
    WHERE ce.patient_num % 5 = 0 AND ce.enc_num = 2
    UNION ALL
    SELECT * FROM (VALUES 
        ('Carboplatin', 'AUC 6', 'mg', 'q21days', 'intravenous'),
        ('Paclitaxel', '200', 'mg/m2', 'q21days', 'intravenous')
    ) AS t(name, dose, unit, frequency, route)
    WHERE ce.patient_num % 5 = 1 AND ce.enc_num = 2
    UNION ALL
    SELECT * FROM (VALUES 
        ('Oxaliplatin', '85', 'mg/m2', 'q14days', 'intravenous'),
        ('5-Fluorouracil', '400', 'mg/m2', 'q14days', 'intravenous')
    ) AS t(name, dose, unit, frequency, route)
    WHERE ce.patient_num % 5 = 2 AND ce.enc_num = 2
    UNION ALL
    SELECT * FROM (VALUES 
        ('Cisplatin', '75', 'mg/m2', 'q21days', 'intravenous')
    ) AS t(name, dose, unit, frequency, route)
    WHERE ce.patient_num % 5 IN (3, 4) AND ce.enc_num = 2
) AS med;

-- Add supportive care medications
WITH chemo_encounters AS (
    SELECT e.id as encounter_id, e.patient_id,
           ROW_NUMBER() OVER (PARTITION BY e.patient_id ORDER BY e.start_at) as enc_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-6789%'
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), patient_id, encounter_id, med.name, med.dose, med.unit, med.frequency, med.route,
    NOW() - INTERVAL '6 months', NOW(), NOW()
FROM chemo_encounters
CROSS JOIN (VALUES 
    ('Ondansetron', '8', 'mg', 'three_times_daily', 'oral'),
    ('Dexamethasone', '4', 'mg', 'twice_daily', 'oral')
) AS med(name, dose, unit, frequency, route)
WHERE enc_num = 2;

-- Display summary
SELECT 
    'Cancer Patients' as category,
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
WHERE p.abha_id LIKE '91-6789%';
