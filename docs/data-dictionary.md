# Data dictionary

Objects in the space `NW_LAB`, by layer. Phase A's objects (`LT_NW_*`, `RT_NW_ORDERS`,
`FACT_NW_SALES`, `DIM_NW_CUSTOMER`, `AM_NW_SALES`) are described in
[`units/01-space-model-remote/`](../units/01-space-model-remote/README.md) and move here in
Phase I. Naming rules: [`naming.md`](naming.md).

## Landed from Azure SQL (Phase B)

### Replication flow targets `LT_NW_AZ_*`

Written by `RF_NW_AZSQL` (*Initial and Delta*). Each is a local table with delta capture, so
it deploys as two objects:

- the **delta capture table** `<name>_Delta`: every record ever loaded, including deletes, plus
  *Change Type* and *Change Date* (UTC). Transformation flows read deltas from it.
- the **active records** object `<name>`: current records only, without the change columns.
  Views and analytic models read it.

| Table | Source | Rows | Notes |
| ----- | ------ | ---- | ----- |
| `LT_NW_AZ_ORDERS` | `dbo.Orders` | 830 | Order headers |
| `LT_NW_AZ_ORDER_DETAILS` | `dbo.[Order Details]` | 2,155 | Order lines; key `OrderID` + `ProductID`; `Discount` arrives as REAL (`hana.REAL`) |
| `LT_NW_AZ_CUSTOMERS` | `dbo.Customers` | 91 | |
| `LT_NW_AZ_PRODUCTS` | `dbo.Products` | 77 | |
| `LT_NW_AZ_EMPLOYEES` | `dbo.Employees` | 9 | `Photo`, `Notes` skipped (unsupported types) |
| `LT_NW_AZ_CATEGORIES` | `dbo.Categories` | 8 | `Picture`, `Description` skipped |
| `LT_NW_AZ_SUPPLIERS` | `dbo.Suppliers` | 29 | `HomePage` skipped |
| `LT_NW_AZ_SHIPPERS` | `dbo.Shippers` | 3 | |

Change types seen: `L` (initial load), `U` (update), `D` (delete).

### `LT_NW_AZ_SALES`: order lines with revenue

Written by `TF_NW_SALES`: `LT_NW_AZ_ORDER_DETAILS` (delta source) left-joined to
`LT_NW_AZ_ORDERS` (active records) on `OrderID`. One row per order line, delta capture on.

| Column | Type | Meaning |
| ------ | ---- | ------- |
| `OrderID`, `ProductID` | key | The order line |
| `UnitPrice`, `Quantity`, `Discount` | from the line | As in the source (`Discount` REAL) |
| Order header columns | from `Orders` | `CustomerID`, `EmployeeID`, `OrderDate`, `ShipCountry` and the other header fields, as of the last full load (see below) |
| `REVENUE` | Decimal(15,2) | `UnitPrice × Quantity × (1 − ROUND(TO_DECIMAL(Discount, 10, 6), 2))`, truncated to cents. Total **1,265,792.64** |
| `ORDER_DATE` | Date | `TO_DATE(OrderDate)` |
| *Change Type*, *Change Date* | delta capture | *Change Date* = the transformation flow's run time |

Header fields only refresh when an order *line* changes or the watermark is reset: the flow's
delta source is the line table.

### `LT_NW_AZ_EMPLOYEES_CLEAN`

Written by `DF_NW_EMPLOYEES` in *Truncate* mode. 9 rows, 13 columns: `EmployeeID`, `LastName`,
`FirstName`, `Title`, `TitleOfCourtesy`, `BirthDate`, `HireDate`, `City`, `Country`, `HomePhone`,
`ReportsTo`, plus two columns from the Python script:

| Column | Type | Meaning |
| ------ | ---- | ------- |
| `FULL_NAME` | String(60) | `FirstName LastName`, trimmed |
| `PHONE_DIGITS` | String(24) | `HomePhone` with every non-digit removed |

## Remote tables (Phase B)

| Table | Connection | Access | Rows | Notes |
| ----- | ---------- | ------ | ---- | ----- |
| `RT_NW_AZ_ORDERS` | `CN_NW_AZSQL` (DP Agent) | Replicated (snapshot) | 830 | Used to measure remote, snapshot, partitioned and real-time access |
| `RT_S4_BUSINESS_PARTNER` | `CN_NW_S4SBX` | Remote | – | SAP S/4HANA Cloud sandbox, Business Partner API |
| `Country_Master_Data_by_DCA` | Data Marketplace | Installed product | 244 | Country, ISO alpha-2, alpha-3, numeric code, average latitude and longitude. Name set by the provider |

## Open SQL schema `NW_LAB#ETL` (Phase B)

| Table | Rows | Meaning |
| ----- | ---- | ------- |
| `SALES_TARGETS` | 62 | Synthetic revenue target per ship country and order year: actual × 1.10, rounded to thousands; total 1,393,000. Key `COUNTRY` + `ORDER_YEAR`. Written by [`scripts/load_sales_targets.py`](../scripts/load_sales_targets.py) (*pending*) |
