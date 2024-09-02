import talib as ta
import pandas as pd
import matplotlib.pyplot as plt
def technical_indicators(df):
    df['SMA_50'] = ta.SMA(df['Close'], timeperiod=50)
    df['RSI'] = ta.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_Signal'], _ = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return df


def plot_technical_indicators(df):
    df = technical_indicators(df)
    
    plt.figure(figsize=(14, 12))

    # Plot Close Price and SMA
    plt.subplot(3, 1, 1)
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['SMA_50'], label='SMA 50', linestyle='--')
    plt.title('Close Price and SMA 50')
    plt.legend()
    plt.grid()

    # Plot RSI
    plt.subplot(3, 1, 2)
    plt.plot(df.index, df['RSI'], label='RSI', color='orange')
    plt.axhline(y=70, color='red', linestyle='--')
    plt.axhline(y=30, color='green', linestyle='--')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()
    plt.grid()

    # Plot MACD
    plt.subplot(3, 1, 3)
    plt.plot(df.index, df['MACD'], label='MACD', color='blue')
    plt.plot(df.index, df['MACD_Signal'], label='MACD Signal', color='red')
    plt.title('MACD and MACD Signal')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()