import pandas as pd
from app.data.db import connect_database

def get_all_tickets():
    """
    Retrieve all IT tickets from the database.
    """
    conn = connect_database()
    query = "SELECT * FROM it_tickets ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_tickets_by_priority(priority):
    """
    Retrieve tickets filtered by priority.
    """
    conn = connect_database()
    query = "SELECT * FROM it_tickets WHERE priority = ? ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=(priority,))
    conn.close()
    return df