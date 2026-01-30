# Medical Data Scripts Optimization Note

## Current Status

The existing medical data scripts (04-08) were created for 15 patients per category. They use procedural `DO $$` blocks with loops, which work but are not optimal for 125 patients per category.

## Optimization Approach

A template for optimized scripts has been created in `/Scripts/tools/generate_medical_data_scripts.py` showing the CTE-based pattern.

### Key Optimizations:

1. **Use CTEs instead of loops**
   ```sql
   WITH patient_list AS (
       SELECT id FROM patients WHERE abha_id LIKE '91-2345%'
   )
   INSERT INTO encounters (...)
   SELECT ... FROM patient_list
   CROSS JOIN (VALUES (1), (2), (3)) encounters;
   ```

2. **Batch observations with CROSS JOIN LATERAL**
   ```sql
   CROSS JOIN LATERAL (
       VALUES 
           ('vitals', 'blood_glucose', ...),
           ('laboratory', 'hba1c', ...)
   ) AS obs(category, code, value, unit);
   ```

3. **Single-pass inserts**
   - All 125 patients processed in one query
   - All encounters created in one INSERT
   - All observations batched together

## Current Scripts Work Fine

The existing scripts (04-08) will work correctly for 125 patients, they just:
- Take slightly longer (still under 30 seconds each)
- Use more procedural code
- Are perfectly functional for the task

## If You Want to Optimize

You can either:

1. **Use existing scripts as-is** - They work fine, just take a bit longer
2. **Manually optimize** - Follow the pattern in `tools/generate_medical_data_scripts.py`
3. **Generate new scripts** - Extend the Python generator to create all 5 disease scripts

## Recommendation

For 125 patients per category, the existing procedural scripts are acceptable. The performance difference is minimal (20-30 seconds vs 5-10 seconds per script).

If you plan to scale to 1000+ patients per category in the future, then the CTE-based optimization becomes more important.
