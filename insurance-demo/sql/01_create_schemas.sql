-- 01_create_schemas.sql
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'staging')
  EXEC('CREATE SCHEMA staging');
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'production')
  EXEC('CREATE SCHEMA production');
GO

