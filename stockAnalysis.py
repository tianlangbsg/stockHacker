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
from util import stockUtil
from util import ig507Util
from util import tushareUtil
from util.commonUtil import get_root_path

quotation = easyquotation.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# 分析历史时长
dayCount = 120

startTime = localtime()
now = datetime.datetime.now()
today = now.strftime('%Y%m%d')
delta = datetime.timedelta(days=1)
# 如果今天是周一，则自动取得上周五的日期
if(now.weekday()==0):
    delta = datetime.timedelta(days=3)
yesterday = (now - delta).strftime('%Y%m%d')

# 初始化过去60天的全部交易数据
end = today
delta = datetime.timedelta(days=dayCount)
start = (now - delta).strftime('%Y%m%d')

allStockHistoryDict = stockUtil.get_history_60()
if allStockHistoryDict is None:
    allStockHistoryDict = tushareUtil.get_all_history(ig507Util.get_main_stock_list_from_ig507(), start, end)
    # 将该对象写入到本地，下次启动时可以直接进行读取
    stockUtil.save_history_60(allStockHistoryDict)
log.info("历史交易数据初始化完成!")

# 存放分析结果
analysisResult = {}
# 存放存在历史涨停板数据
reachHighLimitDict = {}
# 存放历史涨停板收盘数据
closeHighLimitDict = {}
# 存放历史跌停板数据
lowLimitDict = {}

# 遍历所有股票数据
for stockCode in allStockHistoryDict.keys():
    for date in allStockHistoryDict[stockCode].keys():
        # 取得该票每一天的数据
        data = allStockHistoryDict[stockCode][date]
        # 判断该票当天是否是涨停收盘
        if data['close'] == data['limit_high']:
            if not analysisResult.keys().__contains__(date):
                analysisResult[date] = {}
            if not analysisResult[date].keys().__contains__('close_high_limit_count'):
                analysisResult[date]['close_high_limit_count'] = 0
            # 当天涨停计数+1
            analysisResult[date]['close_high_limit_count'] = analysisResult[date]['close_high_limit_count'] + 1
            # 存放到当天的收盘涨停记录中
            if not closeHighLimitDict.keys().__contains__(date):
                closeHighLimitDict[date] = {}
            if not closeHighLimitDict[date].keys().__contains__(stockCode):
                closeHighLimitDict[date][stockCode] = data

        # 判断该票当天是否是存在过涨停
        if data['high'] == data['limit_high']:
            if not analysisResult.keys().__contains__(date):
                analysisResult[date] = {}
            if not analysisResult[date].keys().__contains__('reach_high_limit_count'):
                analysisResult[date]['reach_high_limit_count'] = 0
            # 当天涨停计数+1
            analysisResult[date]['reach_high_limit_count'] = analysisResult[date]['reach_high_limit_count'] + 1
            # 存放到当天的收盘涨停记录中
            if not reachHighLimitDict.keys().__contains__(date):
                reachHighLimitDict[date] = {}
            if not reachHighLimitDict[date].keys().__contains__(stockCode):
                reachHighLimitDict[date][stockCode] = data

        # 判断该票当天是否是跌停收盘
        if data['close'] == data['limit_low']:
            if not analysisResult.keys().__contains__(date):
                analysisResult[date] = {}
            if not analysisResult[date].keys().__contains__('low_limit_count'):
                analysisResult[date]['low_limit_count'] = 0
            # 当天跌停计数+1
            analysisResult[date]['low_limit_count'] = analysisResult[date]['low_limit_count'] + 1
            # 存放到当天的跌停记录中
            if not lowLimitDict.keys().__contains__(date):
                lowLimitDict[date] = {}
            if not lowLimitDict[date].keys().__contains__(stockCode):
                lowLimitDict[date][stockCode] = data

dateList = list(analysisResult.keys())
dateList = sorted(dateList, reverse=False)
codeList = allStockHistoryDict.keys()

preDate = None
preData = {}
# 遍历所有可用交易日期
for date in dateList:
    # 遍历所有的股票代码
    for stockCode in codeList:
        # 取得该票当天的数据
        if allStockHistoryDict[stockCode].keys().__contains__(date):
            data = allStockHistoryDict[stockCode][date]
            # 判断当天的炸板率（判断前一天涨停板买入第二天收盘的差价）
            if data['limit_high'] == data['high'] and data['limit_high'] > data['close']:
                # 炸板计数
                if not analysisResult[date].keys().__contains__('explosion_count'):
                    analysisResult[date]['explosion_count'] = 0
                analysisResult[date]['explosion_count'] = analysisResult[date]['explosion_count'] + 1
                # 总炸板幅度统计
                if not analysisResult[date].keys().__contains__('total_explosion_range'):
                    analysisResult[date]['total_explosion_range'] = float(0)
                analysisResult[date]['total_explosion_range'] = round(
                    analysisResult[date]['total_explosion_range'] + stockUtil.calc_explosion_range(data), 2)
                # 平均开板炸板幅度统计
                analysisResult[date]['avg_explosion_range'] = round(
                    analysisResult[date]['total_explosion_range'] / analysisResult[date]['explosion_count'], 2)
                # 平均封板炸板幅度统计
                analysisResult[date]['avg_all_explosion_range'] = round(
                    analysisResult[date]['total_explosion_range'] / analysisResult[date]['reach_high_limit_count'], 2)

            # 取得该票前一天的数据，如果没有，则暂时不统计
            if preDate is not None and allStockHistoryDict[stockCode].keys().__contains__(preDate):
                preData = allStockHistoryDict[stockCode][preDate]
                if preData['limit_high'] == preData['close']:
                    # 判断当天的打板竞价赚钱效应（判断前一天涨停板买入第二天开盘的差价）
                    if not analysisResult[date].keys().__contains__('total_limit_high_open_range'):
                        analysisResult[date]['total_limit_high_open_range'] = float(0)
                    curOpen = float(data['open'])
                    preClose = float(data['pre_close'])
                    analysisResult[date]['total_limit_high_open_range'] = round(
                        analysisResult[date]['total_limit_high_open_range'] + 100 * (curOpen - preClose) / preClose, 2)
                    analysisResult[date]['avg_limit_high_open_range'] = round(
                        analysisResult[date]['total_limit_high_open_range'] / analysisResult[preDate][
                            'close_high_limit_count'], 2)

                    # 判断当天的打板高点赚钱效应（判断前一天涨停板买入第二天高点的差价）
                    if not analysisResult[date].keys().__contains__('total_limit_high_high_range'):
                        analysisResult[date]['total_limit_high_high_range'] = float(0)
                    curHigh = float(data['high'])
                    preClose = float(data['pre_close'])
                    analysisResult[date]['total_limit_high_high_range'] = round(
                        analysisResult[date]['total_limit_high_high_range'] + 100 * (curHigh - preClose) / preClose, 2)
                    analysisResult[date]['avg_limit_high_high_range'] = round(
                        analysisResult[date]['total_limit_high_high_range'] / analysisResult[preDate][
                            'close_high_limit_count'], 2)

                    # 判断当天的打板收盘赚钱效应（判断前一天涨停板买入第二天收盘的差价）
                    if not analysisResult[date].keys().__contains__('total_limit_high_close_range'):
                        analysisResult[date]['total_limit_high_close_range'] = float(0)
                    curClose = float(data['close'])
                    preClose = float(data['pre_close'])
                    analysisResult[date]['total_limit_high_close_range'] = round(
                        analysisResult[date]['total_limit_high_close_range'] + 100 * (curClose - preClose) / preClose,
                        2)
                    analysisResult[date]['avg_limit_high_close_range'] = round(
                        analysisResult[date]['total_limit_high_close_range'] / analysisResult[preDate][
                            'close_high_limit_count'], 2)

                    # 判断当天的打板竞价亏钱效应（判断前一天涨停板买入第二天低点的差价）
                    if not analysisResult[date].keys().__contains__('total_limit_high_low_range'):
                        analysisResult[date]['total_limit_high_low_range'] = float(0)
                    curlow = float(data['low'])
                    preClose = float(data['pre_close'])
                    analysisResult[date]['total_limit_high_low_range'] = round(
                        analysisResult[date]['total_limit_high_low_range'] + 100 * (curlow - preClose) / preClose, 2)
                    analysisResult[date]['avg_limit_high_low_range'] = round(
                        analysisResult[date]['total_limit_high_low_range'] / analysisResult[preDate][
                            'close_high_limit_count'], 2)

                    # 判断当天的打板高低点中位数赚钱效应（判断前一天涨停板买入第二天高低点中值）
                    if not analysisResult[date].keys().__contains__('total_limit_high_low_middle_range'):
                        analysisResult[date]['total_limit_high_low_middle_range'] = float(0)
                    curMiddle = (float(data['high']) + float(data['low']))/float(2)
                    preClose = float(data['pre_close'])
                    analysisResult[date]['total_limit_high_low_middle_range'] = round(
                        analysisResult[date]['total_limit_high_low_middle_range'] + 100 * (curMiddle - preClose) / preClose, 2)
                    analysisResult[date]['avg_limit_high_low_middle_range'] = round(
                        analysisResult[date]['total_limit_high_low_middle_range'] / analysisResult[preDate][
                            'close_high_limit_count'], 2)
    preDate = date

print(analysisResult)

######################################################################################
######################################################################################
# 日期列表
x1 = dateList

close_high_limit_count_list = []       # 涨停收盘
reach_high_limit_count_list = []       # 盘中到过涨停
low_limit_count_list = []              # 跌停收盘
avg_limit_high_open_range_list = []  # 前一天涨停板买入第二天开盘的差价
avg_limit_high_close_range_list = [] # 前一天涨停板买入第二天收盘的差价
avg_limit_high_high_range_list = []  # 前一天涨停板买入第二天高点的差价
avg_limit_high_low_range_list = []   # 前一天涨停板买入第二天低点的差价

avg_limit_high_low_middle_range_list = []   # 前一天涨停板买入第二天高低点的中位数

for date in dateList:
    if analysisResult.keys().__contains__(date):
        # 涨停收盘
        if analysisResult[date].keys().__contains__('close_high_limit_count'):
            close_high_limit_count_list.append(analysisResult[date]['close_high_limit_count'])
        else:
            close_high_limit_count_list.append(0)

        # 盘中到过涨停
        if analysisResult[date].keys().__contains__('reach_high_limit_count'):
            reach_high_limit_count_list.append(analysisResult[date]['reach_high_limit_count'])
        else:
            reach_high_limit_count_list.append(0)

        # 跌停收盘
        if analysisResult[date].keys().__contains__('low_limit_count'):
            low_limit_count_list.append(analysisResult[date]['low_limit_count'])
        else:
            low_limit_count_list.append(0)

        # 前一天涨停板买入第二天开盘的差价
        if analysisResult[date].keys().__contains__('avg_limit_high_open_range'):
            avg_limit_high_open_range_list.append(analysisResult[date]['avg_limit_high_open_range'])
        else:
            avg_limit_high_open_range_list.append(0)

        # 前一天涨停板买入第二天收盘的差价
        if analysisResult[date].keys().__contains__('avg_limit_high_close_range'):
            avg_limit_high_close_range_list.append(analysisResult[date]['avg_limit_high_close_range'])
        else:
            avg_limit_high_close_range_list.append(0)

        # 前一天涨停板买入第二天高点的差价
        if analysisResult[date].keys().__contains__('avg_limit_high_high_range'):
            avg_limit_high_high_range_list.append(analysisResult[date]['avg_limit_high_high_range'])
        else:
            avg_limit_high_high_range_list.append(0)

        # 前一天涨停板买入第二天低点的差价
        if analysisResult[date].keys().__contains__('avg_limit_high_low_range'):
            avg_limit_high_low_range_list.append(analysisResult[date]['avg_limit_high_low_range'])
        else:
            avg_limit_high_low_range_list.append(0)


        # 前一天涨停板买入第二天低点的中位数
        if analysisResult[date].keys().__contains__('avg_limit_high_low_middle_range'):
            avg_limit_high_low_middle_range_list.append(analysisResult[date]['avg_limit_high_low_middle_range'])
        else:
            avg_limit_high_low_middle_range_list.append(0)


#********************************************************************************
# 使用pyecharts生成图表
#********************************************************************************
columns = []
for date in dateList:
    columns.append(date[4:6] + '-' + date[6:8])

bar = (
    Bar(init_opts=opts.InitOpts(width=str(30*dayCount)+'px',height='900px'))
    .add_xaxis(columns)
    .add_yaxis("涨停收盘数", close_high_limit_count_list, color="#228B22")
    .add_yaxis("盘中涨停数", reach_high_limit_count_list, color="#FF8C00")
    .add_yaxis("跌停收盘数", low_limit_count_list, color="#DC143C")
    .set_global_opts(title_opts=opts.TitleOpts(title="涨停数量分析"), xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}))
)
# bar.render('涨停趋势分析.html')


line = (
    Line()
    .add_xaxis(columns)
    .add_yaxis("涨停开盘", avg_limit_high_open_range_list)
    .add_yaxis("涨停收盘", avg_limit_high_close_range_list)
    .add_yaxis("涨停高点", avg_limit_high_high_range_list)
    .add_yaxis("涨停低点", avg_limit_high_low_range_list)
    .add_yaxis("涨停高低中位数", avg_limit_high_low_middle_range_list)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="涨停趋势分析", pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="48%"),
        xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}, splitline_opts=opts.SplitLineOpts( is_show=True ), ),
        yaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}, splitline_opts=opts.SplitLineOpts(is_show=True), ),
    )
)

filePath = get_root_path() + "\\data\\analysis\\涨停趋势分析"+today+".html";

grid = (
    Grid(init_opts=opts.InitOpts(width=str(30*dayCount)+'px',height='900px'))
    .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
    .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
    .render(filePath)
)

