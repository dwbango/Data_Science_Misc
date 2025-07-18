-- 02_load_staging.sql
-- Prepare the staging table for a fresh raw-data load.
-- Raw CSV ingestion is handled by load_staging.py (Python), so here we just
-- truncate the old data and prompt the user.

USE InsurancePrediction;  
GO

-- Remove any existing rows in staging.insurance_raw to avoid duplicates
TRUNCATE TABLE staging.insurance_raw;  
GO

-- Informational message: actual data load happens in Python
PRINT 'Staging load: please run src/load_staging.py to ingest the CSV';  
GO