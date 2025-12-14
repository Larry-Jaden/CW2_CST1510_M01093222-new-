import pandas as pd
from app.data.db import connect_database

def get_all_datasets():
    """
    Retrieve all datasets from the database.
    """
    conn = connect_database()
    query = "SELECT * FROM datasets_metadata ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_datasets_by_category(category):
    """
    Retrieve datasets filtered by category.
    """
    conn = connect_database()
    query = "SELECT * FROM datasets_metadata WHERE category = ? ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=(category,))
    conn.close()
    return df