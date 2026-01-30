-- Clear all consent data from Consent Ingestion database
-- This script safely deletes all consents and consent versions

-- Disable foreign key checks temporarily (if needed)
SET session_replication_role = 'replica';

-- Delete consent versions first (child table)
DELETE FROM consent_versions;

-- Delete consents (parent table)
DELETE FROM consents;

-- Re-enable foreign key checks
SET session_replication_role = 'origin';

-- Display summary
SELECT 
    'Consent Versions' as table_name,
    COUNT(*) as remaining_records
FROM consent_versions
UNION ALL
SELECT 
    'Consents',
    COUNT(*)
FROM consents;

-- Verify deletion
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM consents) = 0 
         AND (SELECT COUNT(*) FROM consent_versions) = 0 
        THEN '✓ All consent data cleared successfully'
        ELSE '✗ Some records remain'
    END as status;
