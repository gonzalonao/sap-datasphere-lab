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
