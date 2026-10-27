# Decision log

Design decisions and changes to the project plan, newest first.

## 2026-10-27 — Round the `real` discount before computing revenue

- **Decision:** In `TF_NW_SALES`, `REVENUE` = `"UnitPrice" * "Quantity" * (1 - ROUND(TO_DECIMAL("Discount", 10, 6), 2))`,
  stored as `Decimal(15,2)` (truncated to cents, as in Phase A).
- **Why:** The Azure source stores `Discount` as `real`. Used directly, HANA computes the whole
  product in single precision (total 1,265,789.88). `TO_DECIMAL(…, 4, 2)` truncates, and the
  eight odd discounts (0.01–0.06) are stored just below their value (total 1,265,796.29). An
  independent recalculation from the CSV reproduced both totals exactly. Converting to six
  decimals and then rounding gives the exact discount and the reference total 1,265,792.64.
- **Consequence:** Types are fixed at the first transformation after landing. Phase C views
  read `LT_NW_AZ_SALES`, not the raw `real` column.

## 2026-10-27 — Outbound replication to ADLS Gen2 documented, not built

- **Decision:** The replication flow to Azure Data Lake Storage Gen2 (`RF_NW_ADLS`) is not
  built. It stays in the project as a documented design with its cost model. Databricks gets
  Datasphere data through the space's Open SQL schema over JDBC (Phase B) and, if the tenant
  allows it, through Business Data Cloud data products with Delta Sharing (Phase H).
- **Why:** Any non-SAP replication target (ADLS Gen2, S3, GCS, BigQuery, Kafka, SFTP) needs
  at least one *Premium Outbound Integration* block, allocated by an administrator on the
  *Tenant Configuration* page. On this training tenant that page isn't available (neither
  is *Capacities Monitoring*): capacity is managed outside the tenant, so no block can be
  assigned.
- **Cost model (from SAP's documentation):** one block gives 20 GB of transfer per month,
  on top of the data-integration execution hours every replication flow needs. Sizing
  counts the initial load plus the monthly delta volume. A flow that exceeds the
  allocation keeps running and is billed for the overage. For this project's data (under
  1 MB) one block would be plenty.
- **Consequence:** The B5 → B5b chain (replication flow with delta → transformation flow)
  is the delta proof; B5c's done criterion is met by this record.

## 2026-10-26 — Real-time replication through a Data Provisioning Agent

- **Decision:** Remote tables on the Azure SQL source go through an SAP HANA smart data
  integration (SDI) Data Provisioning Agent installed on the author's laptop, so that
  real-time replication of remote tables can be built hands-on. The attempt is
  time-boxed. If the agent can't be registered, the alternative is documented instead.
  Federated vs. snapshot access is measured either way, on the OData connections.
- **Why:** On Azure SQL Database, Datasphere offers replication flows and data flows
  directly, but remote tables only through SDI (the MssqlLogReaderAdapter). Real-time
  replication is the one access mode that needs the agent, and agents are what most
  on-premise SAP and database sources use in practice. The agent comes from SAP's public
  development tools site under the SAP Developer License.
- **Consequence:** A tenant-level agent registration and an IP allowlist entry for the
  agent host, both logged. Real-time runs only while the laptop is on, so it's enabled
  for the test and then switched off, which also protects the database's free compute
  budget.

## 2026-10-21 — Plan gaps closed: outbound to Databricks, SAP source, object store, cost

- **Decision:** Four topics the course list doesn't cover are added to the plan:
  - **Outbound replication to the Microsoft/Databricks stack** (high priority, Phase B): a
    replication flow writes Parquet to Azure Data Lake Storage Gen2 and Azure Databricks
    reads it, reconciled to the reference totals.
  - **An S/4HANA-style source** (brief, Phase B): can a Generic OData connection reach
    SAP's public sandbox APIs? If yes, one remote table; if no, the reason is documented.
  - **Object store and file spaces** (brief, Phase H): the cheaper storage tier that
    Business Data Cloud builds on.
  - **Capacity units and cost** (optional, Phase E): what replication, outbound
    integration, memory and storage cost.
- **Why:** The project targets a Microsoft/Databricks consulting context. "Datasphere
  data in Databricks" is the most likely real-world request, and its classic route
  (premium outbound integration) was only a footnote. SAP sources and cost are what
  clients ask about first.
- **Consequence:** Writing to a non-SAP target needs capacity units assigned to premium
  outbound integration, a tenant-level setting that costs capacity. It is checked before
  anything is changed. If the tenant can't, the setup and cost model are documented
  instead. The BDC route (zero-copy Delta Sharing) stays in Phase H as the strategic
  alternative.

## 2026-10-21 — Transformation flows added to the plan

- **Decision:** Transformation flows join Phase B at top priority, as a sub-phase right
  after replication flows: replication flow → local table with delta capture →
  transformation flow (initial and delta) → target table. The task chain in Phase E runs
  them in that order. Data flows stay, framed as the tool for what transformation flows
  can't do here (Python scripting in a HANA-storage space, one-off ETL straight from a
  source).
- **Why:** The course's topic list didn't include them, so the first rating-based plan
  missed them. SAP's documentation now names replication flows plus transformation flows
  as the preferred way to load and write local tables, instead of data flows. A replication
  flow only extracts and loads. The incremental transformation step belongs to the
  transformation flow, much like an incremental dbt model or a Databricks `MERGE` job
  after ingestion.
- **Consequence:** `TF_` objects move from *optional* to *planned* in the naming
  convention. Phase B's decision table compares replication flow + transformation flow
  against a data flow.

## 2026-10-21 — BW Bridge topics replaced by their BDC equivalents

- **Decision:** The planned SAP BW Bridge topics (value propositions, conversion, layer
  shift) become SAP Business Data Cloud topics with the same priority: BW modernization
  with BDC (BW private cloud edition, Data Product Generator) and BDC data products,
  formations and zero-copy / Delta Sharing to Databricks. BW Bridge remains as one
  option within them.
- **Why:** SAP's BDC FAQ (2025) states that BW Bridge is still supported in BDC, but that
  the strategic path for BW customers is SAP BW private cloud edition inside BDC, with
  BW data exposed as data products. For a Microsoft/Databricks consultancy where BDC is
  arriving, that path matters more than the bridge.
- **Consequence:** Phase H covers it briefly; hands-on work depends on the tenant being
  part of a BDC formation.

## 2026-10-21 — Topic priorities replace the course-unit plan

- **Decision:** The project is no longer planned unit by unit. It follows a priority
  rating of the course's topics (5 = in depth, 4 = properly, 3 = briefly, 2 = optional,
  1 = deprecated). The rating gives nine phases, A–I. Unit 01 becomes Phase A.
- **Why:** The course's unit order mixes depths and repeats topics. A priority list puts
  the effort where it matters for the job: integration, modelling, security and
  consumption in depth; governance, lifecycle and BDC briefly. Same build-journal workflow
  as the author's Fabric project: a guide per phase, a tracker, evidence per phase.
- **Consequence:** The old P0–P7 map, the per-unit READMEs (after unit 01) and the unit
  template are retired. The replication-flow plan of 2026-10-20 moves into Phase B. An
  Azure SQL Database with Microsoft's Northwind script is added as the delta-capable
  source.

## 2026-10-20 — Star schema by association: customer dimension as a view, generated time

- **Decision:** Customer attributes reach the model through an association from
  `FACT_NW_SALES` to a dimension view `DIM_NW_CUSTOMER` on `LT_NW_CUSTOMERS`, not through
  a join in the fact. Time uses the space's generated *Time Dimension - Day*, mapped from
  `ORDER_DATE` (Date). `ShipCountry` stays in the fact.
- **Why:** An association keeps the fact narrow and the dimension reusable by later facts;
  the analytic model joins it only when a query needs it. A view rather than flagging the
  table itself as a dimension leaves the ingestion layer untouched and gives one place for
  business names and later logic. SAC supports only the generated time dimensions as
  time dimensions, so a custom calendar would lose the time features. `ShipCountry`
  (ship-to, frozen per order) and the customer's country (sold-to, current master data)
  mean different things even though they coincide in Northwind.
- **Consequence:** Each new association must be added to `AM_NW_SALES` explicitly,
  redeployed, and the story saved again.

## 2026-10-20 — Replication flows: provisional plan

- **Status:** Superseded on 2026-10-21: adopted into Phase B (Azure SQL source); the ADLS
  outbound part became its own Phase B step later the same day (see *Plan gaps closed*).
- **P1 (ingestion):** Northwind in a free Azure SQL Database as the source of replication
  flows `RF_NW_<ENTITY>` (load type *Initial and Delta*) into `NW_LAB`, so federation,
  snapshot replication and delta replication can be compared on the same data. The
  Generic OData connection can't be used: replication flows aren't supported for it.
- **P7 (integration):** a replication flow to Azure Data Lake Gen2 for Azure Databricks,
  depending on the tenant's premium outbound integration capacity.
- **Source:** SAP's table of supported source and target connections for replication
  flows (Azure SQL Database: source with delta; ADLS Gen2: source initial-only, target
  with delta; OneLake: source only).

## 2026-10-19 — Replicate `RT_NW_ORDERS` (snapshot) instead of pure federation

- **Decision:** Switch `RT_NW_ORDERS` from remote access to a **snapshot replication**
  (*Start Data Replication*), refreshed on demand for now (a schedule follows in P5).
- **Why:** With pure federation the fact view's preview and the SAC story hit the
  3-minute query timeout. The *Remote Queries* monitor showed one full `Orders` fetch
  per query (column pruning via `$select`). Fetches finished in 2–5 s or stalled part-way
  (680 or 819 of 830 rows) for up to 20 minutes, so the public OData service is
  unreliable under repeated, concurrent requests. Replication reads the source once and
  serves every query locally.
- **Trade-off:** The data is only as fresh as the last snapshot, and it uses a little
  storage (830 rows). That's acceptable for a static sample source, and it's the
  federation-vs-replication choice the project is meant to show.

## 2026-10-19 — Align join key types at the source boundary

- **Decision:** After swapping `LT_NW_ORDERS` for `RT_NW_ORDERS`, cast the remote
  `OrderID` (Integer) to Integer64 with `TO_BIGINT` in a calculated column right after the
  remote source. The join then compares Integer64 with Integer64.
- **Why:** The join raised a data-type-mismatch warning. Results were correct through
  implicit widening, but aligning types once at the boundary keeps the model free of
  warnings, avoids per-row conversion, and widening can't lose values.

## 2026-10-19 — Move to an own space `NW_LAB`

- **Decision:** Create space `NW_LAB` and move the unit 01 objects out of the shared
  training space, replacing the earlier "folders as pseudo-spaces" approach. Objects move
  by CSN/JSON export and import plus a data reload; the SAC story is re-pointed with
  *Replace Model*. The old folder and connection in the shared space are deleted after
  verification.
- **Why:** The trainer confirmed that space creation is fine on this educational tenant.
  A real space exercises space-level features (time data, connections, database users,
  cross-space sharing in P4) instead of simulating them. *Copy Spaces* wasn't used
  because it copies a whole space, including other users' objects.
- **Consequence:** Object definitions become version-controlled CSN files in
  `datasphere/csn/`.

## 2026-10-19 — Trust DigiCert Global Root G2 for the Northwind OData service

- **Decision:** Upload the root CA **DigiCert Global Root G2** (valid to 2038) as a
  *TLS Server* certificate, not the `*.odata.org` server certificate or Microsoft's
  issuing CA.
- **Why:** The server certificate expires 2027-01-21 and the remote tables would stop
  working at every renewal. Microsoft rotates between several issuing CAs, so pinning one
  of them is fragile too. The root anchors the whole chain and is already trusted by
  every mainstream OS and browser. The certificate's fingerprint is checked against the
  Windows root store before upload.
- **Trade-off:** Trusting a root lets the tenant validate any HTTPS server whose chain
  ends at it. That's acceptable on an educational tenant. In a client tenant the
  certificate policy is the platform team's call, and a narrower anchor may be preferred.

## 2026-10-16 — REVENUE keeps truncation to 2 decimals

- **Decision:** `REVENUE` stays `Decimal(15,2)` without explicit `ROUND`; the reference
  total is **1,265,792.64** (exact sum 1,265,793.04).
- **Why:** The engine truncates on scale reduction; the 0.40 difference is understood and
  documented. Totals are compared against this reference in later units (source swap).
- **Revisit:** if a consumer needs cent rounding, switch to `ROUND(…, 2)` (→ 1,265,793.29).

## 2026-10-16 — Work in the trainer-provided space, folders as pseudo-spaces

- **Decision:** No own space for now. All objects are built in the shared training space
  inside a Data Builder folder `NW_LAB`; later layers get their own
  folders as if each were a space. The space-creation procedure stays documented in unit
  01 as reference.
- **Why:** In the training tenant only the trainer is meant to create spaces.
- **Limits accepted:** a folder is organisational only. There's no isolation, no own
  technical-name namespace (names must not collide with the other trainee's), no own
  schema or database users, and a shared time dimension and connections.
- **Revisit:** P4 (cross-space sharing) needs a second real space; P1/P3 may too if the
  ingestion/modelling split should be real rather than folder-only.

## 2026-10-16 — Private click-level journal and quiz checkpoints

- **Decision:** Click-level build guides, a progress tracker and a learning log live in a
  private, gitignored journal (`docs/private/`); public unit READMEs keep the condensed,
  reproducible version. Each part has pre- and post-build quiz checkpoints.
- **Why:** Same split as my Fabric projects. The public repo shows the solution; the
  journal holds the noisier build detail and personal learning records.

## 2026-10-16 — Unit 01 plan corrected before tenant work

- **Decision:** Reordered unit 01 to follow the course order (space → first model → first
  story → remote source → time dimension and associations) and made a minimal analytic
  model `AM_NW_SALES` part of the unit instead of an optional fallback.
- **Why:** SAC stories read analytic models, not Fact views directly, so the first story
  needs one. The course introduces the time dimension and associations after the remote
  source, and the story is extended once they exist. Other fixes: space creation needs the
  global DW Administrator role, `PostalCode` must be imported as string, the source swap
  uses the drop-on-node *Replace* action, and associations are inspected in the analytic
  model rather than in the view.

## 2026-10-15 — Unit 01 is a vertical slice across phases

- **Decision:** Unit 01 covers space setup (P0) *and* a first pass through ingestion (P1),
  a graphical view (P2), associations and a time dimension (P3) and a SAC story (P6).
  It is booked under P0; P1–P3 and P6 get later units that deepen each slice, and those
  phases only close once their own units are done.
- **Why:** The course's first unit goes end to end on a small scale. Splitting it by phase
  would break the course order and the objectives I named.

## 2026-10-15 — Naming convention

- **Decision:** `<TYPE>_<DOMAIN>_<ENTITY>` in UPPER_SNAKE_CASE with fixed type prefixes
  (see `docs/naming.md`).
- **Why:** Object type is visible in every list and lineage graph; consistent with SAP
  Datasphere having no folder structure for objects.

## 2026-10-15 — CSV files generated from the OData service

- **Decision:** The flat-file source is exported by `scripts/export_northwind.py` from the
  same OData service later used as remote source; the CSVs are not committed.
- **Why:** The licence of Northwind redistribution is unclear. Same data on both paths also
  makes the "replace local table by remote table" check meaningful: totals must not move.

## 2026-10-15 — Project framing

- **Decision:** Build one end-to-end project in phases (P0–P7), driven by the course units,
  instead of a set of isolated exercises.
- **Why:** A coherent project is better learning and better portfolio evidence; the course
  units map onto phases as they arrive.

## 2026-10-15 — Scenario: Northwind Traders

- **Decision:** Use Northwind as the spine dataset.
- **Why:** Public, well known and relational enough for a star schema. Available both as
  flat files and as a public OData service, so file loads and remote connections run on the
  same data. An SAP-flavoured source may be added in the ingestion phase.
