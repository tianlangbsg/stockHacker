class TradeStockPosition:

    """数据库字段名常量"""
    # 日期
    STOCK_CODE = "STOCK_CODE"
    # 股票代码
    STOCK_CODE = "STOCK_CODE"
    # 股票名字
    STOCK_NAME = "STOCK_NAME"
    # 持仓数量（股）
    STOCK_AMOUNT = "STOCK_AMOUNT"
    # 可买数量（股）
    CAN_SELL_AMOUNT = "CAN_SELL_AMOUNT"
    # 成本价格
    COST_PRICE = "COST_PRICE"
    # 当前价
    CURRENT_PRICE = "CURRENT_PRICE"
    # 浮动盈亏金额
    PL = "PL"
    # 浮动盈亏比例
    PL_RATION = "PL_RATION"
    # 最新市值
    LATEST_MARKET_VALUE = "LATEST_MARKET_VALUE"

    """成员变量"""
    date = ""
    stock_code = ""
    stock_name = ""
    stock_amount = ""
    can_sell_amount = ""
    cost_price = ""
    current_price = ""
    pl = ""
    pl_ration = ""
    latest_market_value = ""

    """构造方法"""
    def __init__(self, date, stock_code, stock_name, stock_amount, can_sell_amount, cost_price, current_price, pl, pl_ration, latest_market_value):
        self.date = date
        self.stock_code = stock_code
        self.stock_name = stock_name

        self.stock_amount = stock_amount
        self.can_sell_amount = can_sell_amount
        self.cost_price = cost_price
        self.current_price = current_price
        self.pl = pl
        self.pl_ration = pl_ration
        self.latest_market_value = latest_market_value

    def __str__(self):
        print(self)
