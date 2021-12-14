import datetime

import numpy as np

import util.logUtil as log
import matplotlib.pyplot as plt

# pyecharts引用
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line

import easyquotation
# from dbUtil import mysqlUtil
from time import strftime, localtime

from simulationTrader.service import tradeRecordService
from util import stockUtil
from util import ig507Util
from util import tushareUtil

# 开始日期
startDate = "20211213"
# 结束日期
endDate = "20211214"
# 指定开始日期，取得该天买入的证券
codeList = tradeRecordService.getStocksByDate(startDate,"buy")
stocklist = []
for stockCode in codeList:
    stocklist.append(stockUtil.get_complete_stock_code(stockCode[0]))

allStockHistoryDict = tushareUtil.get_all_history(stocklist, startDate, endDate)

print(allStockHistoryDict)

# 遍历所有股票数据
pct_change_sum = 0
for stockCode in allStockHistoryDict.keys():
    pct_change_sum += allStockHistoryDict[stockCode]['20211214']['pct_chg']
    print(allStockHistoryDict[stockCode]['20211214']['pct_chg'])

print("sum:" + str(pct_change_sum))
print("avg:" +  str(pct_change_sum/float(allStockHistoryDict.keys().__len__())))