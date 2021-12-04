class AlternativeStockPool:
    """数据库字段名常量"""
    # 股票代码
    STOCK_CODE = "STOCK_CODE"
    # 股票名字
    STOCK_NAME = "STOCK_NAME"
    # 竞买价
    BUY = "BUY"
    # 竞卖价
    SELL = "SELL"
    # 现价
    NOW = "NOW"
    # 开盘价
    OPEN = "OPEN"
    # 昨日收盘价
    CLOSE = "CLOSE"
    # 今日最高价
    HIGH = "HIGH"
    # 今日最低价
    LOW = "LOW"
    # 交易股数
    TURNOVER = "TURNOVER"
    # 交易金额
    VOLUME = "VOLUME"
    # 卖一价
    ASK1 = "ASK1"
    # 卖一量
    ASK1_VOLUME = "ASK1_VOLUME"
    # 卖二价
    ASK2 = "ASK2"
    # 卖二量
    ASK2_VOLUME = "ASK2_VOLUME"
    # 卖三价
    ASK3 = "ASK3"
    # 卖三量
    ASK3_VOLUME = "ASK3_VOLUME"
    # 卖四价
    ASK4 = "ASK4"
    # 卖四量
    ASK4_VOLUME = "ASK4_VOLUME"
    # 卖五价
    ASK5 = "ASK5"
    # 卖五量
    ASK5_VOLUME = "ASK5_VOLUME"
    # 买一价
    BID1 = "BID1"
    # 买一量
    BID1_VOLUME = "BID1_VOLUME"
    # 买二价
    BID2 = "BID2"
    # 买二量
    BID2_VOLUME = "BID2_VOLUME"
    # 买三价
    BID3 = "BID3"
    # 买三量
    BID3_VOLUME = "BID3_VOLUME"
    # 买四价
    BID4 = "BID4"
    # 买四量
    BID4_VOLUME = "BID4_VOLUME"
    # 买五价
    BID5 = "BID5"
    # 买五量
    BID5_VOLUME = "BID5_VOLUME"
    # 日期
    DATE = "DATE"
    # 时间
    TIME = "TIME"
    # 时间戳
    TIMESTAMP = "TIMESTAMP"

    """成员变量"""
    # 股票代码
    stock_code = ""
    # 股票名字
    stock_name = ""
    # 竞买价
    buy = ""
    # 竞卖价
    sell = ""
    # 现价
    now = ""
    # 开盘价
    open = ""
    # 昨日收盘价
    close = ""
    # 今日最高价
    high = ""
    # 今日最低价
    low = ""
    # 交易股数
    turnover = ""
    # 交易金额
    volume = ""
    # 卖一价
    ask1 = ""
    # 卖一量
    ask1_volume = ""
    # 卖二价
    ask2 = ""
    # 卖二量
    ask2_volume = ""
    # 卖三价
    ask3 = ""
    # 卖三量
    ask3_volume = ""
    # 卖四价
    ask4 = ""
    # 卖四量
    ask4_volume = ""
    # 卖五价
    ask5 = ""
    # 卖五量
    ask5_volume = ""
    # 买一价
    bid1 = ""
    # 买一量
    bid1_volume = ""
    # 买二价
    bid2 = ""
    # 买二量
    bid2_volume = ""
    # 买三价
    bid3 = ""
    # 买三量
    bid3_volume = ""
    # 买四价
    bid4 = ""
    # 买四量
    bid4_volume = ""
    # 买五价
    bid5 = ""
    # 买五量
    bid5_volume = ""
    # 日期
    date = ""
    # 时间
    time = ""
    # 时间戳
    timestamp = ""

    """构造方法"""

    def __init__(self, stock_code, stock_name, buy, sell, now, open, close, high, low, turnover, volume, ask1,
                 ask1_volume, ask2, ask2_volume, ask3, ask3_volume, ask4, ask4_volume, ask5, ask5_volume, bid1,
                 bid1_volume, bid2, bid2_volume, bid3, bid3_volume, bid4, bid4_volume, bid5, bid5_volume, date, time,
                 timestamp):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.buy = buy
        self.sell = sell
        self.now = now
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.turnover = turnover
        self.volume = volume
        self.ask1 = ask1
        self.ask1_volume = ask1_volume
        self.ask2 = ask2
        self.ask2_volume = ask2_volume
        self.ask3 = ask3
        self.ask3_volume = ask3_volume
        self.ask4 = ask4
        self.ask4_volume = ask4_volume
        self.ask5 = ask5
        self.ask5_volume = ask5_volume
        self.bid1 = bid1
        self.bid1_volume = bid1_volume
        self.bid2 = bid2
        self.bid2_volume = bid2_volume
        self.bid3 = bid3
        self.bid3_volume = bid3_volume
        self.bid4 = bid4
        self.bid4_volume = bid4_volume
        self.bid5 = bid5
        self.bid5_volume = bid5_volume
        self.date = date
        self.time = time
        self.timestamp = timestamp

    def __str__(self):
        print(self)
