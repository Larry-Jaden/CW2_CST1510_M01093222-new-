import pandas as pd
from app.data.db import connect_database, DB_PATH


def show_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    if not tables:
        print("No user tables found in the database.")
        return

    for table in tables:
        print('\n' + '=' * 60)
        print(f"Table: {table}")
        # Schema
        cursor.execute(f"PRAGMA table_info('{table}')")
        cols = cursor.fetchall()
        print("Schema:")
        for col in cols:
            # PRAGMA table_info returns
            cid, name, ctype, notnull, dflt, pk = col
            print(f" - {name} ({ctype}){' PRIMARY_KEY' if pk else ''}{' NOT NULL' if notnull else ''}  default={dflt}")

        # Count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
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
    conn = connect_database()
    print(f"Using DB: {DB_PATH.resolve()}")
    show_tables(conn)
    conn.close()


if __name__ == '__main__':
    main()
