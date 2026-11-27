"""
E + L ของ ELT: โหลดไฟล์ CSV ของ Northwind เข้า DuckDB

python scripts/load_raw.py
"""
import sys
from pathlib import Path

import duckdb

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "raw_data"
DB_PATH = ROOT / "scripts" / "northwind.duckdb"

SOURCES = {
    "customer": "raw/customer.csv",
    "employees": "raw/employees.csv",
    "order_details": "raw/order_details.csv",
    "orders": "raw/orders.csv",
    "products": "raw/products.csv",
    "shippers": "raw/shippers.csv",
    "suppliers": "raw/suppliers.csv",
    "legacy_orders": "legacy/orders.csv",
    "legacy_order_details": "legacy/order_details.csv",
}


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")

        print(f"โหลดข้อมูลเข้า {DB_PATH.name}")
        for table, relative_path in SOURCES.items():
            csv_path = DATA_DIR / relative_path
            if not csv_path.exists():
                raise FileNotFoundError(f"ไม่พบไฟล์ {csv_path}")

            con.execute(
                f"""
                CREATE OR REPLACE TABLE raw.{table} AS
                SELECT *
                FROM read_csv('{csv_path.as_posix()}', header = true)
                """
            )
            count = con.execute(
                f"SELECT COUNT(*) FROM raw.{table}"
            ).fetchone()[0]
            print(f" raw.{table:<22} {count:>6,} แถว")
    finally:
        con.close()

    print("เสร็จแล้ว — ขั้นต่อไป: dbt run")


if __name__ == "__main__":
    main()