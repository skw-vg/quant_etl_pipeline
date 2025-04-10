import pandas as pd


# Create Momentum Trend Confirmation Strategy
def strategy_momentum_trend(df: pd.DataFrame) -> tuple:
    """Ride strong uptrends confirmed by momentum and volume"""
    buy_signal = (
            (df['EMA_20'] > df['EMA_50']) &      # short-term above long-term EMA (trend)
            (df['RSI'] > 55) &                   # positive momentum
            (df['ADX'] > 20) &                   # confirmed trend strength
            (df['CMF'] > 0)                      # buying pressure from volume
    )

    sell_signal = (
            (df['EMA_20'] < df['EMA_50']) |
            (df['RSI'] < 50)
    )

    return buy_signal, sell_signal


# Calculate Mean Reversion (Bollinger Rebound) Strategy
def strategy_mean_reversion(df: pd.DataFrame) -> tuple:
    """Catch reversions after oversold conditions on price and momentum"""
    buy_signal = (
        (df['Close'] < df['LOWER_band']) &      # price is below lower Bollinger Band
        (df['RSI'] < 30) &                      # momentum oversold
        (df['Williams_%R'] < -80)               # deep oversold signal
    )

    sell_signal = (
        (df['Close'] > df['SMA_20']) |          # price reverts to mean
        (df['RSI'] > 50)
    )

    return buy_signal, sell_signal



# Calculate MACD Cross Momentum Strategy
def strategy_macd_cross(df: pd.DataFrame) -> tuple:
    """Capture early trend reversals based on MACD and volume confirmation"""
    buy_signal = (
        (df['MACD_line'] > df['SIGNAL_line']) &                         # MACD crossover
        (df['MACD_line'].shift(1) < df['SIGNAL_line'].shift(1)) &       # confirmed crossover
        (df['Close'] > df['EMA_20']) &                                  # above short-term EMA
        (df['CMF'] > 0)                                                 # buying volume support
    )

    sell_signal = (
        (df['MACD_line'] < df['SIGNAL_line']) &                         # MACD cross down
        (df['MACD_line'].shift(1) > df['SIGNAL_line'].shift(1))
    )

    return buy_signal, sell_signal



# Calculate Breakout Volatility Expansion Strategy
def strategy_volatility_breakout(df: pd.DataFrame) -> tuple:
    """Buy breakouts after tight range and high volume/volatility"""
    atr_mean = df['ATR'].rolling(window=20).mean()

    buy_signal = (
        (df['Close'] > df['Donchian_High']) &    # price breaks above range
        (df['ATR'] > atr_mean) &                 # volatility expanding
        (df['CMF'] > 0) &                        # buying pressure
        (df['ADX'] > 25)                         # strong trend
    )

    sell_signal = (
        (df['Close'] < df['Donchian_Low']) |     # breaks below range
        (df['ADX'] < 20)                         # weak trend
    )

    return buy_signal, sell_signal



# Calculate RSI + Stochastic Crossover Strategy
def strategy_rsi_stochastic(df: pd.DataFrame) -> tuple:
    """Catch reversals using stochastic crossover and supportive RSI"""
    buy_signal = (
        (df['%K'] > df['%D']) &                                # stochastic cross up
        (df['%K'].shift(1) < df['%D'].shift(1)) &              # confirmation
        (df['RSI'] > 40) &                                     # momentum supportive
        (df['CCI'] > -100)                                     # early reversal momentum
    )

    sell_signal = (
        (df['%K'] < df['%D']) &                                # stochastic cross down
        (df['%K'].shift(1) > df['%D'].shift(1))
    )

    return buy_signal, sell_signal



# Calculate Oversold Reversal (Williams + ROC) Strategy
def strategy_oversold_reversal(df: pd.DataFrame) -> tuple:
    """Identify oversold bounces confirmed by ROC and volume"""
    buy_signal = (
        (df['Williams_%R'] < -90) &             # deep oversold
        (df['ROC_10'] > 0) &                    # upward momentum shift
        (df['OBV'].diff() > 0)                  # increasing volume
    )

    sell_signal = (
        (df['Williams_%R'] > -30) |             # momentum overextended
        (df['ROC_10'] < 0)
    )

    return buy_signal, sell_signal



# Calculate ADX Trend + CCI Pullback Strategy
def strategy_adx_cci_pullback(df: pd.DataFrame) -> tuple:
    """Enter dips during strong trends using ADX + CCI"""
    buy_signal = (
        (df['ADX'] > 25) &                      # strong trend
        (df['EMA_20'] > df['EMA_50']) &         # uptrend
        (df['CCI'] < -100)                      # pullback into value
    )

    sell_signal = (
        (df['ADX'] < 20) |                      # trend fading
        (df['CCI'] > 100)                       # price extended
    )

    return buy_signal, sell_signal


# Option 1
def signals_to_weights_loop(df: pd.DataFrame, buy_signal, sell_signal) -> pd.Series:
    position = pd.Series(index=df.index, data=0.0)
    in_position = False

    for i in range(1, len(df)):
        if buy_signal.iloc[i] and not in_position:
            position.iloc[i] = 1.0
            in_position = True
        elif sell_signal.iloc[i] and in_position:
            position.iloc[i] = 0.0
            in_position = False
        else:
            position.iloc[i] = position.iloc[i-1]

    return position


# Option 2
def signals_to_weights_vectorized(df: pd.DataFrame, buy_signal, sell_signal) -> pd.Series:
    signal = pd.Series(index=df.index)

    signal[buy_signal] = 1.0
    signal[sell_signal] = 0.0

    position = signal.ffill().fillna(0.0)

    return position
    
    
    

    
            














