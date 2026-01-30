#!/usr/bin/env python3
"""
Generate Optimized Medical Data SQL Scripts

This script generates SQL files for seeding medical data (encounters, observations, 
diagnoses, medications) for large patient populations using optimized batch inserts.

Usage:
    python generate_medical_data_scripts.py
"""

def generate_diabetes_script():
    """Generate optimized diabetes medical data script"""
    return """-- Seed Diabetes Medical Data (Optimized for 125 patients)
-- Uses CTEs and batch inserts for better performance

DO $$
DECLARE
    org_id uuid;
    base_time timestamp := NOW();
BEGIN
    -- Get organization ID
    SELECT id INTO org_id FROM organizations WHERE name = 'Apollo Hospitals' LIMIT 1;
    
    -- Create encounters for all diabetes patients (3 encounters per patient = 375 total)
    WITH patient_list AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY abha_id) as rn
        FROM patients WHERE abha_id LIKE '91-2345%'
    )
    INSERT INTO encounters (id, patient_id, organization_id, encounter_type, reason, start_at, end_at, created_at, updated_at)
    SELECT 
        gen_random_uuid(),
        id,
        org_id,
        'outpatient',
        CASE 
            WHEN enc_num = 1 THEN 'Routine checkup - elevated blood sugar'
            WHEN enc_num = 2 THEN 'Diabetes follow-up'
            ELSE 'Routine diabetes monitoring'
        END,
        base_time - (CASE WHEN enc_num = 1 THEN INTERVAL '6 months'
                          WHEN enc_num = 2 THEN INTERVAL '3 months'
                          ELSE INTERVAL '2 weeks' END),
        base_time - (CASE WHEN enc_num = 1 THEN INTERVAL '6 months' - INTERVAL '1 hour'
                          WHEN enc_num = 2 THEN INTERVAL '3 months' - INTERVAL '45 minutes'
                          ELSE INTERVAL '2 weeks' - INTERVAL '30 minutes' END),
        base_time,
        base_time
    FROM patient_list
    CROSS JOIN (SELECT 1 as enc_num UNION SELECT 2 UNION SELECT 3) encounters;
    
    -- Create observations (6 per encounter = 2,250 total)
    WITH encounter_data AS (
        SELECT e.id as encounter_id, e.patient_id, e.start_at,
               ROW_NUMBER() OVER (PARTITION BY e.patient_id ORDER BY e.start_at) as enc_seq
        FROM encounters e
        JOIN patients p ON e.patient_id = p.id
        WHERE p.abha_id LIKE '91-2345%'
    )
    INSERT INTO observations (id, patient_id, encounter_id, category, code, value, unit, effective_at, created_at, updated_at)
    SELECT 
        gen_random_uuid(),
        patient_id,
        encounter_id,
        obs.category,
        obs.code,
        obs.value_expr,
        obs.unit,
        start_at,
        base_time,
        base_time
    FROM encounter_data
    CROSS JOIN LATERAL (
        VALUES 
            ('vitals', 'blood_glucose_fasting', (180 - (enc_seq * 15) + (patient_id::text::bit(32)::int % 20))::text, 'mg/dL'),
            ('laboratory', 'hba1c', (7.5 - (enc_seq * 0.3) + ((patient_id::text::bit(32)::int % 10) * 0.1))::text, '%'),
            ('vitals', 'blood_pressure_systolic', (135 - (enc_seq * 5) + (patient_id::text::bit(32)::int % 15))::text, 'mmHg'),
            ('vitals', 'blood_pressure_diastolic', (85 - (enc_seq * 2) + (patient_id::text::bit(32)::int % 8))::text, 'mmHg'),
            ('vitals', 'bmi', (27 - (enc_seq * 0.3) + ((patient_id::text::bit(32)::int % 10) * 0.2))::text, 'kg/m2'),
            ('vitals', 'weight', (75 - (enc_seq * 1) + (patient_id::text::bit(32)::int % 10))::text, 'kg')
    ) AS obs(category, code, value_expr, unit);
    
    -- Create diagnoses (1-2 per patient = ~150 total)
    WITH first_encounters AS (
        SELECT DISTINCT ON (e.patient_id) e.id as encounter_id, e.patient_id,
               (patient_id::text::bit(32)::int % 10) as patient_mod
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
        CASE WHEN patient_mod <= 6 THEN 'E11' ELSE 'E10' END,
        CASE WHEN patient_mod <= 6 THEN 'Type 2 diabetes mellitus' ELSE 'Type 1 diabetes mellitus' END,
        'active',
        base_time - INTERVAL '6 months',
        base_time,
        base_time
    FROM first_encounters;
    
    -- Create medications (1-2 per patient = ~150 total)
    WITH first_encounters AS (
        SELECT DISTINCT ON (e.patient_id) e.id as encounter_id, e.patient_id,
               (patient_id::text::bit(32)::int % 10) as patient_mod
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
        CASE WHEN patient_mod <= 6 THEN 'Metformin' ELSE 'Insulin Glargine' END,
        CASE WHEN patient_mod <= 6 THEN '500' ELSE '20' END,
        CASE WHEN patient_mod <= 6 THEN 'mg' ELSE 'units' END,
        CASE WHEN patient_mod <= 6 THEN 'twice_daily' ELSE 'once_daily' END,
        CASE WHEN patient_mod <= 6 THEN 'oral' ELSE 'subcutaneous' END,
        base_time - INTERVAL '6 months',
        base_time,
        base_time
    FROM first_encounters;
    
END $$;

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
"""

# Generate the script
if __name__ == '__main__':
    print("Generating optimized diabetes medical data script...")
    script = generate_diabetes_script()
    
    with open('../identity-service/04_seed_diabetes_data.sql', 'w') as f:
        f.write(script)
    
    print("✓ Generated 04_seed_diabetes_data.sql")
    print("\nNote: Similar optimization should be applied to other disease category scripts.")
    print("The key optimizations:")
    print("  - Use CTEs to select patients once")
    print("  - CROSS JOIN with VALUES for batch inserts")
    print("  - Avoid procedural loops where possible")
    print("  - Use set-based operations")
