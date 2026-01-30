-- Seed Cardiovascular Disease Medical Data (Optimized for 125 patients)
-- Uses generate_series and CTEs for efficient bulk inserts

-- Create encounters (3 per patient = 375 total)
WITH org AS (
    SELECT id as org_id FROM organizations WHERE name = 'Medanta - The Medicity' LIMIT 1
),
patient_list AS (
    SELECT id as patient_id FROM patients WHERE abha_id LIKE '91-4567%'
),
encounter_types AS (
    SELECT * FROM (VALUES 
        (1, 'outpatient', 'Chest pain and shortness of breath', '1 year', '1.5 hours'),
        (2, 'outpatient', 'Cardiology follow-up', '6 months', '1 hour'),
        (3, 'outpatient', 'Routine cardiac monitoring', '1 month', '45 minutes')
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
    WHERE p.abha_id LIKE '91-4567%'
)
INSERT INTO observations (id, patient_id, encounter_id, category, code, value, unit, effective_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), ed.patient_id, ed.encounter_id, obs.category, obs.code,
    CASE obs.code
        WHEN 'blood_pressure_systolic' THEN (145 - (ed.enc_seq * 8) + (ed.patient_var % 12))::text
        WHEN 'blood_pressure_diastolic' THEN (90 - (ed.enc_seq * 4) + (ed.patient_var % 8))::text
        WHEN 'heart_rate' THEN (85 - (ed.enc_seq * 5) + (ed.patient_var % 10))::text
        WHEN 'troponin_i' THEN (0.05 + ((ed.patient_var % 10) * 0.01))::text
        WHEN 'cholesterol_total' THEN (240 - (ed.enc_seq * 30) + (ed.patient_var % 20))::text
        WHEN 'ldl_cholesterol' THEN (160 - (ed.enc_seq * 25) + (ed.patient_var % 15))::text
        WHEN 'hdl_cholesterol' THEN (38 - (ed.patient_var % 5))::text
        WHEN 'triglycerides' THEN (180 - (ed.enc_seq * 20) + (ed.patient_var % 15))::text
        WHEN 'ejection_fraction' THEN (50 + (ed.enc_seq * 2) - (ed.patient_var % 8))::text
        WHEN 'ecg' THEN 'ST-segment changes noted'
    END,
    obs.unit, ed.start_at, NOW(), NOW()
FROM encounter_data ed
CROSS JOIN (VALUES 
    ('vitals', 'blood_pressure_systolic', 'mmHg'),
    ('vitals', 'blood_pressure_diastolic', 'mmHg'),
    ('vitals', 'heart_rate', 'bpm'),
    ('laboratory', 'troponin_i', 'ng/mL'),
    ('laboratory', 'cholesterol_total', 'mg/dL'),
    ('laboratory', 'ldl_cholesterol', 'mg/dL'),
    ('laboratory', 'hdl_cholesterol', 'mg/dL'),
    ('laboratory', 'triglycerides', 'mg/dL'),
    ('imaging', 'ejection_fraction', '%'),
    ('imaging', 'ecg', '')
) AS obs(category, code, unit)
WHERE ed.enc_seq = 1 OR obs.category != 'imaging';

-- Create diagnoses
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-4567%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO diagnoses (id, patient_id, encounter_id, code, description, clinical_status, recorded_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), patient_id, encounter_id,
    CASE 
        WHEN patient_num % 3 = 0 THEN 'I25.10'
        WHEN patient_num % 3 = 1 THEN 'I50.9'
        ELSE 'I48.91'
    END,
    CASE 
        WHEN patient_num % 3 = 0 THEN 'Atherosclerotic heart disease of native coronary artery'
        WHEN patient_num % 3 = 1 THEN 'Heart failure, unspecified'
        ELSE 'Unspecified atrial fibrillation'
    END,
    'active', NOW() - INTERVAL '1 year', NOW(), NOW()
FROM first_encounters;

-- Create medications (3 per patient)
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, e.patient_id
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-4567%'
    ORDER BY e.patient_id, e.start_at
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), fe.patient_id, fe.encounter_id, med.name, med.dose, med.unit, med.frequency, med.route,
    NOW() - INTERVAL '1 year', NOW(), NOW()
FROM first_encounters fe
CROSS JOIN (VALUES 
    ('Atorvastatin', '40', 'mg', 'once_daily', 'oral'),
    ('Aspirin', '81', 'mg', 'once_daily', 'oral'),
    ('Carvedilol', '25', 'mg', 'twice_daily', 'oral')
) AS med(name, dose, unit, frequency, route);

-- Add ACE inhibitors for heart failure patients
WITH first_encounters AS (
    SELECT DISTINCT ON (e.patient_id) 
        e.id as encounter_id, e.patient_id,
        ROW_NUMBER() OVER (ORDER BY e.patient_id) as patient_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-4567%'
    ORDER BY e.patient_id, e.start_at
),
follow_up AS (
    SELECT e.id as encounter_id, e.patient_id,
           ROW_NUMBER() OVER (PARTITION BY e.patient_id ORDER BY e.start_at) as enc_num
    FROM encounters e JOIN patients p ON e.patient_id = p.id
    WHERE p.abha_id LIKE '91-4567%'
)
INSERT INTO medications (id, patient_id, encounter_id, name, dose, unit, frequency, route, start_at, created_at, updated_at)
SELECT 
    gen_random_uuid(), fu.patient_id, fu.encounter_id,
    CASE WHEN fe.patient_num % 3 = 1 THEN 'Enalapril' ELSE 'Warfarin' END,
    CASE WHEN fe.patient_num % 3 = 1 THEN '10' ELSE '5' END,
    'mg',
    CASE WHEN fe.patient_num % 3 = 1 THEN 'twice_daily' ELSE 'once_daily' END,
    'oral', NOW() - INTERVAL '6 months', NOW(), NOW()
FROM follow_up fu
JOIN first_encounters fe ON fu.patient_id = fe.patient_id
WHERE fu.enc_num = 2 AND (fe.patient_num % 3 = 1 OR fe.patient_num % 3 = 2);

-- Display summary
SELECT 
    'Cardiovascular Patients' as category,
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
WHERE p.abha_id LIKE '91-4567%';
