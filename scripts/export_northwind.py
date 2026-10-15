"""Export the Northwind sample tables from the public OData V4 service to CSV.

The CSV files are written to ``data/raw/`` (gitignored) and are the flat-file
source for the local tables in the lab. The same service is later used as a
remote OData source, so local and remote data stay identical.

Usage:
    python scripts\\export_northwind.py
"""

from __future__ import annotations

import csv
import json
import logging
import urllib.parse
import urllib.request
from collections.abc import Iterator
from pathlib import Path
from typing import Any

SERVICE_URL = "https://services.odata.org/V4/Northwind/Northwind.svc"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
REQUEST_TIMEOUT_S = 30
DATE_PREFIX_LEN = len("YYYY-MM-DD")

# entity set -> (output file, ordered columns to export)
EXPORTS: dict[str, tuple[str, list[str]]] = {
    "Customers": (
        "customers.csv",
        [
            "CustomerID",
            "CompanyName",
            "ContactTitle",
            "City",
            "Region",
            "PostalCode",
            "Country",
        ],
    ),
    "Orders": (
        "orders.csv",
        [
            "OrderID",
            "CustomerID",
            "EmployeeID",
            "OrderDate",
            "RequiredDate",
            "ShippedDate",
            "Freight",
            "ShipCity",
            "ShipCountry",
        ],
    ),
    "Order_Details": (
        "order_details.csv",
        ["OrderID", "ProductID", "UnitPrice", "Quantity", "Discount"],
    ),
}

DATE_COLUMNS = {"OrderDate", "RequiredDate", "ShippedDate"}

logger = logging.getLogger(__name__)


def fetch_pages(url: str) -> Iterator[dict[str, Any]]:
    """Yield every entity of an OData collection, following server-side paging.

    Args:
        url: Collection URL, optionally with query options.

    Yields:
        One decoded JSON entity per row.
    """
    next_url: str | None = url
    while next_url:
        request = urllib.request.Request(  # noqa: S310 - fixed https endpoint
            next_url, headers={"Accept": "application/json"}
        )
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_S) as response:  # noqa: S310
            payload: dict[str, Any] = json.load(response)
        yield from payload["value"]
        link: str | None = payload.get("@odata.nextLink")
        # the service returns paging links relative to the current request URL
        next_url = urllib.parse.urljoin(next_url, link) if link else None


def clean(column: str, value: Any) -> str:
    """Render a value for CSV; date-times are cut down to ISO dates.

    Args:
        column: Column name.
        value: Raw JSON value.

    Returns:
        The CSV cell text (empty string for null).
    """
    if value is None:
        return ""
    text = str(value)
    if column in DATE_COLUMNS:
        return text[:DATE_PREFIX_LEN]
    return text


def export_entity_set(entity_set: str, filename: str, columns: list[str]) -> int:
    """Download one entity set and write it as a UTF-8 CSV with a header row.

    Args:
        entity_set: OData entity set name.
        filename: Output file name inside ``OUTPUT_DIR``.
        columns: Columns to export, in order.

    Returns:
        Number of rows written.
    """
    select = ",".join(columns)
    url = f"{SERVICE_URL}/{entity_set}?$select={select}"
    target = OUTPUT_DIR / filename
    rows = 0
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        for entity in fetch_pages(url):
            writer.writerow([clean(c, entity.get(c)) for c in columns])
            rows += 1
    return rows


def main() -> None:
    """Export all configured entity sets."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for entity_set, (filename, columns) in EXPORTS.items():
        count = export_entity_set(entity_set, filename, columns)
        logger.info("%s: %d rows -> %s", entity_set, count, OUTPUT_DIR / filename)


if __name__ == "__main__":
    main()
