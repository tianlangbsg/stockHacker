class TradeRecord:

    """数据库字段名常量"""
    # ID
    ID = "ID"
    # 股票代码
    STOCK_CODE = "STOCK_CODE"
    # 股票名字
    STOCK_NAME = "STOCK_NAME"
    # 交易时5档详情
    DETAIL = "DETAIL"
    # 交易价格
    TRADE_PRICE = "TRADE_PRICE"
    # 交易数量
    TRADE_AMOUNT = "TRADE_AMOUNT"
    # 交易日期
    TIMESTAMP = "TIMESTAMP"

    """成员变量"""
    id = ""
    stock_code = ""
    stock_name = ""
    detail = ""
    trade_price = ""
    trade_amount = ""
    timestamp = ""

    """构造方法"""
    def __init__(self, id, stock_code, stock_name=None, detail=None, trade_price=None, trade_amount=None, timestamp=None):
        self.id = id
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.detail = detail
        self.trade_price = trade_price
        self.trade_amount = trade_amount
        self.timestamp = timestamp

    def __str__(self):
        print(self)
