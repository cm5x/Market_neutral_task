import pandas as pd

# Function to backtest the strategy
def backtest_strategy(df):

    print("Backtesting the strategy...")

    df['pair1_position'] = 0  # 0 indicates no position, 1 indicates long (buy), -1 indicates short (sell)
    df['pair2_position'] = 0
    df['position_index'] = 0  # Position index
    df['pair1_entry_price'] = 0.0 
    df['pair1_exit_price'] = 0.0  
    df['pair1_trade_change'] = 0.0 
    df['pair2_entry_price'] = 0.0  
    df['pair2_exit_price'] = 0.0  
    df['pair2_trade_change'] = 0.0  
    pair1_current_position = 0
    pair2_current_position = 0
    last_open = 0
    # DataFrame to store trade-related data
    trade_data = pd.DataFrame(columns=['position_index', 'entry_time', 'exit_time', 'pair1_entry_price', 'pair1_exit_price', 'pair1_trade_change', 'pair2_entry_price', 'pair2_exit_price', 'pair2_trade_change' ])

    trade_data['position_index'] = 0
    trade_data['entry_time'] = 0
    trade_data['exit_time'] = 0
    trade_data['pair1_entry_price'] = 0.0
    trade_data['pair1_exit_price'] = 0.0
    trade_data['pair1_trade_change'] = 0.0
    trade_data['pair2_entry_price'] = 0.0 
    trade_data['pair2_exit_price'] = 0.0  
    trade_data['pair2_trade_change'] = 0.0 
 

    for i in range(1, len(df)):
        #if (df['rsi'][i] > 60) & (df['symbol2_rsi'] < 40) & (pair1_current_position == 0):
        if (df['rsi'][i] > 60) & (pair1_current_position == 0):
            if (df['open'][i] != 0) & (df['symbol2_open'][i] != 0):
                if (df['symbol2_rsi'][i]<40):
                    df['pair1_position'][i] = 1
                    df['pair2_position'][i] = df['pair1_position'][i]*(-1)
                    pair1_current_position = 1
                    pair2_current_position = pair2_current_position*(-1)
                    df['position_index'][i] = df['position_index'][i - 1] + 1
                    df['pair1_entry_price'][i] = df['close'][i]
                    df['pair2_entry_price'][i] = df['symbol2_close'][i]
            
            # last_open  = df['close'][i]
        # elif (df['rsi'][i] < 40) & (df['symbol2_rsi'] > 60) & (pair1_current_position == 0): 
        elif (df['rsi'][i] < 40) & (pair1_current_position == 0): 
            if (df['open'][i] != 0) & (df['symbol2_open'][i] != 0):
                if (df['symbol2_rsi'][i]>60):
                    df['pair1_position'][i] = -1
                    df['pair2_position'][i] = df['pair1_position'][i]*(-1)
                    pair1_current_position = -1
                    pair2_current_position = pair2_current_position*(-1)
                    df['position_index'][i] = df['position_index'][i - 1] + 1
                    df['pair1_entry_price'][i] = df['close'][i]
                    df['pair2_entry_price'][i] = df['symbol2_close'][i]
                    #last_open = df['close'][i]
        elif (df['pair1_position'][i - 1] == 1) & (df['rsi'][i] < 55):
            df['pair1_position'][i] = 0
            df['pair2_position'][i] = df['pair1_position'][i]*(-1)
            pair1_current_position = 0
            pair2_current_position = pair2_current_position*(-1)
            df['position_index'][i] = df['position_index'][i - 1]
            df['pair1_exit_price'][i] = df['close'][i]
            df['pair2_exit_price'][i] = df['symbol2_close'][i]
            df['pair1_entry_price'][i] = df['pair1_entry_price'][i-1]
            df['pair2_entry_price'][i] = df['pair2_entry_price'][i-1]
            df['pair1_trade_change'][i] = ((df['pair1_exit_price'][i] - df['pair1_entry_price'][i]) / df['pair1_entry_price'][i]) * 100
            df['pair2_trade_change'][i] = ((df['pair2_entry_price'][i] - df['pair2_exit_price'][i]) / df['pair2_entry_price'][i] ) * 100
            # Record trade data in the trade_data DataFrame
            trade_data = trade_data.append({
                'position_index': df['position_index'][i],
                'entry_time': df.index[i - 1],
                'exit_time': df.index[i],
                'pair1_entry_price': df['pair1_entry_price'][i],
                'pair2_entry_price': df['pair2_entry_price'][i],
                'pair1_exit_price': df['pair1_exit_price'][i],
                'pair2_exit_price': df['pair2_exit_price'][i],
                'pair1_trade_change': df['pair1_trade_change'][i],
                'pair2_trade_change': df['pair2_trade_change'][i]
            }, ignore_index=True)
        elif (df['pair1_position'][i - 1] == -1) & (df['rsi'][i] > 45):
            df['pair1_position'][i] = 0
            df['pair2_position'][i] = df['pair1_position'][i]*(-1)
            pair1_current_position = 0
            pair2_current_position = pair2_current_position*(-1)
            df['position_index'][i] = df['position_index'][i - 1]
            df['pair1_exit_price'][i] = df['close'][i]
            df['pair2_exit_price'][i] = df['symbol2_close'][i]
            df['pair1_entry_price'][i] = df['pair1_entry_price'][i-1]
            df['pair2_entry_price'][i] = df['pair2_entry_price'][i-1]
            df['pair1_trade_change'][i] = ((df['pair1_entry_price'][i] - df['pair1_exit_price'][i]) / df['pair1_entry_price'][i] ) * 100
            df['pair2_trade_change'][i] = ((df['pair2_exit_price'][i] - df['pair2_entry_price'][i]) / df['pair2_entry_price'][i]) * 100

            # Record trade data in the trade_data DataFrame
            trade_data = trade_data.append({
                'position_index': df['position_index'][i],
                'entry_time': df.index[i - 1],
                'exit_time': df.index[i],
                'pair1_entry_price': df['pair1_entry_price'][i],
                'pair2_entry_price': df['pair2_entry_price'][i],
                'pair1_exit_price': df['pair1_exit_price'][i],
                'pair2_exit_price': df['pair2_exit_price'][i],
                'pair1_trade_change': df['pair1_trade_change'][i],
                'pair2_trade_change': df['pair2_trade_change'][i]
            }, ignore_index=True)
        else:
            df['pair1_position'][i] = df['pair1_position'][i - 1]
            df['pair2_position'][i] = df['pair2_position'][i - 1]
            df['position_index'][i] = df['position_index'][i - 1]
            df['pair1_entry_price'][i] = df['pair1_entry_price'][i-1]
            df['pair2_entry_price'][i] = df['pair2_entry_price'][i-1]
    
    return df, trade_data



