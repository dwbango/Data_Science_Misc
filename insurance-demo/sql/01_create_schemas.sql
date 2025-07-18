-- 01_create_schemas.sql
-- Ensure that we have two separate schemas: staging for raw loads, production for
-- cleaned & modeled data.

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'staging')
    EXEC('CREATE SCHEMA staging');    -- create staging schema if missing

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'production')
    EXEC('CREATE SCHEMA production'); -- create production schema if missing
GO