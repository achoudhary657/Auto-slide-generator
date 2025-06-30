"""
Module for data ingestion from spreadsheets, SQL files, and databases.
"""

import pandas as pd
from sqlalchemy import create_engine

def read_excel(file_path):
    """Read data from an Excel file."""
    return pd.read_excel(file_path)

def read_csv(file_path):
    """Read data from a CSV file."""
    return pd.read_csv(file_path)

def read_sql_file(sql_file_path, db_url='sqlite:///:memory:'):
    """Execute SQL queries from a file on a database and return the result as a DataFrame."""
    engine = create_engine(db_url)
    with open(sql_file_path, 'r') as file:
        sql_query = file.read()
    with engine.connect() as connection:
        result = pd.read_sql_query(sql_query, connection)
    return result

def read_database_table(table_name, db_url):
    """Read a table from a database and return as a DataFrame."""
    engine = create_engine(db_url)
    with engine.connect() as connection:
        result = pd.read_sql_table(table_name, connection)
    return result
