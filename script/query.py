"""
รันคำสั่ง SQL กับคลังข้อมูล แล้วพิมพ์ผลเป็นตาราง

    python scripts/query.py "SELECT * FROM warehouse.dim_product LIMIT 5"
    python scripts/query.py queries/q1_revenue_by_category_month.sql
"""
import sys
from pathlib import Path

import duckdb

# ให้พิมพ์ภาษาไทยได้บน Windows ทุกรุ่น
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "northwind.duckdb"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    arg = sys.argv[1]
    sql = Path(arg).read_text(encoding="utf-8") if arg.endswith(".sql") else arg

    # read_only=True: เปิดอ่านอย่างเดียว จึงไม่ไปล็อกไฟล์ขณะที่โปรแกรมอื่นใช้งานอยู่
    con = duckdb.connect(str(DB_PATH), read_only=True)
    result = con.execute(sql)
    columns = [d[0] for d in result.description]
    rows = result.fetchall()
    con.close()

    cells = [[("" if v is None else str(v)) for v in row] for row in rows]
    widths = [max([len(c)] + [len(r[i]) for r in cells]) for i, c in enumerate(columns)]
    print("  ".join(c.ljust(w) for c, w in zip(columns, widths)))
    print("  ".join("-" * w for w in widths))
    for r in cells:
        print("  ".join(v.ljust(w) for v, w in zip(r, widths)))
    print(f"({len(rows)} แถว)")


if __name__ == "__main__":
    main()
