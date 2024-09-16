# Task : Market Neutral Strategy for Cryptomarket & Backtesting

This repository includes code of practically manual backtesting algorithm based on time-series based price data. Also includes extra functions enables to get correlation values of pairs to enhance market neutral strategy.

Strategy is based on taking advantage of negative correlation between crypto pairs, taking position with regard to market neutral strategy principles. RSI is used at the stage of position taking decision, to examplify as simple and general. 

## PARTS

1. Create combination of all futures pairs in Binance market. Compare them and achieve the most negative correlated pairs.
2. Fetch OHLCV data of chosen pairs and process the data in Dataframe structure. All datas are stored and processed in dataframe structure.
3. By processing OHLCV data, getting necessary data: RSI, Correlation data, Beta value data.
4. Generate backtesting method for pairs, RSI has been used. 
5. In backtesting, all system was built for market neutral strategy principles. Also diversification in portfolio has been provided.
6. Common performance metrics returned. Also via excel format, all data is achievable and workable.


