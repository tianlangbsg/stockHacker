import datetime
from entity.TradeRecord import TradeRecord
from simulationTrader.service import tradeRecordService


def buyStock(stockData):
    # 查询当日是否已经购买该票
    todayTradeRecords = tradeRecordService.getBuyRecords(datetime.datetime.now().strftime('%Y%m%d'),stockData.stock_code)

    # 模拟买入股票
    if todayTradeRecords.__len__() > 0:
        return 0

    tradeRecord = TradeRecord(
        stock_code=stockData.stock_code,
        stock_name=stockData.stock_name,
        detail=stockData.bid1_volume,
        trade_type='buy',
        trade_price=stockData.now,
        trade_amount=100,
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    )
    return tradeRecordService.insert(tradeRecord)
