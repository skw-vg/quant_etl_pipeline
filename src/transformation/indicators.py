import pandas as pd
import numpy as np

# Rolling windows
windows = [5, 10, 20, 50, 100, 200]

# Simple Moving Averages
def calculate_sma(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    return df


# Exponential moving averages
def calculate_ema(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df[f'EMA_{window}'] = df['Close'].ewm(span=window, adjust=False).mean()
    return df


# Calculate Relative Strength Index (RSI)
def calculate_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


# Moving Average Convergence Divergence (MACD)
def calculate_macd(df: pd.DataFrame, short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> pd.DataFrame:
    short_ema = df['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = df['Close'].ewm(span=long_window, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    df['MACD_line'] = macd_line
    df['SIGNAL_line'] = signal_line
    return df

# Bollinger Bands
def calculate_bollinger_bands(df: pd.DataFrame, window: int = 20, num_sd: int = 2) -> pd.DataFrame:
    sma = df['Close'].rolling(window=window).mean()
    rolling_std = df['Close'].rolling(window=window).std()
    upper_band = sma + (rolling_std * num_sd)
    lower_band = sma - (rolling_std * num_sd)
    df['UPPER_band'] = upper_band
    df['LOWER_band'] = lower_band
    return df

# Calculate Average True Range (ATR)
def calculate_atr(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    high = df['High']
    low = df['Low']
    close = df['Close']
    tr = pd.concat([high - low, abs(high - close.shift()), abs(low - close.shift())], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(window=window).mean()
    return tr

# Calculate Average Directional Index (ADX)
def calculate_adx(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    high, low, close = df['High'], df['Low'], df['Close']
    tr = calculate_atr(df, window)
    plus_dm = (high.diff() > low.diff()).astype(float) * (high.diff() - low.diff())
    minus_dm = (low.diff() > high.diff()).astype(float) * (low.diff() - high.diff())
    plus_dm = plus_dm.rolling(window=window).sum()
    minus_dm = minus_dm.rolling(window=window).sum()
    plus_di = 100 * (plus_dm / tr)
    minus_di = 100 * (minus_dm / tr)
    df['ADX'] = 100 * abs((plus_di - minus_di) / (plus_di + minus_di)).rolling(window=window).mean()
    return df

# Calculate Commodity Channel Index (CCI)
def calculate_cci(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    sma = typical_price.rolling(window=window).mean()
    mean_deviation = (typical_price - sma).abs().rolling(window=window).mean()
    df['CCI'] = (typical_price - sma) / (0.015 * mean_deviation)
    return df

# Calculate Rate of Change (ROC)
def calculate_roc(df: pd.DataFrame, periods: int = 10) -> pd.DataFrame:
    df['ROC_10'] = df['Close'].pct_change(periods=10) * 100
    return df

# Calculate Stochastic Oscillator (%K, %D)
def calculate_stochastic_oscillator(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    low_min = df['Low'].rolling(window=window).min()
    high_max = df['High'].rolling(window=window).max()
    df['%K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    df['%D'] = df['%K'].rolling(window=3).mean()
    return df

# Calculate Williams %R
def calculate_williams(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    high_high = df['High'].rolling(window=window).max()
    low_low = df['Low'].rolling(window=window).min()
    df['Williams_%R'] = -100 * ((high_high - df['Close']) / (high_high - low_low))
    return df

# Calculate On-Balance Volume (OBV)
def calculate_obv(df: pd.DataFrame) -> pd.DataFrame:
    df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
    return df

# Calculate Chaikin Money Flow (CMF)
def calculate_cmf(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    mfm = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    mfm = mfm.replace([np.inf, -np.inf], 0).fillna(0)  # Handle divide by zero
    mfv = mfm * df['Volume']
    cmf = mfv.rolling(window=window).sum() / df['Volume'].rolling(window=window).sum()
    df['CMF'] = cmf
    return df


# Calculate Donchian Channels
def calculate_donchian(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df['Donchian_High'] = df['High'].rolling(window=window).max()
    df['Donchian_Low'] = df['Low'].rolling(window=window).min()
    return df


# Run feature engineering calculations
def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # Loop through rolling windows and calculate respective SMA & EMA
    for window in windows:
        calculate_sma(df, window)
        calculate_ema(df, window)

    # Call RSI, MACD & Bollinger Bands
    calculate_rsi(df)
    calculate_macd(df)
    calculate_bollinger_bands(df)
    calculate_atr(df)
    calculate_adx(df)
    calculate_cci(df)
    calculate_roc(df)
    calculate_stochastic_oscillator(df)
    calculate_williams(df)
    calculate_obv(df)
    calculate_cmf(df)
    calculate_donchian(df)

    return df