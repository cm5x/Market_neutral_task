import requests
import numpy as np
import pandas as pd
import ccxt
import data

def calculate_rsi(df, period=14):
    df['price_change'] = df['close'].diff()
    df['gain'] = df['price_change'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['price_change'].apply(lambda x: abs(x) if x < 0 else 0)

    avg_gain = df['gain'].rolling(window=period).mean()
    avg_loss = df['loss'].rolling(window=period).mean()

    relative_strength = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + relative_strength))

    df.drop(['price_change', 'gain', 'loss'], axis=1, inplace=True)

    return rsi


    
def calculate_price_change(df):
    # Calculate price change
    price_change = df['close'].diff()

    return price_change   



def calculate_proportional_difference(df):
    # Calculate proportional difference
    close_prices = df['close']
    proportional_difference = close_prices.pct_change() * 100  # Multiply by 100 to get percentage

    return proportional_difference


def calculate_correlation(df, data_count, limit = 1000 ):
    correlation_coefficients = []
    # Initialize an empty list to store correlation coefficients
    for i in range(1, data_count + 1,1 ):
        correlation_coefficients.append(0)


    # Iterate over rows in the DataFrame
    for i in range(data_count, len(df)):
        # Extract the last data_count elements for each column
        window1 = df['change%'].iloc[i - data_count:i]
        window2 = df['symbol2_change%'].iloc[i - data_count:i]

        # Calculate correlation coefficient for the current row
        correlation_coefficient = np.corrcoef(window1, window2)[0, 1]
        correlation_coefficients.append(correlation_coefficient)

    return correlation_coefficients

def calculate_beta(df, data_count, limit =1000):
    
    beta = []

    for i in range(1, data_count + 1,1 ):
        beta.append(0)

    for i in range(data_count, len(df)):
        # Extract the last data_count elements for each column
        window1 = df['change%'].iloc[i - data_count:i]
        window2 = df['btc_market_main_change%'].iloc[i - data_count:i]

        covariance = np.cov(window1, window2)[0, 1]
        market_variance = np.var(window2)

        beta_value = covariance/market_variance
        beta.append(beta_value)

    return beta

def calculate_beta_for_symbol2(df, data_count, limit =1000):
    
    beta = []

    for i in range(1, data_count + 1,1 ):
        beta.append(0)

    for i in range(data_count, len(df)):
        # Extract the last data_count elements for each column
        window1 = df['symbol2_change%'].iloc[i - data_count:i]
        window2 = df['btc_market_main_change%'].iloc[i - data_count:i]

        covariance = np.cov(window1, window2)[0, 1]
        market_variance = np.var(window2)

        beta_value = covariance/market_variance
        beta.append(beta_value)

    return beta
