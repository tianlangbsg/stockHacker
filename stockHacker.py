import datetime
import operator
import threading
import time
import util.logUtil as log

import easyquotation
# from dbUtil import mysqlUtil
from time import strftime, localtime

from entity.AlternativeStockPool import AlternativeStockPool
from simulationTrader.service import alternativeStockPoolService
from util import stockUtil
from util import ig507Util
from util import tushareUtil

quotation = easyquotation.use('qq')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# 股票数据list
rawStockCodeList = []  # 原始不带前缀
stockCodeList = []  # 带前缀
stockHistoryList = []  # 股票历史数据
stockRankList = []  # 股票涨跌幅排行
stockRank100List = []  # 股票涨幅排行前100
# 全股票数据集合
stockHistoryDict = {}  # 股票上个交易日信息
allStockHistoryDict = {}  # 过去指定时间内全部股票信息
stockRealDict = {}  # 股票实时信息
stockRankDict = {}  # 股票涨跌幅排行
stockRank100Dict = {}  # 股票涨幅排行前100
stockTargetDict = {}  # 目标要操作的股票信息（含5档）
candidateList = {}  # 候选股票


# *************************************************************************************
# 标准方法
# *************************************************************************************
# *************************************************************************************

# 刷新获取所有股票数组数据，并保存到stockRealDict, key=stock_code
def get_all_real_and_save(stockCodeListList):
    global stockRealDict
    for stockCodeList in stockCodeListList:
        tempDict = quotation.get_stock_data(stockCodeList)
        for key in tempDict.keys():
            stockData = tempDict[key]
            # 如果该票的key不存在，则跳过
            if stockHistoryDict.get(key) == None:
                continue
            # 如果该票未开盘，则跳过
            if stockData['now'] == None or stockHistoryDict[key]['close'] == None:
                continue
            # 根据上个收盘价，计算当天涨停价格
            stockData['limit_high'] = stockUtil.calc_price_limit_high(stockHistoryDict[key]['close'])
            # 根据上个收盘价，计算当天涨停幅度
            stockData['change_range'] = stockUtil.calc_price_change_range(stockHistoryDict[key]['close'],
                                                                          stockData['now'])
            stockRealDict[key] = stockData


# 刷新获取排名靠前股票数组数据，并保存到stockReal100Dict, key=stock_code
def get_top_real_and_save():
    global stockRank100List
    global stockRank100Dict
    if stockRank100List.__len__() < 1:
        return
    refreshTopTime = datetime.datetime.now()
    tempDict = quotation.get_stock_data(stockRank100List)
    # log.info('Top100行情API获取耗时:' + format((datetime.datetime.now() - refreshTopTime).total_seconds(), '.3f') + 'S')
    stockRank100Dict.clear()
    # 获取最新top100分时价格数据
    for key in tempDict.keys():
        stockData = tempDict[key]
        # 如果该票的key不存在，则跳过
        if stockHistoryDict.get(key) == None:
            continue
        # 如果该票未开盘，则跳过
        if stockData['now'] == None or stockHistoryDict[key]['close'] == None:
            continue
        # 根据上个收盘价，计算当天涨停价格
        stockData['limit_high'] = stockUtil.calc_price_limit_high(stockHistoryDict[key]['close'])
        # 根据上个收盘价，计算当天涨停幅度
        stockData['change_range'] = stockUtil.calc_price_change_range(stockHistoryDict[key]['close'], stockData['now'])
        stockRank100Dict[key] = stockData
    tempDict.clear()
    log.info('Top100行情刷新耗时:' + format((datetime.datetime.now() - refreshTopTime).total_seconds(), '.3f') + 'S')


# 对涨幅前100的进行排序
def sort_stock_rank100():
    global stockRealDict
    global stockRankDict
    global stockRankList
    global stockRank100List
    # 按最新涨跌幅排序
    for key in stockRealDict.keys():
        try:
            stockRankDict[key] = stockRealDict[key]['change_range']
        except:
            log.info(stockRealDict[key])
            stockRealDict[key]['change_range']

    stockRankList = sorted(stockRankDict.items(), key=operator.itemgetter(1), reverse=True)
    stockRank100List.clear()
    for rank in stockRankList[0:100]:
        stockRank100List.append(stockUtil.get_complete_stock_code(rank[0]))


# *************************************************************************************
# 多线程定时执行任务
# *************************************************************************************
# 定时任务，刷新最新股票价格
def refresh_real_info(stockCodeListList):
    global stockRealDict
    global stockRankDict
    global stockRankList
    global stockRank100List

    # 获取最新分时价格数据
    while True:
        try:
            refreshTime = datetime.datetime.now()
            # 更新数据键值对
            get_all_real_and_save(stockCodeListList)
            # log.info('全行情API获取耗时' + format((datetime.datetime.now() - refreshTime).total_seconds(), '.3f') + 'S')
            sort_stock_rank100()
            log.info('全行情刷新耗时' + format((datetime.datetime.now() - refreshTime).total_seconds(), '.3f') + 'S')
            refreshTime = datetime.datetime.now()
            time.sleep(60)
        except Exception as e:
            log.info('全行情刷新失败:' + e)


# 定时任务，刷新接近涨停的前100个股票最新情况
def refresh_top100_info():
    global stockCodeList
    # 获取最新分时价格数据
    while True:
        try:
            # 更新数据键值对
            get_top_real_and_save()
            time.sleep(1)
        except Exception as ex:
            log.error('Top100刷新错误:' + ex.__str__())


# 定时任务，判断top100股票的实时5档行情，并物色合适的待操作目标
def select_target_from_top100():
    global stockRank100Dict
    global candidateList
    while True:
        try:
            time.sleep(1)
            for key in stockRank100Dict.keys():

                # 取出单只股票实时数据
                stockData = stockRank100Dict[key]
                # 取出单只股票过去60日数据
                stockHistory60Data = allStockHistoryDict[key]
                # 判断当前股票是否濒临涨停（ask1在涨停价格上）
                if not stockUtil.is_ask1_at_high_limit(stockData):
                    continue
                # 判断卖一剩余金额是否小于指定数量
                if not stockUtil.ask1_money_less_than_goal(stockData):
                    continue
                # 判断量能是否温和放量
                # if not stockUtil.is_moderate_volume(stockHistory60Data):
                #     continue
                # TODO 判断过去n个交易日内，最高涨幅是否符合1.2倍-1.8倍的区间
                # TODO 判断股票是否创新高
                # TODO 判断当前股票当日内的开板次数
                # TODO 判断当天价格是否是30日内的新高，如果不是，计算出与前高的差距
                # TODO 判断板子上的封单数量是否满足，判断卖一是否金额小于500W
                # TODO 判断所属板块的涨幅，以及所属板块是否是热点
                # TODO 根据首次涨停时间、计算连板数量判断是不是龙头？
                # 判断当前股票当日内是否有过涨停
                # if not stockUtil.has_reached_high_limit(stockData):
                #     continue

                # #################################################################################
                alternativeStock = candidateList[key] = stockRank100Dict[key]
                # 添加到候选股票池
                log.info('选中股票:' + key)
                log.info('实时数据:' + str(candidateList[key]))
                # 添加到候选股票池
                alternativeStockPool = AlternativeStockPool(
                    stock_code=alternativeStock["code"],
                    stock_name=alternativeStock["name"],
                    buy=None,
                    sell=None,
                    now=alternativeStock["now"],
                    open=alternativeStock["open"],
                    close=alternativeStock["close"],
                    high=alternativeStock["high"],
                    low=alternativeStock["low"],
                    turnover=alternativeStock["turnover"],
                    volume=alternativeStock["volume"],
                    ask1=alternativeStock["ask1"],
                    ask1_volume=alternativeStock["ask1_volume"],
                    ask2=alternativeStock["ask2"],
                    ask2_volume=alternativeStock["ask2_volume"],
                    ask3=alternativeStock["ask3"],
                    ask3_volume=alternativeStock["ask3_volume"],
                    ask4=alternativeStock["ask4"],
                    ask4_volume=alternativeStock["ask4_volume"],
                    ask5=alternativeStock["ask5"],
                    ask5_volume=alternativeStock["ask5_volume"],
                    bid1=alternativeStock["bid1"],
                    bid1_volume=alternativeStock["bid1_volume"],
                    bid2=alternativeStock["bid2"],
                    bid2_volume=alternativeStock["bid2_volume"],
                    bid3=alternativeStock["bid3"],
                    bid3_volume=alternativeStock["bid3_volume"],
                    bid4=alternativeStock["bid4"],
                    bid4_volume=alternativeStock["bid4_volume"],
                    bid5=alternativeStock["bid5"],
                    bid5_volume=alternativeStock["bid5_volume"],
                    date=datetime.datetime.now().strftime('%Y%m%d'),
                    time=alternativeStock["datetime"],
                    timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                )
                result = alternativeStockPoolService.insert(alternativeStockPool)
                # #################################################################################
            log.info('********************************************************************')
            log.info(candidateList.keys())
            log.info('********************************************************************')
        except Exception as e:
            log.info('选股失败' + e)

            # TODO


# *************************************************************************************
# *************************************************************************************


# *************************************************************************************
# 主要逻辑
# *************************************************************************************
startTime = localtime()
now = datetime.datetime.now()
today = now.strftime('%Y%m%d')
delta = datetime.timedelta(days=1)
# 如果今天是周一，则自动取得上周五的日期
if(now.weekday()==0):
    delta = datetime.timedelta(days=3)
yesterday = (now - delta).strftime('%Y%m%d')

# 查询当前所有正常上市交易的股票列表ig507
stockCodeList = ig507Util.get_main_stock_list_from_ig507()

# 取得所有主板股票上个交易日的信息，并保存到stockHistoryDict
log.info("初始化上个交易日数据...")
stockHistoryDict = stockUtil.get_history_1(yesterday)
if stockHistoryDict is None:
    stockHistoryDict = tushareUtil.get_last_day_data(yesterday)
    # 将该对象写入到本地，下次启动时可以直接进行读取
    stockUtil.save_history_1(stockHistoryDict, yesterday)
log.info("上个交易日数据初始化完成!")

# 查询主板所有股票过去60个交易日的全部日线信息
log.info("初始化过去60天交易数据...")
end = today
delta = datetime.timedelta(days=60)
start = (now - delta).strftime('%Y%m%d')
# 先判断当前是否存在最新的日线数据文件
allStockHistoryDict = stockUtil.get_history_60()
if allStockHistoryDict is None:
    allStockHistoryDict = tushareUtil.get_all_history(ig507Util.get_main_stock_list_from_ig507(), start, end)
    # 将该对象写入到本地，下次启动时可以直接进行读取
    stockUtil.save_history_60(allStockHistoryDict)
log.info("60天交易数据初始化完成!")

# 初始化今日全部实时行情
# 切割成固定大小的子数组
stockCodeListList = stockUtil.list_split(stockCodeList, 300)
log.info("初始化今日全行情...")
get_all_real_and_save(stockCodeListList)
sort_stock_rank100()
log.info("今日全行情初始化完成!")
log.info("初始化今日Top100行情...")
get_top_real_and_save()
log.info("今日Top100行情初始化完成!")

# 启动全行情刷新线程
log.info("启动全行情刷新线程...")
refreshRealThread = threading.Thread(target=refresh_real_info, args=(stockCodeListList,))
refreshRealThread.start()

# 启动top100行情刷新线程
log.info("启动top100行情刷新线程...")
refreshTop100Thread = threading.Thread(target=refresh_top100_info)
refreshTop100Thread.start()

# 启动top100选择操作目标线程
time.sleep(5)  # 等待实时数据初始化完成
log.info("启动top100选择操作目标线程...")
selectTargetThread = threading.Thread(target=select_target_from_top100())
selectTargetThread.start()



# 启动买卖操作线程
# TODOedd

log.info("系统初始化完成")
