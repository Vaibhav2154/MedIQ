-- Seed Users for Identity Service
-- This script creates users across all roles: doctors, researchers, hospital admins, regulators, and patients
-- Note: Passwords are hashed using bcrypt. The plain password for all users is "Password123!"
-- Hash generated using: bcrypt.hashpw("Password123!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

-- Clear existing users (optional, comment out if you want to keep existing data)
-- TRUNCATE TABLE users CASCADE;

-- Insert Doctors
INSERT INTO users (id, email, role, password_hash, created_at, updated_at) VALUES
    (gen_random_uuid(), 'dr.sharma@apollo.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.patel@aiims.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.kumar@fortis.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.singh@max.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.reddy@manipal.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.mehta@medanta.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.gupta@apollo.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.verma@aiims.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.joshi@fortis.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.rao@max.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.nair@manipal.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.iyer@medanta.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.desai@apollo.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.chopra@aiims.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'dr.malhotra@fortis.com', 'doctor', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW());

-- Insert Researchers
INSERT INTO users (id, email, role, password_hash, created_at, updated_at) VALUES
    (gen_random_uuid(), 'researcher.agarwal@icmr.gov.in', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'researcher.bansal@nih.gov.in', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'researcher.kapoor@tmc.gov.in', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'researcher.saxena@icmr.gov.in', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'researcher.mishra@nih.gov.in', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'researcher.pandey@tmc.gov.in', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'researcher.trivedi@icmr.gov.in', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'researcher.bhatt@nih.gov.in', 'researcher', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW());

-- Insert Hospital Admins
INSERT INTO users (id, email, role, password_hash, created_at, updated_at) VALUES
    (gen_random_uuid(), 'admin@apollo.com', 'hospital_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'admin@aiims.com', 'hospital_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'admin@fortis.com', 'hospital_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'admin@max.com', 'hospital_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'admin@manipal.com', 'hospital_admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW());

-- Insert Regulators
INSERT INTO users (id, email, role, password_hash, created_at, updated_at) VALUES
    (gen_random_uuid(), 'regulator@mohfw.gov.in', 'regulator', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'regulator@nha.gov.in', 'regulator', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW()),
    (gen_random_uuid(), 'compliance@mohfw.gov.in', 'regulator', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIeWJ3o6qW', NOW(), NOW());

-- Display inserted users by role
SELECT role, COUNT(*) as count FROM users GROUP BY role ORDER BY role;
