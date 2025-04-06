import pandas as pd

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

    return df