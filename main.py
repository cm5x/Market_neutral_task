import backtest, data, factor, portfolioGeneration
import ccxt
import pandas as pd
import matplotlib.pyplot as plt
# import openpyxl

# #***************************************


# # Define the symbol and timeframe
# symbol1 = 'UNIUSDT'
# symbol2 = 'ALGOUSDT'
# timeframe = '4h'
# limit = 100 # Adjust the limit based on your historical data requirements

# # Fetch historical data
# historical_data = data.fetch_historical_data_corr(symbol1, symbol2, timeframe, limit) 

# # pd.set_option('display.max_rows', None)
# # pd.set_option('display.max_columns', None)

# # # Fetch historical data with RSI
# # historical_data = data.fetch_historical_data(symbol, timeframe, limit)

# # Backtest the strategy
# backtested_data, trade_data = backtest.backtest_strategy(historical_data)

# # Print the backtested data
# print(backtested_data)
# print(trade_data)

# # Export the DataFrames to Excel files
# excel_file_path_backtest = 'backtested_data_with_changes.xlsx'
# excel_file_path_trade_data = 'trade_data.xlsx'

# backtested_data.to_excel(excel_file_path_backtest)
# trade_data.to_excel(excel_file_path_trade_data)

# print(f"Backtested data with changes has been saved to {excel_file_path_backtest}")
# print(f"Trade data has been saved to {excel_file_path_trade_data}")


# #***************************************

# symbol1 = 'ADA/USDT'
# symbol2 = 'UNI/USDT'
timeframe = '4h'
limit = 1000 # Adjust the limit based on your historical data requirements
div_count = 10 # Adjust count of diversification in portfolio

portfolio = portfolioGeneration.generatePortfolio(div_count) 


trade_changes_data = pd.DataFrame()

totalTradeCount = 0
with pd.ExcelWriter('final_result_data_file.xlsx', engine='xlsxwriter') as writer:
    for i in portfolio:
        symbol1, symbol2 = i.split('/')

            
        # Fetch historical data
        historical_data = data.fetch_historical_data_corr(symbol1, symbol2, timeframe,10 ,limit=1000) 

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)

        # # Fetch historical data with RSI  
        # historical_data = data.fetch_historical_data(symbol, timeframe, limit)

        # Backtest the strategy
        backtested_data, trade_data = backtest.backtest_strategy(historical_data)

        # Print the backtested data
        print(backtested_data)
        print(trade_data)

        

        trade_data['{}_cumulative_proportional_change_pair1'.format(i)] = (1 + trade_data['pair1_trade_change'] / 100).cumprod() - 1 
        trade_data['{}_cumulative_proportional_change_pair2'.format(i)] = (1 + trade_data['pair2_trade_change'] / 100).cumprod() - 1
        


        # Assuming 'i' is a pair name
        trade_changes_data[i] = i
        trade_changes_data.loc['pair1_beta', i] = backtested_data['symbol1_beta'].mean()    
        trade_changes_data.loc['pair2_beta', i] = backtested_data['symbol2_beta'].mean()
        trade_changes_data.loc['pair1_trade_result', i] = 100*trade_data['{}_cumulative_proportional_change_pair1'.format(i)].mean()
        trade_changes_data.loc['pair2_trade_result', i] = 100*trade_data['{}_cumulative_proportional_change_pair2'.format(i)].mean()

        # trade_changes_data['{}_pair1_beta'.format(i)].iloc[0]= backtested_data['symbol1_beta'].mean()
        # trade_changes_data['{}_pair2_beta'.format(i)].iloc[0]= backtested_data['symbol2_beta'].mean()



        # # Append trade changes data to the new DataFrame
        # trade_changes_data = pd.concat([trade_changes_data, trade_data[['pair1_trade_change', 'pair2_trade_change']]])
     
        final_trade_changes_data = 'final_trade_changes_data.xlsx'
        trade_changes_data.to_excel(final_trade_changes_data)

         # Write backtested data to Excel
        backtested_data.to_excel(writer, sheet_name=f'{symbol1}_{symbol2}_Backtested', index=False)

        # Write trade data to Excel
        trade_data.to_excel(writer, sheet_name=f'{symbol1}_{symbol2}_Trades', index=False)
        totalTradeCount += len(trade_data)

portfolioGeneration.hedgeStrategyMain(trade_changes_data)
print('Also, total trade count was', totalTradeCount*2)

