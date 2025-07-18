-- 02_load_staging.sql
USE InsurancePrediction;
GO

-- Clear out old staging data
TRUNCATE TABLE staging.insurance_raw;
GO

-- NOTE: Raw CSV load is handled by Python (load_staging.py)
PRINT 'Staging load: please run load_staging.py to ingest the CSV';
GO

