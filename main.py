from distutils.command.clean import clean

import yaml                         # lets you read .yaml files
from dotenv import load_dotenv      # loads environment variables from .env file

load_dotenv()                       # loads the .env file into your environment (for DB credentials later)

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)      # reads your config file into a Python dictionary

        # config =  {
        # "tickers": ["AAPL", "MSFT", "GOOGL"],
        # "start_date": "2023-01-01",
        # "end_date": "2023-12-31"
        # }

tickers = config["tickers"]
start_date = config["start_date"]
end_date = config["end_date"]


if __name__ == '__main__':
    # 1. Import needed functions
    from src.ingestion.yfinance_loader import download_stock_data
    from src.transformation.basic_cleaning import clean_data
    from src.storage.db_writer import save_to_database

    # 3. Run pipeline for one ticker ('AAPL')
    df = download_stock_data(tickers[0], start_date, end_date)
    clean_df = clean_data(df)
    save_to_database(clean_df, table_name='market_data')

    # 4. TEST output right here:
    print(df.head())
    print(clean_df.head())
    print(clean_df.columns)
