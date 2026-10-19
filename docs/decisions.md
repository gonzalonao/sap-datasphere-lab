# Decision log

Design decisions and changes to the project plan, newest first.

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
  (`LABORATORIO`) inside a Data Builder folder `NW_LAB`; later layers get their own
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
