# Data

Only public or synthetic data is used. Raw downloads are **not committed**: they are
generated locally into `data\raw\` (gitignored).

## Northwind Traders

| Item | Value |
| ---- | ----- |
| Source | Public Northwind sample OData service published by the OData organisation: `https://services.odata.org/V4/Northwind/Northwind.svc/` (V2 variant at `/V2/Northwind/Northwind.svc/`) |
| Content | Sample company data: customers, orders, order details (further entity sets are used in later units) |
| Licence | Published as a demo/sample dataset; no explicit licence stated on the service (⚠ verify before any redistribution). Hence not stored in the repo |
| Used in | Unit 01: CSV upload into local tables, then the same service as a remote OData source |

### Regenerating the CSV files

```powershell
python scripts\export_northwind.py
```

| File | Entity set | Rows (as exported 2026-10-15) | Columns |
| ---- | ---------- | ----------------------------- | ------- |
| `data\raw\customers.csv` | `Customers` | 91 | CustomerID, CompanyName, ContactTitle, City, Region, PostalCode, Country |
| `data\raw\orders.csv` | `Orders` | 830 | OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, Freight, ShipCity, ShipCountry |
| `data\raw\order_details.csv` | `Order_Details` | 2155 | OrderID, ProductID, UnitPrice, Quantity, Discount |

Notes: contact names, phone numbers and street addresses are deliberately left out of the
export. Date-time columns are cut to `YYYY-MM-DD`.

## Northwind on Azure SQL Database (Phase B)

The same Northwind data, loaded into an Azure SQL Database. It's the delta-capable source
for replication flows (the OData service can't be a replication-flow source).

| Item | Value |
| ---- | ----- |
| Source | Microsoft's sample script `instnwnd (Azure SQL Database).sql` in [microsoft/sql-server-samples](https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/northwind-pubs) |
| Licence | MIT (Microsoft SQL Server Sample Code). The script isn't copied into this repo; download it from the source |
| Content | 13 tables under `dbo`: the 8 core Northwind tables plus Region, Territories, EmployeeTerritories, CustomerDemographics, CustomerCustomerDemo; views and procedures |
| Target | Azure SQL Database, free offer (General Purpose serverless, auto-pause when the monthly free limit is reached), database `northwind` |
| Used in | Phase B: `CN_NW_AZSQL` → replication flows (with delta), data flows |

### Loading it

1. Create the free database (Azure portal → aka.ms/azuresqlhub → *Start free*). Open the
   server firewall to your client IP and to Datasphere's *Replication/Data Flow NAT IP
   (egress)*, which is shown under *Profile → About → More* in Datasphere.
2. Connect as the server admin to database `northwind` with a client that understands `GO`
   (VS Code with the MSSQL extension, or SSMS), and run the downloaded script.
3. Create the Datasphere user: [`sql/azure-sql/01_dsp_rep_user.sql`](../sql/azure-sql/01_dsp_rep_user.sql).
4. Check the load: [`sql/azure-sql/02_verify_northwind.sql`](../sql/azure-sql/02_verify_northwind.sql).

| Table | Rows | Reconciles with |
| ----- | ---- | --------------- |
| `Orders` | 830 | `orders.csv` |
| `Order Details` | 2,155 | `order_details.csv` |
| `Customers` | 91 | `customers.csv` |
| `Products` / `Employees` / `Suppliers` | 77 / 9 / 29 | not in the CSV export |

Totals over `Order Details`: Quantity **51,317**, revenue **1,265,792.64**
(`UnitPrice × Quantity × (1 − Discount)`, each line truncated to 2 decimals), identical to
the Phase A reference. Verified at the source on 2026-10-26.

Notes: `Employees`, `Categories`, `Suppliers` and `CustomerDemographics` contain `image` /
`ntext` columns, which replication flows don't support. The serverless database pauses when
idle, and the first connection after a pause fails while it resumes.

## Synthetic sales targets (Phase B, Open SQL schema)

`scripts/load_sales_targets.py` derives one revenue target per ship country and order year
from the CSV export: actual revenue (each line truncated to 2 decimals) × 1.10, rounded to
thousands. That gives **62 rows totalling 1,393,000**. The script writes them to the table
`SALES_TARGETS` in the space's Open SQL schema through a database user (`hdbcli`, connection
settings from environment variables). The numbers are synthetic and exist only to show an
external write into the space.

## Synthetic category texts (Phase C, text entity)

[`synthetic/category_texts.csv`](synthetic/category_texts.csv) holds the 8 Northwind category
names in English, Spanish and German: 24 rows, columns `CategoryID`, `LANGUAGE` (ISO 639-1,
lowercase, one of the formats a Datasphere text entity accepts) and `CATEGORY_TEXT`. Northwind
itself is English-only, so the Spanish and German names are written for this project
(synthetic, no licence restrictions). The English rows match `Categories.CategoryName`. The file
is imported as the local table `LT_NW_CATEGORY_TEXTS` and wrapped by the text entity
`TXT_NW_CATEGORY`.
