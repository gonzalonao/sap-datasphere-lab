-- Check the Northwind load against the project's reference numbers.
-- Expected: Orders 830, Order Details 2,155, Customers 91, Products 77, Employees 9,
-- Suppliers 29; qty 51,317; revenue_trunc 1,265,792.64.

SELECT 'Orders' AS table_name, COUNT(*) AS row_count FROM dbo.Orders UNION ALL
SELECT 'Order Details', COUNT(*) FROM dbo.[Order Details] UNION ALL
SELECT 'Customers', COUNT(*) FROM dbo.Customers UNION ALL
SELECT 'Products', COUNT(*) FROM dbo.Products UNION ALL
SELECT 'Employees', COUNT(*) FROM dbo.Employees UNION ALL
SELECT 'Suppliers', COUNT(*) FROM dbo.Suppliers;

-- Revenue as in Phase A: each line truncated to 2 decimals (ROUND(x, 2, 1) truncates).
-- Discount is `real`, so it's cast to decimal before multiplying.
SELECT SUM(Quantity) AS qty,
       SUM(ROUND(CAST(UnitPrice * Quantity * (1 - CAST(Discount AS decimal(9, 4)))
                      AS decimal(19, 6)), 2, 1)) AS revenue_trunc
FROM dbo.[Order Details];
