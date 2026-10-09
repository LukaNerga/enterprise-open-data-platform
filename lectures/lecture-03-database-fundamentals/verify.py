import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import psycopg2

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

EXPECTED_SCHEMAS = ["weather", "currency", "seismic"]

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "enterprise_open_data"),
        user=os.getenv("POSTGRES_USER", "eodp_user"),
        password=os.getenv("POSTGRES_PASSWORD", "change_me_locally"),
    )

def main() -> int:
    checks_passed = 0
    checks_total = 1 + len(EXPECTED_SCHEMAS)

    try:
        conn = get_connection()
        print("[OK] Connected to PostgreSQL")
        checks_passed += 1
    except Exception as exc:
        print(f"[FAIL] Connection failed: {exc}")
        return 1

    with conn, conn.cursor() as cur:
        cur.execute("SELECT schema_name FROM information_schema.schemata;")
        existing_schemas = {row[0] for row in cur.fetchall()}

        for schema in EXPECTED_SCHEMAS:
            if schema in existing_schemas:
                print(f"[OK] schema '{schema}' exists")
                checks_passed += 1
            else:
                print(f"[FAIL] schema '{schema}' not found")

    print(f"\nChecks passed ({checks_passed}/{checks_total})")
    return 0 if checks_passed == checks_total else 1

if __name__ == "__main__":
    sys.exit(main())
