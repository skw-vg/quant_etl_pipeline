import yfinance as yf
import pandas as pd


def download_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Downloads historical stock data for a given ticker and date range.

    Args:
        ticker (str): Stock symbol (e.g. "AAPL")
        start_date (str): Start date (e.g. "2023-01-01")
        end_date (str): End date (e.g. "2023-12-31")

    Returns:
        pd.DataFrame: Stock data with Date, OHLCV, and Ticker columns
    """

    df = yf.download(ticker, start=start_date, end=end_date)

    # Drop out index level (Ticker) for columns to flatten DataFrame
    df.columns = df.columns.droplevel('Ticker')

    # Reset the index to turn the 'Date' from Index to a column, to make it more database friendly
    df.reset_index(inplace=True)

    # Add ticker symbol as a new column
    df['Ticker'] = ticker

    return df