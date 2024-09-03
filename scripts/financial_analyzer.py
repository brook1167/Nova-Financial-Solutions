import talib as ta
import pandas as pd
import pynance as pn
import numpy as np
import matplotlib.pyplot as plt


def load_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    return df

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

def calculate_financial_metrics(df, risk_free_rate=0.01, rolling_window=30):
     # Calculate daily returns using Adj Close
    df['Daily_Return'] = df['Adj Close'].pct_change()
    
    # Calculate cumulative returns
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
    
    # Calculate volatility (20-day rolling standard deviation of returns)
    df['Volatility'] = df['Daily_Return'].rolling(window=20).std()
    
    # Print all three columns' values
    print("Daily Return Values:")
    print(df[['Daily_Return']].head())  # Print first few rows of Daily_Return
    
    print("\nCumulative Return Values:")
    print(df[['Cumulative_Return']].head())  # Print first few rows of Cumulative_Return
    
    print("\nVolatility Values:")
    print(df[['Volatility']].head())  # Print first few rows of Volatility
    
    return df
    
    

def plot_stock_data(df, ticker):
    plt.figure(figsize=(12, 8))
    plt.plot(df.index, df['Adj Close'], label='Adjusted Close Price')
    plt.plot(df.index, df['SMA_50'], label='50-day SMA')
    plt.title(f'{ticker} Adjusted Stock Price and 50-day SMA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

def plot_financial_metrics(df, ticker):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
    
    ax1.plot(df.index, df['Cumulative_Return'], label='Cumulative Return')
    ax1.set_title(f'{ticker} Financial Metrics')
    ax1.set_ylabel('Cumulative Return')
    ax1.legend()
    
    ax2.plot(df.index, df['Daily_Return'], label='Daily Return')
    ax2.set_ylabel('Daily Return')
    ax2.legend()
    
    ax3.plot(df.index, df['Volatility'], label='Volatility (20-day)')
    ax3.set_ylabel('Volatility')
    ax3.legend()
    calculate_financial_metrics
    plt.xlabel('Date')
    plt.show()

def plot_volume_and_dividends(df, ticker):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    ax1.bar(df.index, df['Volume'], label='Volume')
    ax1.set_title(f'{ticker} Volume and Dividends')
    ax1.set_ylabel('Volume')
    ax1.legend()
    
    ax2.bar(df.index, df['Dividends'], label='Dividends', color='green')
    ax2.set_ylabel('Dividends')
    ax2.legend()
    
    plt.xlabel('Date')
    plt.show()

def plot_time_series_closing_price(df, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'])
    plt.title(f'Time Series of Closing Prices for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.show()

def plot_time_series_volume(df, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Volume'])
    plt.title(f'Time Series of Trading Volume for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.show()


