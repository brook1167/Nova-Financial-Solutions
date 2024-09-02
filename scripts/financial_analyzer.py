import talib as ta
import pandas as pd
def technical_indicators(df):
    df['SMA_50'] = ta.SMA(df['Close'], timeperiod=50)
    df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_Signal'], _ = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return df