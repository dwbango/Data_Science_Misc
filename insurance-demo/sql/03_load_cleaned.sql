USE InsurancePrediction;
GO

-- Clear out old data so we don’t duplicate on re-runs
TRUNCATE TABLE production.insurance_clean;
GO

-- Now insert fresh, clean data
INSERT INTO production.insurance_clean
( age, sex, bmi, children, smoker, region, charges )
SELECT
  age,
  sex,
  bmi,
  children,
  CASE WHEN LOWER(smoker) = 'yes' THEN 1 ELSE 0 END,
  region,
  charges
FROM staging.insurance_raw;
GO

