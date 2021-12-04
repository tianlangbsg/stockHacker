import datetime
import operator
import threading

import easyquotation
from util import mysqlUtil
from time import strftime, localtime
import tushare as ts


quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
# 初始化tushare
tspro = ts.pro_api('679167463f27215174d15fc1f1cb216577b41f5f67d5740acce52f0b')

# 股票数据list
rawStockCodeList = [] # 原始不带前缀
stockCodeList = [] # 带前缀
stockHistoryList = [] # 股票历史数据
stockRankList = [] # 股票涨跌幅排行
stockRank100List = [] # 股票涨幅排行前100
# 全股票数据集合
stockHistoryDict = {} # 股票上个交易日信息
stockRealDict = {} # 股票实时信息
stockRankDict = {} # 股票涨跌幅排行
stockRank100Dict = {} # 股票涨幅排行前100

# 刷新获取所有股票数组数据，并保存到stockRealDict, key=stock_code
def get_all_real_and_save(stockCodeList):
    global stockRealDict
    tempDict = quotation.get_stock_data(stockCodeList)
    for key in tempDict.keys():
        stockData = tempDict[key]
        # 如果该票的key不存在，则跳过
        if stockHistoryDict.get(key) == None:
            continue
        # 如果该票未开盘，则跳过
        if stockData['now']==None or stockHistoryDict[key]['close']==None:
            continue
        # 根据上个收盘价，计算当天涨停价格
        stockData['limit_high'] = calc_price_limit_high(stockHistoryDict[key]['close'])
        # 根据上个收盘价，计算当天涨停幅度
        stockData['change_range'] = calc_price_change_range(stockHistoryDict[key]['close'], stockData['now'])
        stockRealDict[key] = stockData


# 刷新获取排名靠前股票数组数据，并保存到stockReal100Dict, key=stock_code
def get_top_real_and_save():
    global stockRank100List
    global stockRank100Dict
    if stockRank100List.__sizeof__() < 1:
        return
    tempDict = quotation.get_stock_data(stockRank100List)
    for key in tempDict.keys():
        stockData = tempDict[key]
        # 如果该票的key不存在，则跳过
        if stockHistoryDict.get(key) == None:
            continue
        # 如果该票未开盘，则跳过
        if stockData['now']==None or stockHistoryDict[key]['close']==None:
            continue
        # 根据上个收盘价，计算当天涨停价格
        stockData['limit_high'] = calc_price_limit_high(stockHistoryDict[key]['close'])
        # 根据上个收盘价，计算当天涨停幅度
        stockData['change_range'] = calc_price_change_range(stockHistoryDict[key]['close'], stockData['now'])
        stockRank100Dict[key] = stockData

# 切割数组
def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]

# 获取并保存上个交易日的收盘数据
def get_last_day_data(lastDay):
    global stockHistoryDict
    df = tspro.daily(trade_date=lastDay)
    dfList = [tuple(x) for x in df.values]
    for dataSet in dfList:
        stockData = {}
        stockData['ts_code'] = dataSet[0][0:6]
        stockData['trade_date'] = dataSet[1]
        stockData['open'] = dataSet[2]
        stockData['high'] = dataSet[3]
        stockData['low']= dataSet[4]
        stockData['close'] = dataSet[5]
        stockData['pre_close'] = dataSet[6]
        stockData['change'] = dataSet[7]
        stockData['pct_chg'] = dataSet[8]
        stockData['vol'] = dataSet[9]
        stockData['amount'] = dataSet[10]
        # 用字典形式存储上个交易日的数据,key=stock_code
        stockHistoryDict[stockData['ts_code']] = stockData

# 计算涨停价格
def calc_price_limit_high(lastDayClose):
    lastDayClose = float(lastDayClose)
    priceLimit = round((float)(1.1) * lastDayClose, 2)
    return priceLimit

# 计算跌停价格
def calc_price_limit_low(lastDayClose):
    lastDayClose = float(lastDayClose)
    priceLimit = round((float)(0.9) * lastDayClose, 2)
    return priceLimit

# 计算涨跌幅度
def calc_price_change_range(price1, price2):
    price1 = float(price1)
    price2 = float(price2)
    range = 100*(price2-price1)/price1
    return round(range,2)

# *************************************************************************************
# *************************************************************************************
# 定时任务，刷新最新股票价格
def refresh_real_info(stockCodeListList):
    global stockRealDict
    global stockRankDict
    global stockRankList
    global stockRank100List
    # 获取最新分时价格数据
    refreshTime = datetime.datetime.now()
    while True:
        # 更新数据键值对
        for list in stockCodeListList:
            get_all_real_and_save(list)
        # 按最新涨跌幅排序
        # stockRealDict.sort(key='change_range', reverse=True)
        for key in stockRealDict.keys():
            # stockRank = {}
            # stockRank['stock_code'] = stockRealDict[key]['change_range']
            # stockRank['stock_name'] = stockRealDict[key]['name']
            # stockRank['change_range'] = stockRealDict[key]['change_range']
            try:
                # stockRankDict.update(key=stockRealDict[key]['change_range'])
                stockRankDict[key] = stockRealDict[key]['change_range']
            except:
                print(stockRealDict[key])
                stockRealDict[key]['change_range']

        stockRankList = sorted(stockRankDict.items(), key=operator.itemgetter(1), reverse=True)
        for rank in stockRankList[0:100]:
            stockRank100List.append(rank[0])
        print(strftime("全行情刷新：%Y-%m-%d %H:%M:%S", localtime()))
        print(stockRankList)
        print('全行情刷新耗时:' + str((datetime.datetime.now() - refreshTime).total_seconds()) + 'S')
        refreshTime = datetime.datetime.now()


# 定时任务，刷新接近涨停的前100个股票最新情况
def refresh_top100_info():
    global stockCodeList
    # 获取最新分时价格数据
    while True:
        # 更新数据键值对
        get_top_real_and_save()
# *************************************************************************************
# *************************************************************************************

# 取得所有主板股票列表
startTime = localtime()
stockCodeInfo = mysqlUtil.getMainBoardStockList()
for stockCode in stockCodeInfo:
    rawStockCodeList.append(stockCode[0])
    # 自动添加sh/sz前缀
    stockCodeList.append(easyquotation.helpers.get_stock_type(stockCode[0]) + stockCode[0])


# 取得所有主板股票上个交易日的信息，并保存到stockHistoryDict
get_last_day_data('20210923')

# 切割成固定大小的子数组
stockCodeListList = list_split(stockCodeList,800)


refreshRealThread = threading.Thread(target=refresh_real_info, args=(stockCodeListList,))
refreshRealThread.start()

refreshTop100Thread = threading.Thread(target=refresh_top100_info)
refreshTop100Thread.start()

print(strftime("%Y-%m-%d %H:%M:%S", startTime))
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
