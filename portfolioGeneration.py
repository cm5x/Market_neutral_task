from itertools import combinations
import requests
import numpy as np
import data
import pandas as pd

def get_futures_pairs():

    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    data = response.json()

    # Filter for futures contracts
    print("Getting futures pairs...")
    futures_pairs = [symbol['symbol'] for symbol in data['symbols'] if not symbol['symbol'][-1].isdigit()]

    return futures_pairs

# x = get_futures_pairs()
# print(x)
# pairs = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "XRPUSDT", "SUSHIUSDT","UNIUSDT"]



# ####################################

def generatePortfolio(div_count = 10):
    
    # pairs = get_futures_pairs()
    # pairs.remove("BTCUSDT")
    # pairs.remove("ETHUSDT")
    # print(pairs)

    # pairs = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "XRPUSDT", "SUSHIUSDT","UNIUSDT"]
    # pairs = ["XRPUSDT", "ETHUSDT", "ADAUSDT", "XRPUSDT",'BCHUSDT', ]
    # pairs = ['STPTUSDT','XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT', 'BNBUSDT',
    # 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT', 'BATUSDT', 'VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT', 'ALGOUSDT', 'ZILUSDT', 'KNCUSDT', 'ZRXUSDT', 'COMPUSDT',
    # 'OMGUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT', 'RLCUSDT', 'WAVESUSDT', 'MKRUSDT', 'SNXUSDT', 'DOTUSDT', 'DEFIUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT',
    # 'TRBUSDT', 'RUNEUSDT', 'SUSHIUSDT', 'SRMUSDT', 'EGLDUSDT', 'SOLUSDT', 'ICXUSDT', 'STORJUSDT']

    # pairs = ['STPTUSDT','AGLDUSDT','MATICUSDT','APTUSDT','STGUSDT','IOTXUSDT','FRONTUSDT','RAYUSDT','NEARUSDT','AUDIOUSDT','WLDUSDT','DOCKUSDT','MATICUSDT','MATICUSDT',
    #          'STXUSDT','FARMUSDT','DENTUSDT','QIUSDT','ZRXUSDT','IOTXUSDT','IOSTUSDT','SUIUSDT','BCHUSDT','CAKEUSDT','OMGUSDT','HOTUSDT','ASTRUSDT','RSRUSDT','NKNUSDT',
    #          'TWTUSDT','ARUSDT','SEIUSDT','BTCUSDT','CVPUSDT','SUSHIUSDT','ONEUSDT','ALGOUSDT','CFXUSDT','ANKRUSDT','MANAUSDT','MINAUSDT','ATAUSDT','BELUSDT']
    #pairs = ['LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT', 'ADAUSDT', 'XMRUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT']
    # pairs = ['OMGUSDT','HOTUSDT','DENTUSDT','QIUSDT','ZRXUSDT','IOTXUSDT','DOCKUSDT','MATICUSDT','APTUSDT','STGUSDT']
    # pairs = ['STPTUSDT','IOSTUSDT','HOTUSDT','SUIUSDT','QIUSDT','ASTRUSDT']
    pairs = ['STPTUSDT','ZRXUSDT','KEYUSDT','TWTUSDT']
    print("Generating portfolio...")
    combination_pairs = list(combinations(pairs, 2))
    print(combination_pairs)
    dataset = []

    for i in combination_pairs:
        fulldata = data.fetch_historical_data_corr(i[0],i[1],"1h",5)
        correlation_values = fulldata['line_correlation'].tolist()
        correlation_values = [value for value in correlation_values if value != 0.0 and not np.isnan(value)]
        if len(correlation_values)==0:
            break
        
        avg_corr = sum(correlation_values) / len(correlation_values)

        pair = i[0] + "/" + i[1]
        
        dataset.append({'Pair': pair, 'Correlation Value': avg_corr})


    df = pd.DataFrame(dataset)

    df_sorted = df.sort_values(by='Correlation Value', ascending=False)
    # print(df_sorted)
    excel_file_pair_correlations = 'correlation_of_pairs.xlsx'
    df_sorted.to_excel(excel_file_pair_correlations)
    # print(f"Correlation data of pairs has been saved to {excel_file_pair_correlations}")
    
    ##
      
    portfolio = df_sorted['Pair'].tail(div_count)

    return portfolio

##df = trade_changes_data
def hedgeStrategyMain(df, asset=100000, div_count=10):
    
    assetPerPair = asset/div_count

    print("Calculating final trade statistics...")
    
    initialAsset = asset
    # newAsset = asset
    total = 0
    xyz = []
    column_counter = 0
    for column_name, column_data in df.iteritems():
        b1 = column_data.loc['pair1_beta']
        b2 = column_data.loc['pair2_beta']
        
        a1 = (assetPerPair*(b2))/(b1+b2)
        a2 = (assetPerPair*(b1))/(b1+b2)

        a1 = a1*((100+column_data.loc['pair1_trade_result'])/100)
        a2 = a2*((100+column_data.loc['pair2_trade_result'])/100)
        # xyz.append(column_data,a1,a2)
        total += (a1+a2) 
        column_counter += 1
        
    # newAsset = newAsset + total
    # print(xyz)
    # print(total, "total")
        
    total += (div_count-column_counter)*(asset/div_count)

    percentProfit = (total-initialAsset)/(initialAsset)*100
    print("Initial asset was ", asset, ";Total asset is ",total, " now.")
    print("Percent profit is %", percentProfit)
    return total
