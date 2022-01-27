import datetime
import json
import os

import easyquotation


# 根据股票代码，自动补全前缀（600001=>sh600001）
def get_complete_stock_code(stockCode):
    # 自动添加sh/sz前缀
    return easyquotation.helpers.get_stock_type(stockCode) + stockCode


# 转换股票代码格式 sh600001 => 600001.sh
def format_stock_code_suffix(code):
    return code[2:8] + '.' + code[0:2]


# 转换股票代码格式 600001.sh => sh600001
def format_stock_code_prefix(code):
    return code[7:9] + code[0:6]


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
    range = 100 * (price2 - price1) / price1
    return round(range, 2)


# 切割数组
def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


# 保存缓存文件
def save_json_file(jsonObject, path):
    # 将该对象写入到本地
    allStockHistoryDictObj = json.dumps(jsonObject)
    writeFileObj = open(path, 'w')
    writeFileObj.write(allStockHistoryDictObj)
    writeFileObj.close()


# 保存过去60天数据(文件名默认为今天日期)
def save_history_60(jsonObject):
    path = 'data/history/60/' + datetime.datetime.now().strftime('%Y%m%d' + '.json')
    save_json_file(jsonObject, path)


# 获取过去60天数据(文件名默认为今天日期)
def get_history_60():
    path = 'data/history/60/' + datetime.datetime.now().strftime('%Y%m%d' + '.json')
    if os.path.exists(path):
        readFileObj = open(path, 'r')
        return json.load(readFileObj)


# 保存上个交易日数据(文件名默认为今天日期)
def save_history_1(jsonObject, date=datetime.datetime.now().strftime('%Y%m%d' + '.json')):
    path = 'data/history/1/' + date + '.json'
    save_json_file(jsonObject, path)


# 获取指定交易日数据
def get_history_1(date):
    path = 'data/history/1/' + date + '.json'
    if os.path.exists(path):
        readFileObj = open(path, 'r')
        return json.load(readFileObj)
    else:
        return None


# 判断当前股票是否濒临涨停（ask1在涨停价格上）
def is_ask1_at_high_limit(stockData):
    return stockData['ask1'] == stockData['limit_high']


# 判断卖一剩余金额是否小于指定数量
def ask1_money_less_than_goal(stockData):
    ask1Money = stockData['ask1'] * stockData['ask1_volume']
    # 判断卖一剩余单子金额数是否小于1200w
    if ask1Money < 12000000:
        return True
    return False


# 判断当前股票当日内是否有过涨停
def has_reached_high_limit(stockData):
    return stockData['limit_high'] == stockData['high']


# 判断日K期间内的最低价（默认除权）
def get_lowest_price(stockHistory60Data):
    lowestPrice = 999999
    for date in stockHistory60Data.keys():
        curLow = stockHistory60Data[date]['low']
        if lowestPrice > curLow:
            lowestPrice = curLow

    return lowestPrice


# 判断日K期间内的最高价（默认除权）
def get_highest_price(stockHistory60Data):
    highestPrice = 0
    for date in stockHistory60Data.keys():
        curHigh = stockHistory60Data[date]['high']
        if highestPrice < curHigh:
            highestPrice = curHigh

    return highestPrice


# 判断日K期间涨跌幅倍数(价格)
def get_price_increase_times(stockHistory60Data):
    highestPrice = get_highest_price(stockHistory60Data)
    lowestPrice = get_lowest_price(stockHistory60Data)

    return highestPrice / lowestPrice


# 判断日K期间内的最低量（默认除权）
def get_lowest_vol(stockHistory60Data):
    lowestVol = 999999999
    for date in stockHistory60Data.keys():
        curLow = stockHistory60Data[date]['vol']
        if lowestVol > curLow:
            lowestVol = curLow

    return lowestVol


# 判断日K期间内的最高量（默认除权）
def get_highest_vol(stockHistory60Data):
    highestVol = 0
    for date in stockHistory60Data.keys():
        curHigh = stockHistory60Data[date]['vol']
        if highestVol < curHigh:
            highestVol = curHigh

    return highestVol


# 判断日K期间涨跌幅倍数(量能)
def get_vol_increase_times(stockHistory60Data):
    highestVol = get_highest_vol(stockHistory60Data)
    lowestVol = get_lowest_vol(stockHistory60Data)

    return float(highestVol / lowestVol)


# 判断当前股票当日内炸板幅度
def calc_explosion_range(stockData):
    limit_high = float(stockData['limit_high'])
    close = float(stockData['close'])
    return round(100 * (close - limit_high) / limit_high, 2)


# 判断量能是否温和放量
def is_moderate_volume(stockHistory60Data):
    # 最低成交量
    minVol = 0
    # 最高成交量
    maxVol = 0
    # 平均成交量
    avgVol = 0
    # 总成交量
    totalVol = 0

    for date in stockHistory60Data.keys():
        curVol = stockHistory60Data[date]['vol']
        if curVol < minVol:
            minVol = curVol
        if curVol > maxVol:
            maxVol = curVol
        totalVol = totalVol + curVol

    avgVol = totalVol / stockHistory60Data.keys().__len__()

    # 计算最近60个交易日最高量最低量倍数
    volumeRate = maxVol / minVol
    return volumeRate < 4
