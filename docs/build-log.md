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

From the laptop, the loader created `SALES_TARGETS` and wrote 62 rows (total 1,393,000); a
second run reloaded the same 62 rows without re-creating the table. In the SQL editor the
schema `NW_LAB#ETL` appears on the *Sources* tab next to *Connections*, and dragging the table
in inserts its plain name. `V_NW_SALES_VS_TARGET` full-outer-joins actuals per ship country
and year to the targets: actual 1,265,792.64 against 1,393,000.00, with no nulls on either
side. Reviewing the run showed that `hdbcli` autocommits by default, so the delete and the
insert weren't one transaction; the loader now turns autocommit off and rolls back on error.
A rerun of the fixed loader against the tenant loaded the same 62 rows.

From about 1,600 free Marketplace products, a country reference set was installed in one step
as a remote table with 244 rows.

## Phase C — Modelling in the Data Builder (2026-10-27 → 2026-11-04)

### Views

`Discontinued` arrived from SQL Server's `bit` as a Boolean, so filters use `= TRUE`. The SQLScript
view took three tries. A table variable failed with a syntax error, an inline subquery compiled, and
the deploy then failed with error 1306 because the declared return columns had defaulted to
NVARCHAR(100); declaring all seven by hand fixed it. Deleting `CategoryName` from `V_NW_PRODUCT`, which
the SQLScript view selects, gave no warning, although the docs describe one. Version history restored
it. A table function's body may be opaque to that check, but this wasn't tested against other consumers.

### Joins and the union

A graphical join defaults to inner. Choosing left with *Exactly One → Many* appears in *Preview SQL* as
`LEFT EXACT ONE TO MANY JOIN`. The docs say a graphical `COUNT` counts distinct values, but the generated
SQL is plain `COUNT(col)`: same result on a unique `OrderID`, different on anything else.

Deploying the union gave four type warnings, because columns take their type from the first leg. The CSV
leg's Integer64 keys didn't match Azure's Integer, or SmallInt for `Quantity`, so the archive leg now
casts them. Both legs then reconciled to the cent against the CSV calculation.

### Dimensions, the fact and hierarchies

A new dimension's preview can show *no visible columns* with the settings greyed out, until another node
is selected and back. `TXT_NW_CATEGORY` only shows in *Dependency Analysis* after *Show Next Level*, and
that graph reads the deployed object, so a new association appears only after deploy. A scratch SQL view
failed with `CSN_COMPILATION_FAIL` first for using a business name as a column, and then until the page
was reloaded, which was editor state rather than the query.

Hierarchy technical names are limited to 20 characters, which the docs don't mention. The directory
association on Employee was greyed out with no explanation, because the dimension already had a
parent-child hierarchy. That led to moving the
directory to Customer and giving each dimension its own hierarchy type. Until a node type is flagged as
data node, the entity reports *Set one node type value as leaf*, where the docs say *Set as Data Node*. In
the preview, the location tree's revenue matched an independent CSV calculation at each level checked.

### Persistence

`V_DEMO_PUSHDOWN` from Phase B no longer existed, so `V_S4_BP_BY_CATEGORY` replaced it with the same
query. *Runtime Metrics* showed *Remote Statements (0)* on the federated view; the cause is unknown. View
Analyzer scored the local union 10, *Best Option*, at 0.07 s, which is how the score was found to be
relative to its lineage.

### Intelligent Lookup

The first rule matched 18 of 21 names. String(15) mapped to the lookup's String(5000) without complaint.
The prediction was that `USA` and `UK` would fail both rules, and `UK` didn't: the fuzzy rule proposed
Ukraine, on the same *Review* tab as the correct `Venezuela` proposal. Adding ISO columns to the fuzzy rule
also caught `USA`, which led to a separate exact rule on ISO-3. In this tenant the lookup and its output
view share one name, and the output's columns carry `input_` and `lookup_` prefixes, renamed in the wrapper.
