-- Seed Organizations for Identity Service
-- This script creates hospitals, research organizations, and government entities

-- Clear existing organizations (optional, comment out if you want to keep existing data)
-- TRUNCATE TABLE organizations CASCADE;

-- Insert Hospitals
INSERT INTO organizations (id, name, org_type, created_at, updated_at) VALUES
    (gen_random_uuid(), 'Apollo Hospitals', 'hospital', NOW(), NOW()),
    (gen_random_uuid(), 'AIIMS Delhi', 'hospital', NOW(), NOW()),
    (gen_random_uuid(), 'Fortis Healthcare', 'hospital', NOW(), NOW()),
    (gen_random_uuid(), 'Max Healthcare', 'hospital', NOW(), NOW()),
    (gen_random_uuid(), 'Manipal Hospitals', 'hospital', NOW(), NOW()),
    (gen_random_uuid(), 'Medanta - The Medicity', 'hospital', NOW(), NOW());

-- Insert Research Organizations
INSERT INTO organizations (id, name, org_type, created_at, updated_at) VALUES
    (gen_random_uuid(), 'Indian Council of Medical Research', 'research_org', NOW(), NOW()),
    (gen_random_uuid(), 'National Institute of Health', 'research_org', NOW(), NOW()),
    (gen_random_uuid(), 'Tata Memorial Centre', 'research_org', NOW(), NOW());

-- Insert Government Entities
INSERT INTO organizations (id, name, org_type, created_at, updated_at) VALUES
    (gen_random_uuid(), 'Ministry of Health and Family Welfare', 'government', NOW(), NOW()),
    (gen_random_uuid(), 'National Health Authority', 'government', NOW(), NOW());

-- Display inserted organizations
SELECT id, name, org_type FROM organizations ORDER BY org_type, name;
