# Build log

What happened while building, in order, including what went wrong and how it was fixed.
Phase A's record is still in [`units/01-space-model-remote/`](../units/01-space-model-remote/README.md)
and is folded in here in Phase I. Per-phase results are in [`phases/`](phases/README.md).

## Phase B — Ingestion & integration (2026-10-21 → 2026-10-27)

### Connections and the Azure source

The connection wizard offered 37 connection types. Its feature filters combine with OR, not
AND, so ticking two features lists the union. Azure SQL's remote-table feature was flagged
*Disconnected Agent* from the start: remote tables on this source need a Data Provisioning
Agent, while replication and data flows only need Datasphere's egress IPs in the database
firewall.

Getting the free Azure SQL Database took three tries. A personal Microsoft account first needs a
subscription of its own; the free offer then wasn't available in the first region tried, and a
new server in another region worked with default settings. The least-privilege login `dsp_rep`
is a contained database user, so client tools only connect once the database name is set in the
connection profile. `CREATE SEQUENCE` isn't a database-level permission (the schema owner has it
already), so the first grant script failed and was corrected.

The serverless database pauses when idle. The first connection after a pause fails with
*database not currently available*, and Datasphere's *Validate* fails the same way; a retry a
minute later succeeds.

The SAP S/4HANA Cloud sandbox API was reachable through a Generic OData connection with an
API-key header. It validated for remote tables and data flows but not replication flows: the
features follow the connection type, not the system behind it.

### Remote tables and the DP Agent

The agent installed cleanly but its Windows service failed to log on under a passwordless
personal account (error 1069); running it as Local System fixed that for the lab. Its
configuration menu differed from the documentation. Once registered, the SQL Server log reader
adapter enabled remote tables on `CN_NW_AZSQL`.

*Remote Queries* showed what reached SQL Server: `TOP`, `COUNT_BIG` and `WHERE` with bound
parameters, about 0.65 s per statement. On the OData sandbox the count wasn't pushed, which is
why previews read `1000 / n`, and a view's aggregation ran in HANA over every fetched row. A
second statistics object first failed with *already exists*: the page was stale, and after a
refresh it replaced the old one as documented.

Real-time replication first failed because SAP's trigger-based capture also creates a
database-level DDL trigger, which needs `ALTER ANY DATABASE DDL TRIGGER`. That grant isn't in
the replication-flow privilege list and was added to the script. Stopping the agent's Windows
service didn't stop changes arriving, because the agent process kept running; ending the process
did, and the changes queued at the source were applied after the restart.

### Replication flow with delta

`RF_NW_AZSQL` replicated eight tables. The editor skipped unsupported `image`/`ntext` columns on
its own. The first run showed objects as *Retrying* for several minutes after the data had
arrived: that's the first delta pass waiting, not an error. The Azure query editor ran only one
statement of a multi-statement paste, so test changes were run one statement at a time. A
deleted shipper stayed in the delta table with change type `D` and disappeared from the active
records. The flow also writes change type `L` for initial-load rows, a code the documentation
doesn't list.

### Transformation flow

The first run of `TF_NW_SALES` failed with *value not allowed* on `REVENUE`: the target table
had been created as `Decimal(5,2)` although the calculated column was `Decimal(15,2)`. The editor
re-derives a calculated column's type from its expression on every edit.

The revenue total then came out at 1,265,789.88 instead of 1,265,792.64. The source's `Discount`
column is `real`, so HANA evaluated the whole expression in single precision. Converting the
discount with `TO_DECIMAL(…, 4, 2)` gave 1,265,796.29: HANA's `TO_DECIMAL` truncates, and the
eight odd discounts (0.01–0.06) are stored just below their value. An independent recalculation
from the CSV reproduced both wrong totals to the cent. `ROUND(TO_DECIMAL("Discount", 10, 6), 2)`
restored the reference total. SQL Server's own check had shown the right number all along,
because its `CAST` rounds.

The delta tests confirmed the documented rules: a changed line was the only record processed,
while a change to an order header (not the delta source) left the target unchanged until the
watermark was reset, at one point leaving a single order with two different customers.

### Outbound to Azure Data Lake

The tenant has no *Tenant Configuration* or *Capacities Monitoring* page for this user, so no
premium outbound capacity could be assigned and the ADLS replication flow wasn't built. The
setup and cost model are in the [decision log](decisions.md).

### Data flow, Open SQL schema, Data Marketplace

The data flow source listed the unsupported `Photo` and `Notes` columns, unlike the replication
flow editor, so they were removed in a projection. A new target table only offers a write mode
after *Create and Deploy Table*, and its technical name defaults from the business name. Run
metrics appeared minutes after the run, without a source count.

The database user `NW_LAB#ETL` was created. The browser-based database explorer asked for an
identity provider and rejected the author's credentials under both options, so the external
write moves to the Python loader on the author's laptop.

From about 1,600 free Marketplace products, a country reference set was installed in one step
as a remote table with 244 rows.
