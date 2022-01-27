# pyecharts引用
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Kline, Page

from simulationTrader.service import tradeRecordService, alternativeStockPoolService
from util import stockUtil, ig507Util
from util import tushareUtil
from util.commonUtil import get_root_path

# 取得所有主板股票代码名称
from util.pyecharts import professionalKlineChart

stockInfoDict = ig507Util.get_main_stock_dict_from_ig507()

# 回溯开始时间，交易开始日期，结束日期
def calcProfit(historyStart, startDate, endDate):
    # 指定开始日期，取得该天买入的证券
    # 标准买入
    tradeRecordDict = tradeRecordService.getByDate(startDate)
    # 20211210前买入
    # codeList = alternativeStockPoolService.getStocksByDate(startDate)
    stocklist = list(tradeRecordDict.keys())
    stocklist = sorted(stocklist, reverse=False)

    # 证券历史数据集
    # indexHistoryDict = tushareUtil.get_index_history(historyStart, endDate) # 沪深指数
    allStockHistoryDict = tushareUtil.get_all_history(stocklist, startDate, endDate) # 交易日开始
    allStockPreHistoryDict = tushareUtil.get_all_history(stocklist, historyStart, endDate) # 交易日前

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
    # 个股利润dict
    single_stock_profit_dict = {}

    # 交易日期dict
    tradeDateDict = {}
    for stockCode in allStockHistoryDict.keys():
        for tradeDate in allStockHistoryDict[stockCode].keys():
            tradeDateDict[tradeDate] = {}
    # 按日期从小到大排序
    tradeDateList = sorted(tradeDateDict.keys(), reverse=False)
    tradeDateList.remove(startDate)

    # 交易日期dict(个股历史K线)
    preTradeDateDict = {}
    for stockCode in allStockPreHistoryDict.keys():
        for tradeDate in allStockPreHistoryDict[stockCode].keys():
            preTradeDateDict[tradeDate] = {}
    # 按日期从小到大排序
    preTradeDateList = sorted(preTradeDateDict.keys(), reverse=False)

    # 总资产
    # totalAssets = 10000 * allStockHistoryDict.keys().__len__()
    totalAssets = tradeRecordService.getTotalAssetsByDate(startDate)[0][0]

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
                # 实际手数个股利润
                open_profit_single = (allStockHistoryDict[stockCode][endDate]['open']-allStockHistoryDict[stockCode][startDate]['high'])*tradeRecordDict[stockCode]['trade_amount']
                high_profit_single = (allStockHistoryDict[stockCode][endDate]['high']-allStockHistoryDict[stockCode][startDate]['high'])*tradeRecordDict[stockCode]['trade_amount']
                low_profit_single = (allStockHistoryDict[stockCode][endDate]['low']-allStockHistoryDict[stockCode][startDate]['high'])*tradeRecordDict[stockCode]['trade_amount']
                close_profit_single = (allStockHistoryDict[stockCode][endDate]['close']-allStockHistoryDict[stockCode][startDate]['high'])*tradeRecordDict[stockCode]['trade_amount']
                if not single_stock_profit_dict.keys().__contains__(stockCode):
                    single_stock_profit_dict[stockCode] = {}
                if not single_stock_profit_dict[stockCode].keys().__contains__(tradeDate):
                    single_stock_profit_dict[stockCode][tradeDate] = {}
                single_stock_profit_dict[stockCode][tradeDate]["open_profit_single"] = open_profit_single
                single_stock_profit_dict[stockCode][tradeDate]["high_profit_single"] = high_profit_single
                single_stock_profit_dict[stockCode][tradeDate]["low_profit_single"] = low_profit_single
                single_stock_profit_dict[stockCode][tradeDate]["close_profit_single"] = close_profit_single
                # 实际手数总利润
                open_profit_sum += open_profit_single
                high_profit_sum += high_profit_single
                low_profit_sum += low_profit_single
                close_profit_sum += close_profit_single
                # 平均金额利润，金额10000
                # open_profit_sum += 10000 * (allStockHistoryDict[stockCode][endDate]['open']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
                # high_profit_sum += 10000 * (allStockHistoryDict[stockCode][endDate]['high']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
                # low_profit_sum += 10000 * (allStockHistoryDict[stockCode][endDate]['low']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
                # close_profit_sum += 10000 * (allStockHistoryDict[stockCode][endDate]['close']-allStockHistoryDict[stockCode][startDate]['high'])/allStockHistoryDict[stockCode][startDate]['high']
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

    print("**************************************************************")
    print(startDate)
    print("初始金额:" + str(totalAssets))
    print("买入数量:" + str(stocklist.__len__()))
    print("open结算金额:" + str(round(totalAssets+open_profit_sum,2)))
    print("high结算金额:" + str(round(totalAssets+high_profit_sum,2)))
    print("low结算金额:" + str(round(totalAssets+low_profit_sum,2)))
    print("close结算金额:" + str(round(totalAssets+close_profit_sum,2)))


    # 实例化page类
    # page = Page(layout=Page.DraggablePageLayout, page_title='打板分析')
    page = Page(page_title=str(startDate))
    filePath = get_root_path() + "\\data\\analysis\\涨停利润趋势分析"+startDate+".html";

    # 利润柱状图
    profit_bar = (
        Bar(init_opts=opts.InitOpts(width='1800px',height='600px'))
        .add_xaxis(tradeDateList)
        .add_yaxis("开盘利润", open_profit_sum_list, color="#696969")
        .add_yaxis("高点利润", high_profit_sum_list, color="#228B22")
        .add_yaxis("低点利润", low_profit_sum_list, color="#AA143C")
        .add_yaxis("收盘利润", close_profit_sum_list, color="#FFD700")
        .set_global_opts(title_opts=opts.TitleOpts(title="涨停利润分析"), xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}))
    )
    page.add(profit_bar)

    # 利润率折线图
    profit_rate_line = (
        Line(init_opts=opts.InitOpts(width='1800px',height='600px'))
        .add_xaxis(tradeDateList)
        .add_yaxis("开盘利润率", open_profit_rate_list, color="#696969")
        .add_yaxis("高点利润率", high_profit_rate_list, color="#228B22")
        .add_yaxis("低点利润率", low_profit_rate_list, color="#AA143C")
        .add_yaxis("收盘利润率", close_profit_rate_list, color="#FFD700")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="涨停利润率分析", pos_top="48%"),
            # legend_opts=opts.LegendOpts(pos_top="48%"),
            xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}, splitline_opts=opts.SplitLineOpts( is_show=True ), ),
            yaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45}, splitline_opts=opts.SplitLineOpts(is_show=True), ),
        )
    )
    page.add(profit_rate_line)

    # 添加个股K线图
    candlestickListDict = {}
    for stockCode in stocklist:
        candlestickList = []
        stockData = allStockPreHistoryDict[stockCode]
        candleStick = professionalKlineChart.draw_kline(stockInfoDict[stockCode], stockData, startDate)
        page.add(candleStick)

    # # 个股K线图
    # candlestickListDict = {}
    # for stockCode in stocklist:
    #     candlestickList = []
    #     stockData = allStockPreHistoryDict[stockCode]
    #     # 取得该股的所有日期数据
    #     preData = [0, 0, 0, 0]  # 上一天的交易数据，当后一天停牌时使用
    #     for date in preTradeDateList:
    #         data = [0, 0, 0, 0]
    #         if allStockPreHistoryDict[stockCode].keys().__contains__(date):
    #             data = [stockData[date]['open'],stockData[date]['close'],stockData[date]['low'],stockData[date]['high']]
    #             preData = data
    #         else:
    #             data = [preData[1],preData[1],preData[1],preData[1]]
    #         candlestickList.append(data)
    #     candlestickListDict[stockCode] = candlestickList
    #
    # xaxisList = preTradeDateList.copy()
    # xaxisList[xaxisList.index(startDate)] = startDate + '★★' # 标记买入当天日期
    #
    # # 添加个股K线图
    # for key in candlestickListDict.keys():
    #     candleStick = (
    #         Kline(init_opts=opts.InitOpts(width='1800px',height='600px'))
    #             .add_xaxis(xaxisList)
    #             .add_yaxis("price", candlestickListDict[key])
    #             .set_global_opts(
    #             title_opts=opts.TitleOpts(title=stockInfoDict[key]),
    #             # legend_opts=opts.LegendOpts(pos_top="48%"),
    #             xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45},
    #                                      splitline_opts=opts.SplitLineOpts(is_show=True), ),
    #             yaxis_opts=opts.AxisOpts(name="日期",  splitline_opts=opts.SplitLineOpts(is_show=True), ),
    #         )
    #     )
    #     page.add(candleStick)


    # 指数K线图
    # for key in indexHistoryDict.keys():
    #     candleStick = (
    #         Kline(init_opts=opts.InitOpts(width='1800px',height='600px'))
    #             .add_xaxis(xaxisList)
    #             .add_yaxis("price", candlestickListDict[key])
    #             .set_global_opts(
    #             title_opts=opts.TitleOpts(title="上证指数"),
    #             xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45},
    #                                      splitline_opts=opts.SplitLineOpts(is_show=True), ),
    #             yaxis_opts=opts.AxisOpts(name="日期",  splitline_opts=opts.SplitLineOpts(is_show=True), ),
    #         )
    #     )
    #     page.add(candleStick)

    # 添加指数K线图
    # for key in indexCandlestickListDict.keys():
    #     candleStick = (
    #         Kline()
    #             .add_xaxis(tradeDateList)
    #             .add_yaxis("price", indexCandlestickListDict[key])
    #             .set_global_opts(
    #             title_opts=opts.TitleOpts(title=key, pos_top="48%"),
    #             legend_opts=opts.LegendOpts(pos_top="48%"),
    #             xaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45},
    #                                      splitline_opts=opts.SplitLineOpts(is_show=True), ),
    #             yaxis_opts=opts.AxisOpts(name="日期", axislabel_opts={"rotate": 45},
    #                                      splitline_opts=opts.SplitLineOpts(is_show=True), ),
    #         )
    #     )
    #     page.add(candleStick)

    dateCount = tradeDateList.__len__()+1
    page.render(filePath)


if __name__ == '__main__':
    # 回溯开始日期
    historyStart = "20211101"
    # 交易开始日期
    startDateList = [
                     # "20211220","20211221", "20211222","20211223","20211224","20211227","20211228","20211229","20211230",
                     # "20211231", "20220104", "20220105", "20220106", "20220107", "20220110", "20220111", "20220112",
                     "20220113","20220114","20220117","20220118","20220119","20220120","20220121","20220124","20220125","20220126"
                     ]
    # 结束日期
    endDate = "20220127"
    for startDate in startDateList:
        calcProfit(historyStart, startDate, endDate)
