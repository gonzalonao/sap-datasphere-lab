-- Datasphere connection user for the Northwind Azure SQL Database.
-- Run as the server admin, connected to database `northwind` (not `master`).
-- Run each block on its own if your client doesn't split on GO.
--
-- Privileges follow SAP's "Prepare Connectivity to Microsoft Azure SQL Database"
-- (replication flows, initial and delta loads). CREATE SEQUENCE isn't granted: it's a
-- schema-scoped permission, and the user already has it as owner of its own schema.

-- Contained user: it exists only in this database, so clients must connect to `northwind`.
CREATE USER dsp_rep WITH PASSWORD = '<set a strong password; keep it in a password manager>';
GO

-- Delta loads create shadow tables, procedures and sequences in a schema named after the user.
CREATE SCHEMA dsp_rep AUTHORIZATION dsp_rep;
GO

GRANT VIEW DATABASE PERFORMANCE STATE TO dsp_rep;   -- metadata access
GRANT SELECT, ALTER ON SCHEMA::dbo TO dsp_rep;      -- read source tables, create triggers
GRANT CREATE TABLE, CREATE PROCEDURE TO dsp_rep;    -- delta replication objects
GO

-- Only for real-time replication of remote tables through an SDI Data Provisioning Agent
-- (MssqlLogReaderAdapter, trigger-based): it also creates a database-level DDL trigger.
-- Without this grant, enabling real-time fails with "Cannot create the trigger
-- '..._DDL_TRIG', because you do not have permission".
GRANT ALTER ANY DATABASE DDL TRIGGER TO dsp_rep;
GO

-- Expect: CONNECT, CREATE PROCEDURE, CREATE TABLE, VIEW DATABASE PERFORMANCE STATE,
-- ALTER ANY DATABASE DDL TRIGGER (class DATABASE) and ALTER, SELECT on schema dbo
-- (class SCHEMA), all GRANT.
SELECT p.class_desc, p.permission_name, p.state_desc, s.name AS schema_name
FROM sys.database_permissions AS p
LEFT JOIN sys.schemas AS s ON p.class = 3 AND p.major_id = s.schema_id
WHERE p.grantee_principal_id = DATABASE_PRINCIPAL_ID('dsp_rep');
