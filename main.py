import yaml                         # lets you read .yaml files
import pandas as pd
from dotenv import load_dotenv      # loads environment variables from .env file
from datetime import datetime
from src.ingestion.yfinance_loader import download_stock_data
from src.transformation.basic_cleaning import clean_data
from src.storage.db_writer import save_to_database
from src.utils.get_sp500_ticker_list import sp500_web_scrapper
from src.transformation.indicators import calculate_all_indicators

load_dotenv()                       # loads the .env file into your environment (for DB credentials later)

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)      # reads your config file into a Python dictionary


today_date = datetime.today().strftime('%Y-%m-%d')

tickers = sp500_web_scrapper()
start_date = config["start_date"]
end_date = today_date


if __name__ == '__main__':

    def run_pipeline_for_ticker(ticker:str, start_date: str, end_date: str) -> pd.DataFrame:
        df = download_stock_data(ticker, start_date, end_date)
        clean_df = clean_data(df)
        transformed_df = calculate_all_indicators(clean_df)
        #save_to_database(transformed_df, table_name=f'market_data_{ticker}')
        print(transformed_df)
        print(transformed_df.columns)

    #for ticker in tickers:
        # Run pipeline for one ticker ('AAPL')
        #run_pipeline_for_ticker(ticker, start_date, end_date)


    run_pipeline_for_ticker('AAPL', start_date, end_date)
