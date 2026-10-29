# Phase B evidence

Screenshots from the SAP Datasphere tenant and the Azure portal, taken on 2026-10-29 during the
phase close. Tenant URLs and host names are cropped out. Steps refer to the
[phase summary](../../phases/phase-b-ingestion.md); the narrative is in the
[build log](../../build-log.md).

## Sources and connections

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`b1-azure-free-offer.png`](b1-azure-free-offer.png) | B1 | Azure SQL Database cost summary (Spanish UI): compute and storage at 0.00 USD under the free offer, overage billing disabled |
| [`b1-azsql-tile-info.png`](b1-azsql-tile-info.png) | B1 | *Create Connection*: the *Microsoft Azure SQL Database* tile's available features (data flows, remote tables, replication flows) |
| [`b1-cn-nw-azsql-validated.png`](b1-cn-nw-azsql-validated.png) | B1 | `CN_NW_AZSQL` validated: data flows, replication flows and remote tables enabled |
| [`b3-agent-connected.png`](b3-agent-connected.png) | B3 | DP Agent `NWLAB01` connected (2.8.1.2) with `MssqlLogReaderAdapter` enabled |

## Remote tables and schedules

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`b3-snapshot-run.png`](b3-snapshot-run.png) | B3 | `RT_NW_AZ_ORDERS` snapshot run: 830 records, *Switching data access (batch) to the new replica*, and the `OrderID` partition ranges |
| [`b4-schedule.png`](b4-schedule.png) | B4 | *Remote Tables* monitor: Phase A's `RT_NW_ORDERS` on *Every 1 Days* with its next run, next to the Azure, sandbox and Marketplace tables |

## Replication, transformation and data flows

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`b5-rf-run.png`](b5-rf-run.png) | B5 | `RF_NW_AZSQL` run: 8 objects *Completed (next run will be delta)*; Orders metrics 830 initial-load operations, 1 delta record |
| [`b5-delta-preview.png`](b5-delta-preview.png) | B5 | `LT_NW_AZ_SHIPPERS` with delta capture on: *Change Type* `L` for the initial load, `D` for the deleted `Test Shipper` |
| [`b5b-tf-editor.png`](b5b-tf-editor.png) | B5b | `TF_NW_SALES` view transform: order lines (*Delta Capture*) left-joined to orders (*Active Records*), then projection and calculated columns |
| [`b5b-watermark.png`](b5b-watermark.png) | B5b | `TF_NW_SALES` run on SAP HANA: 2,155 records written; *Delta Capture Settings* with the watermark on `LT_NW_AZ_ORDER_DETAILS_Delta` and *Reset Watermark* |
| [`b5b-tf-totals.png`](b5b-tf-totals.png) | B5b | Reconciliation of `LT_NW_AZ_SALES`: 2,155 lines, Quantity 51,317, revenue 1,265,792.64 |
| [`b6-df-canvas.png`](b6-df-canvas.png) | B6 | `DF_NW_EMPLOYEES`: source → projection → Python script operator (`FULL_NAME`, `PHONE_DIGITS`) → target |
| [`b6-df-run.png`](b6-df-run.png) | B6 | `DF_NW_EMPLOYEES` run completed, 9 records written to the target |

## Open SQL schema and Data Marketplace

| File | Step | What it shows |
| ---- | ---- | ------------- |
| [`b7-db-user.png`](b7-db-user.png) | B7 | Database user `NW_LAB#ETL` with read and write access, active |
| [`b7-targets-view.png`](b7-targets-view.png) | B7 | `V_NW_SALES_VS_TARGET`: the full outer join of actuals and `SALES_TARGETS`, 62 rows, deployed |
| [`b8-marketplace-product.png`](b8-marketplace-product.png) | B8 | *Global Country Identifier Data by DCA*: open access, integrated delivery, under 1,000 records, one-time replication |
| [`b8-installed.png`](b8-installed.png) | B8 | *Marketplace Data Products*: the product installed into `NW_LAB`, up to date |

Not captured: the *Remote Queries* statements for pushdown, partitioned loads and the OData
sandbox. The build log and the phase summary's measured table record what they showed.
