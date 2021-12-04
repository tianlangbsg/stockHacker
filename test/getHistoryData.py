import tushare as ts

historyData = ts.get_hist_data(code='600848',start='2021-09-17', end='2021-09-17') #一次性获取全部日k线数据

print(historyData)