# Datasphere object definitions

Definitions exported from the tenant, kept as code. No data, no credentials.

- `csn/` — CSN/JSON exports (*Export to CSN/JSON File*) of the project's objects. They can
  be imported into another space or tenant with *Import → Import Objects from CSN/JSON
  File*. Tenant-internal identifiers (source schema and internal dataset IDs in
  `@DataWarehouse.dataSource.*`) are replaced with placeholders before committing.
- `certs/` — public root CA certificates the tenant trusts for its connections (see
  `docs/decisions.md`).
