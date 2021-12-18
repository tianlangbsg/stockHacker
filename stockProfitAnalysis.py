# pyecharts引用
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line


from simulationTrader.service import tradeRecordService, alternativeStockPoolService
from util import stockUtil
from util import tushareUtil
from util.commonUtil import get_root_path

# 开始日期
startDate = "20211216"
# 结束日期
endDate = "20211217"
# 指定开始日期，取得该天买入的证券
# 标准买入
codeList = tradeRecordService.getStocksByDate(startDate, "buy")
# 20211210前买入
# codeList = alternativeStockPoolService.getStocksByDate(startDate)
stocklist = []
for stockCode in codeList:
    stocklist.append(stockUtil.get_complete_stock_code(stockCode[0]))

allStockHistoryDict = tushareUtil.get_all_history(stocklist, startDate, endDate)

print(allStockHistoryDict)
# 利润率
open_profit_rate_list = []
high_profit_rate_list = []
low_profit_rate_list = []
close_profit_rate_list = []
# 利润
open_profit_sum_list = []
high_profit_sum_list = []
low_profit_sum_list = []
close_profit_sum_list = []

# 交易日期dict
tradeDateDict = {}
for stockCode in allStockHistoryDict.keys():
    for tradeDate in allStockHistoryDict[stockCode].keys():
        tradeDateDict[tradeDate] = {}
# 按日期从小到大排序
tradeDateList = sorted(tradeDateDict.keys(), reverse=False)
tradeDateList.remove(startDate)

# 总资产
totalAssets = 10000 * allStockHistoryDict.keys().__len__()

# 遍历所有数据，计算利润和利润率
for tradeDate in tradeDateList:
    endDate = tradeDate
    # 利润率
    open_profit_sum_rate = 0
    high_profit_sum_rate = 0
    low_profit_sum_rate = 0
    close_profit_sum_rate = 0
    # 利润
    open_profit_sum = 0
    high_profit_sum = 0
    low_profit_sum = 0
    close_profit_sum = 0
    stop_count = 0

    for stockCode in allStockHistoryDict.keys():
        if allStockHistoryDict[stockCode].__contains__(endDate):
            # 利润率
            open_profit_sum_rate += (allStockHistoryDict[stockCode][endDate]['open']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
            high_profit_sum_rate += (allStockHistoryDict[stockCode][endDate]['high']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
            low_profit_sum_rate += (allStockHistoryDict[stockCode][endDate]['low']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
            close_profit_sum_rate += (allStockHistoryDict[stockCode][endDate]['close']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
            # 实际手数利润
            # open_profit_sum += (allStockHistoryDict[stockCode][endDate]['open']-allStockHistoryDict[stockCode][startDate]['high'])*100
            # high_profit_sum += (allStockHistoryDict[stockCode][endDate]['high']-allStockHistoryDict[stockCode][startDate]['high'])*100
            # low_profit_sum += (allStockHistoryDict[stockCode][endDate]['low']-allStockHistoryDict[stockCode][startDate]['high'])*100
            # close_profit_sum += (allStockHistoryDict[stockCode][endDate]['close']-allStockHistoryDict[stockCode][startDate]['high'])*100
            # 平均金额利润，金额10000
            open_profit_sum += 10000 * (allStockHistoryDict[stockCode][endDate]['open']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
            high_profit_sum += 10000 * (allStockHistoryDict[stockCode][endDate]['high']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
            low_profit_sum += 10000 * (allStockHistoryDict[stockCode][endDate]['low']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
            close_profit_sum += 10000 * (allStockHistoryDict[stockCode][endDate]['close']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
        else:
            stop_count += 1

    # 利润
    open_profit_sum_list.append(round(open_profit_sum,2))
    high_profit_sum_list.append(round(high_profit_sum,2))
    low_profit_sum_list.append(round(low_profit_sum,2))
    close_profit_sum_list.append(round(close_profit_sum,2))
    # 利润率
    # open_profit_rate_list.append(round(100*open_profit_sum_rate/allStockHistoryDict.keys().__len__(),2))
    # high_profit_rate_list.append(round(100*high_profit_sum_rate/allStockHistoryDict.keys().__len__(),2))
    # low_profit_rate_list.append(round(100*low_profit_sum_rate/allStockHistoryDict.keys().__len__(),2))
    # close_profit_rate_list.append(round(100*close_profit_sum_rate/allStockHistoryDict.keys().__len__(),2))
    open_profit_rate_list.append(round(100*open_profit_sum/totalAssets,2))
    high_profit_rate_list.append(round(100*high_profit_sum/totalAssets,2))
    low_profit_rate_list.append(round(100*low_profit_sum/totalAssets,2))
    close_profit_rate_list.append(round(100*close_profit_sum/totalAssets,2))

print("初始金额:" + str(totalAssets))
print("open结算金额:" + str(round(totalAssets+open_profit_sum,2)))
print("high结算金额:" + str(round(totalAssets+high_profit_sum,2)))
print("low结算金额:" + str(round(totalAssets+low_profit_sum,2)))
print("close结算金额:" + str(round(totalAssets+close_profit_sum,2)))

bar = (
    Bar(init_opts=opts.InitOpts(width='1800px',height='900px'))
    .add_xaxis(tradeDateList)
    .add_yaxis("开盘利润", open_profit_sum_list, color="#696969")
    .add_yaxis("高点利润", high_profit_sum_list, color="#228B22")
    .add_yaxis("低点利润", low_profit_sum_list, color="#AA143C")
    .add_yaxis("收盘利润", close_profit_sum_list, color="#FFD700")
    .set_global_opts(title_opts=opts.TitleOpts(title="涨停利润分析"), xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}))
)

line = (
    Line()
    .add_xaxis(tradeDateList)
    .add_yaxis("开盘利润率", open_profit_rate_list, color="#696969")
    .add_yaxis("高点利润率", high_profit_rate_list, color="#228B22")
    .add_yaxis("低点利润率", low_profit_rate_list, color="#AA143C")
    .add_yaxis("收盘利润率", close_profit_rate_list, color="#FFD700")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="涨停利润率分析", pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="48%"),
        xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}, splitline_opts=opts.SplitLineOpts( is_show=True ), ),
        yaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}, splitline_opts=opts.SplitLineOpts(is_show=True), ),
    )
)

filePath = get_root_path() + "\\data\\analysis\\涨停利润趋势分析"+startDate+".html";


dateCount = tradeDateList.__len__()+1

grid = (
    Grid(init_opts=opts.InitOpts(width=str(dateCount*300)+'px',height='900px',page_title=startDate+'涨停利润趋势分析'))
    .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
    .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
    .render(filePath)
)