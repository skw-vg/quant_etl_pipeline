# INITIAL PROJECT STRUCTURE
```
quant_etl_pipeline/
├── .venv/                <-- virtual environment (local Python + packages)
├── main.py               <-- your main script (starts your pipeline)
├── External Libraries/   <-- PyCharm-managed libraries used in your project
├── Scratches and Consoles <-- notes, experimental code in PyCharm
```
**`.venv/`** - Where Python interpreter and installed packacges live.
Lib/ – Contains installed libraries like pandas, requests, etc.
- `Scripts/` – Contains Python executables and activation scripts
- `pyvenv.cfg` – Config file that tells Python it's a virtual environment
- `.gitignore` – Tells Git to ignore the venv so you don’t commit 1,000s of package files
  - Never commit `.venv/` to GitHub
  - Use `requirements.txt`/`environment.yml` to track environment

**`main.py`** – Your pipeline’s entry point, the main script to run to kick off the pipeline.
- Will call functions like extract_data() -> transform_data() -> load_data()
- Be clean, readable, and as minimal as possible – all the logic should be offloaded to modular files

**External Libraries** – Shows the packages in your .venv, either via pip or conda.
- Pandas, yfinance and slqalchemy

**Scratches and Consoles** – Quick throwaway scripts or exploratory notes, similar to notebooks. Useful for trying things before moving to production code.

---
# DATA ENGINEERING FILE STRUCTURE CONVENTIONS
```
quant_etl_pipeline/
├── .venv/                  		# virtual env (ignored in git)
├── data/                 			# raw and processed data files
│   ├── raw/
│   └── cleaned/
├── src/                   			# all your code
│   ├── ingestion/          		# data downloaders, API connectors
│   ├── transformation/     	# cleaning, processing, feature engineering
│   ├── storage/            		# database connection + write logic
│   └── utils/              		# logging, config loaders, etc.
├── config.yaml             		# project settings like tickers, date ranges
├── .env                    		# secrets (e.g. DB passwords, API keys)
├── main.py                 		# your main pipeline script
├── requirements.txt        		# list of packages
└── README.md               		# overview, instructions, usage
```
---
# STEP 1: ENVIRONMENT SETUP - INSTALLING PYTHON PACKAGES (DEPENDENCIES)
**1.Install via PyCharm terminal:**
```
pip install yfinance pandas sqlalchemy python-dotenv pyyaml
```
If you get an error like pip not recognised try:
```
python -m pip install yfinance pandas sqlalchemy python-dotenv pyyaml
```
**2.Save environment (best practice)**
```
pip freeze > requirements.txt
```
**Python Consolde** – Runs python code interactively. Quickly testing Python scripts, functions or lines.  
**Terminal** – Runs shell/command line (actualy system).  The “control room”. Used for:
- Installing packages (pip install)
- Running scripts (e.g., python main.py)
- Using tools like git, docker or conda
- Managing files and folders (cd, mkdir, ls, etc.)
---
# STEP 2: CREATE config.yaml
**What is `config.yaml`**
Think of it as the “control panel” – you change things here, not inside Pythong code. It’s essentially a configuration file – a place to store values or settings that your code needs, such as:
- Which stock tickers to download
- What date range to use
- File paths
- Column names
- Parameters for functions

**`config.yaml`:**
```
tickers:
  - AAPL
  - MSFT
  - GOOGL

start_date: "2023-01-01"
end_date: "2023-12-31"
```
**How to read `config.yaml` in Python**
Use a package called pyyaml to load this config into Python script. Here’s an example from main.py:
```python
import yaml
# Open the file and load it
with open("config.yaml", "r") as file:
 	config = yaml.safe_load(file)

tickers = config["tickers"]
start_date = config["start_date"]
end_date = config["end_date"]
```
---
# STEP 3: EXTRACTING STOCK DATA (INGESTION)
**Download stock data script in `yfinance_loader.py`:**
```
import yfinance as yf
import pandas as pd


def download_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """python
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
```
**Flatten multi-level index columns**
Initial DataFrame is multi-index with 2 levels [‘Ticker’, ‘Price’], so we want to flatten is an get rid of the first (outer) level ‘Ticker’:
- `df.columns = df.columns.droplevel(‘Ticker’)` or `= df.columns.droplevel(0)`
- Only works if there is only one ticker
**Example using either Python Console or put temporarily in `main.py`:**
```python
If __name__ == ‘__main__’:
  from src.ingestion.yfinance_loader import download_stock_data

  df = download_stock_data("AAPL", "2023-01-01", "2023-12-31")
  print(df.head())
```
**Type Hint (type annotation)**
- `ticker: str, start_date: str, end_date: str1
  - It means: “I expect the `ticker` argument to be a `string`”
  - Does not enforce the type by default
- `-> pd.DataFrame`
  - “This function will return a `pandas.DataFrame`”
  - Just a hint, not a strict rule

**Having date as the index?**
Normally with Time-Series data we want the date to be the index as we can run (model/analysis) operations like:
- `.loc[“2023-06-01”]` to access a specific date (day)
- `.rolling(window=10)` for moving averages (10-day)
- `.resample(“W”)` for weekly aggregates

**Why data engineers reset the index (flatten)?**
1.	Databases (like SQL) don’t understand indexes
    - If we later want to write this DataFrame to a AQL table using `.to_sql()`, the index will be ignored unless expliitely telling pandas to keep it.
2.	Merging/joining multiple dataframes
    - May want to merge price data with metadata (e.g. company names, sector)
    - Combine multiple tickers into one giant table
    - Havging date as a `column` – makes it easier to `merge`, `groupby` or `concat`
3.	Pipelines work better with uniform schemas
    - In a production data pipeline we often clean date, join data, write it into tables or feed to APIs/dashboard. These systems expect the columns to be flat and obvious, not hidden in the index.

Could return both:
```python
df_raw = download_stock_data("AAPL", start, end)
df_time_series = df_raw.set_index("Date")
```
---
# WHAT DOES if__name__ == ‘__main__’: mean?
- Tells your script: “Only run this block of code when you execute this file directly (not when it’s imported into another file).”
    - Can use functions in other scripts without automatically running them
    - You can test things when the script is run directly

**Where and how do you test your function?**
- At the bottom of main.py, you should have your test code under if __name__ == '__main__':
  - This will be the code that runs only when you hit Run on main.py in PyCharm or type python main.py in the terminal
  - Gives you a controlled environment to import data, run cleaning and print results and visually check if it worked

**What is `__name__`?**  
- Every python script has a built in variable called `__name__`
- If you run the script directly, like `python main.py`, Python sets `__name__ =  ‘__main__’`
- If you import that script into another script (like a module), then `__name__ = ‘main.py’`
- Therefore, we check ` if __name__ == ‘__main__’` because we only want certain parts of the code to run when the script is executed directly – not when it is imported as a module
  - This ensures the pipeline runs when you execute the file, but lets other scripts safely import the functions without triggering a full run 

**What code should go below**  
The Golden Rule: Only put code under `__name__ == ‘__main__’:` if you want it to only run when the script is executed directly. Put all your “run this” logic inside:
-Running functions (like calling the pipeline)
- Printing results
- Writing to database
**What code should go above?**  
Code that should always be available, no matter how this file is used:  
- Imports
- Definiging functions or classes
- Reading config files or constants
- Environment setup
























