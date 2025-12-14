import pandas as pd
from pathlib import Path
from app.data.db import connect_database, DB_PATH, DATA_DIR
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents


def show_tables(conn):
    """Print table names, row counts and up to 5 sample rows (no schema)."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        print("No user tables found in the database.")
        return

    for table in tables:
        print('\n' + '=' * 60)
        print(f"Table: {table}")

        # Count
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
        except Exception:
            count = 0
        print(f"Row count: {count}")

        # Show first 5 rows
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5", conn)
            if df.empty:
                print(" (no rows)")
            else:
                print("First rows:")
                print(df.to_string(index=False))
        except Exception as e:
            print(f"Could not read rows for {table}: {e}")


def main():
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting Week 8 demo")
    print(f"DATA folder: {DATA_DIR.resolve()}")
    print(f"Database will be created at: {DB_PATH.resolve()}")

    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)

    # Ensure datasets and tickets are loaded if empty
    def _load_csv_if_empty(table_name, keyword):
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        cnt = cur.fetchone()[0]
        if cnt > 0:
            return 0

        # find file in DATA_DIR containing keyword
        found = None
        for p in DATA_DIR.iterdir():
            if p.is_file() and keyword in p.name.lower():
                found = p
                break
        if not found:
            return 0

        try:
            df = pd.read_csv(found)
            df.columns = df.columns.str.strip()
            df.to_sql(table_name, conn, if_exists='append', index=False)
            return len(df)
        except Exception:
            return 0

    loaded_datasets = _load_csv_if_empty('datasets_metadata', 'datasets')
    loaded_tickets = _load_csv_if_empty('it_tickets', 'ticket')
    if loaded_datasets:
        print(f"Loaded {loaded_datasets} rows into datasets_metadata")
    if loaded_tickets:
        print(f"Loaded {loaded_tickets} rows into it_tickets")

    # 2. Migrate users from file (if present)
    migrated = migrate_users_from_file(conn)
    print(f"Migrated {migrated} users from file (if present).")

    # 3. Test register/login 
    success, msg = register_user("demo_user", "DemoPass123!", "analyst")
    print(f"Register: {msg}")

    success, msg = login_user("demo_user", "DemoPass123!")
    print(f"Login: {msg}")

    # 4. Create an incident and list incidents
    incident_id = insert_incident("Phishing attempt", "High", "Open", "2024-11-25", conn=conn)
    print(f"Created incident id: {incident_id}")

    df = get_all_incidents(conn=conn)
    print(f"Total incidents in DB: {len(df)}")

    # 5. Show tables and samples
    show_tables(conn)

    conn.close()


if __name__ == "__main__":
    main()
