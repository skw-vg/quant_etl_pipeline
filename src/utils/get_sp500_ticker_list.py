import pandas as pd

def sp500_web_scrapper() -> pd.DataFrame:

    """ Scrapes the latest S&P 500 ticker symbols from Wikipedia.

    Returns:
        List of ticker symbols (str)
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_df = pd.read_html(url)
    ticker_list = sp500_df[0]['Symbol'].tolist()
    return ticker_list
