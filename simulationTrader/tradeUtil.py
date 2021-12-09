import datetime
from entity.TradeRecord import TradeRecord
from simulationTrader.service import tradeRecordService


def buyStock(stockData):
    # 查询当日是否已经购买该票
    todayTradeRecords = tradeRecordService.getByDate(datetime.datetime.now().strftime('%Y%m%d'))

    # TODO
    if todayTradeRecords.__contains__('000001'):
        print('a')

    # 买入股票测试
    tradeRecord = TradeRecord(
        stock_code='000892',
        stock_name='20211209',
        detail='',
        trade_price='',
        trade_amount='',
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
    )
    tradeRecordService.insert(tradeRecord)


buyStock(None)