"""Load synthetic yearly revenue targets into the space's Open SQL schema.

The targets are derived from the Northwind CSV export in ``data/raw/`` (see
``scripts/export_northwind.py``): actual revenue per ship country and order year,
each line truncated to 2 decimals as in Phase A, times 1.10, rounded to thousands.
The table lands in the database user's own schema (``NW_LAB#<SUFFIX>``), where
Datasphere views can use it as a source.

Connection settings come from environment variables, never from the repo:

- ``DSP_DB_HOST``: host name from the database user's details dialog
- ``DSP_DB_USER``: database user name, e.g. ``NW_LAB#ETL`` (also the schema name)
- ``DSP_DB_PASSWORD``: the user's password
- ``DSP_DB_PORT``: optional, defaults to 443

``--sql`` writes the same rows as a SQL script instead, for running in the SAP HANA
database explorer as the database user when no local client is at hand.

Usage:
    python scripts\\load_sales_targets.py --dry-run
    python scripts\\load_sales_targets.py
    python scripts\\load_sales_targets.py --sql sql\\datasphere\\01_sales_targets.sql
"""

from __future__ import annotations

import argparse
import csv
import logging
import os
from collections import defaultdict
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
TABLE_NAME = "SALES_TARGETS"
DEFAULT_SCHEMA = "NW_LAB#ETL"
DEFAULT_PORT = 443
TARGET_UPLIFT = Decimal("1.10")
CENT = Decimal("0.01")
THOUSAND = Decimal("1E3")
YEAR_LEN = len("YYYY")

CREATE_TABLE_SQL = """
CREATE COLUMN TABLE "{schema}"."{table}" (
    "COUNTRY" NVARCHAR(15) NOT NULL,
    "ORDER_YEAR" INTEGER NOT NULL,
    "TARGET_REVENUE" DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY ("COUNTRY", "ORDER_YEAR")
)
"""

logger = logging.getLogger(__name__)


def compute_targets(raw_dir: Path) -> list[tuple[str, int, Decimal]]:
    """Compute one revenue target per ship country and order year.

    Args:
        raw_dir: Folder holding ``orders.csv`` and ``order_details.csv``.

    Returns:
        Rows of (country, year, target revenue), sorted by country and year.
    """
    with (raw_dir / "orders.csv").open(encoding="utf-8", newline="") as handle:
        order_keys = {
            row["OrderID"]: (row["ShipCountry"], int(row["OrderDate"][:YEAR_LEN]))
            for row in csv.DictReader(handle)
        }

    actuals: defaultdict[tuple[str, int], Decimal] = defaultdict(Decimal)
    with (raw_dir / "order_details.csv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            line = (
                Decimal(row["UnitPrice"])
                * int(row["Quantity"])
                * (1 - Decimal(row["Discount"]))
            )
            actuals[order_keys[row["OrderID"]]] += line.quantize(
                CENT, rounding=ROUND_DOWN
            )

    return [
        (
            country,
            year,
            (actual * TARGET_UPLIFT).quantize(THOUSAND, rounding=ROUND_HALF_UP),
        )
        for (country, year), actual in sorted(actuals.items())
    ]


def load(rows: list[tuple[str, int, Decimal]]) -> None:
    """Create the target table if needed and replace its contents.

    Args:
        rows: Rows of (country, year, target revenue).

    Raises:
        KeyError: If a required environment variable is missing.
        hdbcli.dbapi.Error: If a statement fails; the transaction is rolled back
            first, so the table keeps its previous rows.
    """
    # hdbcli (SAP HANA client) ships without type stubs
    from hdbcli import dbapi  # type: ignore[import-untyped]

    schema = os.environ["DSP_DB_USER"]
    connection = dbapi.connect(
        address=os.environ["DSP_DB_HOST"],
        port=int(os.environ.get("DSP_DB_PORT", DEFAULT_PORT)),
        user=schema,
        password=os.environ["DSP_DB_PASSWORD"],
        encrypt=True,
        sslValidateCertificate=True,
        # hdbcli autocommits by default; one transaction keeps the old rows on a failure
        autocommit=False,
    )
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM SYS.TABLES WHERE SCHEMA_NAME = ? AND TABLE_NAME = ?",
            (schema, TABLE_NAME),
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(CREATE_TABLE_SQL.format(schema=schema, table=TABLE_NAME))
            logger.info("Created %s.%s", schema, TABLE_NAME)
        # delete + insert keeps reruns idempotent
        cursor.execute(f'DELETE FROM "{schema}"."{TABLE_NAME}"')
        cursor.executemany(
            f'INSERT INTO "{schema}"."{TABLE_NAME}" VALUES (?, ?, ?)',
            [(country, year, f"{target:.2f}") for country, year, target in rows],
        )
        connection.commit()
    except dbapi.Error:
        connection.rollback()
        raise
        logger.info("Loaded %d rows into %s.%s", len(rows), schema, TABLE_NAME)
    finally:
        connection.close()


def render_sql(rows: list[tuple[str, int, Decimal]], schema: str) -> str:
    """Render the table definition and rows as a SQL script.

    HANA has no multi-row ``VALUES``, so the rows go in as one ``INSERT … SELECT``
    over ``DUMMY``.

    Args:
        rows: Rows of (country, year, target revenue).
        schema: Open SQL schema to create the table in.

    Returns:
        The script text: ``CREATE`` and ``INSERT`` statements, each ending in ``;``.
    """
    selects = "\nUNION ALL ".join(
        f"SELECT '{country}', {year}, {target:.2f} FROM DUMMY"
        for country, year, target in rows
    )
    create = CREATE_TABLE_SQL.format(schema=schema, table=TABLE_NAME).strip()
    return (
        f"-- Generated by scripts/load_sales_targets.py: {len(rows)} rows.\n"
        f"{create};\n\n"
        f'INSERT INTO "{schema}"."{TABLE_NAME}"\n{selects};\n'
    )


def main() -> None:
    """Compute the targets, then load them, or write SQL with ``--sql``."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dry-run", action="store_true", help="compute and log only, don't connect"
    )
    parser.add_argument(
        "--sql", type=Path, help="write a SQL script to this path instead of loading"
    )
    parser.add_argument(
        "--schema", default=DEFAULT_SCHEMA, help="schema used in the --sql script"
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    rows = compute_targets(RAW_DIR)
    total = sum((target for _, _, target in rows), Decimal(0))
    logger.info("%d targets, total %s", len(rows), f"{total:,}")
    if args.dry_run:
        return
    if args.sql:
        args.sql.parent.mkdir(parents=True, exist_ok=True)
        args.sql.write_text(render_sql(rows, args.schema), encoding="utf-8")
        logger.info("Wrote %s", args.sql)
        return
    load(rows)


if __name__ == "__main__":
    main()
