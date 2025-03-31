import pandas as pd
from typing import List

def add_moving_averages(
    df: pd.DataFrame,
    column: str = "Close",                                              # default keyword argument
    windows: List[int] = None                                           # default keyword argument
) -> pd.DataFrame:

    if windows is None:
        windows = [5, 10, 20, 50, 100, 200]

    for window in windows:
        # Generate column name, e.g., "SMA,5", "SMA_20, etc.
        col_name = f'SMA_{window}'

        # Calculate the SMA for given window
        df[col_name] = df[column].rolling(window=window).mean()

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans stock data and adds useful features:
    - Drops missing values
    - Adds daily return
    - Adds 10-day moving average

    Args:
         df (pd.DataFrame): Raw stock data

    Returns:
        pd.DataFrame: Cleaned and enriched stock data
    """

    # Drop any rows with missing data (Nan)
    df = df.dropna()

    # Sort date just to be safe
    df = df.sort_values(by='Date')

    # Calculate daily return (percentage change)
    df['Return'] = df['Close'].pct_change().fillna(0)

    # Call helper function - SMA moving average of closing price
    df = add_moving_averages(df)

    return df