import ccxt
import factor
import pandas as pd
import requests

# Function to fetch historical OHLCV data
def fetch_historical_data(symbol, timeframe, limit=1000):
    binance = ccxt.binance()

    binance.options = {'defaultType': 'future',
                    'adjustForTimeDifference': True}
    
    # Fetch OHLCV data
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # Set timestamp as index
    df.set_index('timestamp', inplace=True)
    df['rsi'] = factor.calculate_rsi(df)
    # df['volatility'] = factor.calculate_volatility(df) 
    df['price change'] = factor.calculate_price_change(df)
    df['change%'] = factor.calculate_proportional_difference(df)
    
    return df


def fetch_historical_data_corr(symbol1, symbol2, timeframe, corr_count, limit=1000):

    print("Fetching data from ccxt.binance...")
    binance = ccxt.binance()

    binance.options = {'defaultType': 'future',
                    'adjustForTimeDifference': True}
    
    # Fetch OHLCV data
    ohlcv = binance.fetch_ohlcv(symbol1, timeframe, limit=limit)
    ohlcv2 = binance.fetch_ohlcv(symbol2, timeframe, limit=limit)
    ohlcv3 = binance.fetch_ohlcv("BTC/USDT", timeframe, limit=limit)

    # Convert to DataFrame
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df2 = pd.DataFrame(ohlcv2, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df3 = pd.DataFrame(ohlcv3, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df2['timestamp'] = pd.to_datetime(df2['timestamp'], unit='ms')
    df3['timestamp'] = pd.to_datetime(df3['timestamp'], unit='ms')
    
    # Set timestamp as index
    df.set_index('timestamp', inplace=True)
    df2.set_index('timestamp', inplace=True)
    df3.set_index('timestamp', inplace=True)

    df['rsi'] = factor.calculate_rsi(df);
    # df['volatility'] = calculate_volatility(df) 
    df['price change'] = factor.calculate_price_change(df);
    df['change%'] = factor.calculate_proportional_difference(df);
    df['symbol2_open'] = df2['open'];
    df['symbol2_close'] = df2['close'];
    df['symbol2_volume'] = df2['volume'];
    df['symbol2_rsi'] = factor.calculate_rsi(df2)
    df['symbol2_change%'] = factor.calculate_proportional_difference(df2);
    df['line_correlation'] = factor.calculate_correlation(df,corr_count);
    

    df['btc_market_main_change%'] = factor.calculate_proportional_difference(df3);
    df['symbol1_beta'] = factor.calculate_beta(df,corr_count)
    df['symbol2_beta'] = factor.calculate_beta_for_symbol2(df,corr_count)
    # df['x'] = factor.calculate_correlation(df,5);

    

    return df

    