-- 03_load_cleaned.sql
-- Transform raw staging data into a cleaned, analyzable production table.
-- Idempotent: truncates before insert so it can be re-run safely.

USE InsurancePrediction;  
GO

-- 1) Clear out old production data to prevent duplicates on re-runs
TRUNCATE TABLE production.insurance_clean;  
GO

-- 2) Populate production.insurance_clean from raw staging table
INSERT INTO production.insurance_clean
(
  age,
  sex,
  bmi,
  children,
  smoker,    -- convert yes/no to bit
  region,
  charges
)
SELECT
  age,
  sex,
  bmi,
  children,
  CASE WHEN LOWER(smoker) = 'yes' THEN 1 ELSE 0 END AS smoker,
  region,
  charges
FROM staging.insurance_raw;  
GO

-- 3) Quick row-count check
SELECT 
  COUNT(*) AS raw_cnt,
  (SELECT COUNT(*) FROM production.insurance_clean) AS clean_cnt
FROM staging.insurance_raw;  
GO