import datetime
import operator
import time
import tushare as tushare
from config import configManager
from util import stockUtil

# 初始化
TUSHARE_TOKEN = configManager.get(section='tushare', option='tushare_token')
tspro = tushare.pro_api(TUSHARE_TOKEN)


# 计算过去n个交易日内最低价格
def get_history_lowest(stockCode, n):
    # 取得当天日期并格式化
    endDay = time.strftime("%Y-%m-%d", time.localtime())
    # 根据n计算出开始日期
    delta = datetime.timedelta(days=n)
    startDay = (datetime.datetime.now() - delta).strftime("%Y-%m-%d")

    historyData = tushare.get_hist_data(code=stockCode, start=startDay, end=endDay)

    # 解析过去的日K线数据，找出历史最低价格
    lowList = historyData['low']
    lowList = sorted(lowList.items(), key=operator.itemgetter(1), reverse=False)
    lowest = lowList[0]
    return lowest


# 计算过去n个交易日内最高价格
def get_history_highest(stockCode, n):
    # 取得当天日期并格式化
    endDay = time.strftime("%Y-%m-%d", time.localtime())
    # 根据n计算出开始日期
    delta = datetime.timedelta(days=n)
    startDay = (datetime.datetime.now() - delta).strftime("%Y-%m-%d")

    historyData = tushare.get_hist_data(code=stockCode, start=startDay, end=endDay)

    # 解析过去的日K线数据，找出历史最高价格
    highList = historyData['high']
    highList = sorted(highList.items(), key=operator.itemgetter(1), reverse=True)
    highest = highList[0]
    return highest


# 取得单个交易日的全部股票数据
def daily(tradeDate):
    return tspro.daily(tradeDate)


# 获取并保存上个交易日的收盘数据
def get_last_day_data(lastDay):
    stockHistoryDict = {}
    df = tspro.daily(trade_date=lastDay)
    dfList = [tuple(x) for x in df.values]
    for dataSet in dfList:
        stockData = {}
        stockData['ts_code'] = dataSet[0][0:6]
        stockData['trade_date'] = dataSet[1]
        stockData['open'] = dataSet[2]
        stockData['high'] = dataSet[3]
        stockData['low'] = dataSet[4]
        stockData['close'] = dataSet[5]
        stockData['pre_close'] = dataSet[6]
        stockData['change'] = dataSet[7]
        stockData['pct_chg'] = dataSet[8]
        stockData['vol'] = dataSet[9]
        stockData['amount'] = dataSet[10]
        # 用字典形式存储上个交易日的数据,key=stock_code
        stockHistoryDict[stockData['ts_code']] = stockData
    return stockHistoryDict


# 获取指定时间段的所有股票数据日k dict
# stockCodes:  000001.SZ,600000.SH,600001.SH
def get_all_history(stockCodeList, startDate, endDate):
    allStockHistoryDict = {}
    # 对stockCodeList进行个数变换，切割为单个size为20的小数组
    stockCodeListList = stockUtil.list_split(stockCodeList, 20)
    # 遍历所有的list
    for list in stockCodeListList:
        # 转换成适合直接调用的str参数
        listStr = ''
        for data in list:
            listStr = listStr + stockUtil.format_stock_code_suffix(data) + ','
        # 传入参数
        df = tspro.query('daily', ts_code=listStr, start_date=startDate, end_date=endDate)
        dfList = [tuple(x) for x in df.values]
        # 用字典形式存储全部历史交易数据,key=stock_code
        for dataSet in dfList:
            stockData = {}
            stockCode = stockData['ts_code'] = dataSet[0][0:6]
            tradeDate = stockData['trade_date'] = dataSet[1]
            stockData['open'] = dataSet[2]
            stockData['high'] = dataSet[3]
            stockData['low'] = dataSet[4]
            stockData['close'] = dataSet[5]
            stockData['pre_close'] = dataSet[6]
            stockData['change'] = dataSet[7]
            stockData['pct_chg'] = dataSet[8]
            stockData['vol'] = dataSet[9]
            stockData['amount'] = dataSet[10]
            stockData['limit_high'] = stockUtil.calc_price_limit_high(dataSet[6])
            stockData['limit_low'] = stockUtil.calc_price_limit_low(dataSet[6])
            if not allStockHistoryDict.keys().__contains__(stockCode):
                allStockHistoryDict[stockCode] = {}
            allStockHistoryDict[stockCode][tradeDate] = stockData

    return allStockHistoryDict
