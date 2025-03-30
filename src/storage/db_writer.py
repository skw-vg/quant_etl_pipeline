import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# Load .env file
load_dotenv()

def save_to_database(df: pd.DataFrame, table_name: str, if_exists: str = 'append') -> None:
    """
    Saves a pandas DataFrame to a PostgresSQL table.

    Args:
        df (pd.DataFrame): The DataFrame to save
        table)name (str): Table name in the PostgresSQL DB
        if_exists (str): What to do if table exists ("fail", "replace", "append")
    """
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError('DATABASE_URL not found in .env')

    # Create a SQLAlchemy engine (connects Python to the DB)
    engine = create_engine(db_url)

    # Save the DataFrame to the DB table
    df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)

    print(f"✅ Saved {len(df)} rows to table '{table_name}' in PostgreSQL.")

