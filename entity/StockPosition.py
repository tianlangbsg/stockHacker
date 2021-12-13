class StockPosition:

    """数据库字段名常量"""
    # 股票代码
    STOCK_CODE = "STOCK_CODE"
    # 股票名字
    STOCK_NAME = "STOCK_NAME"
    #市值
    MARKET_VALUE = "MARKET_VALUE"
    #盈亏
    PROFIT = "PROFIT"
    #持仓数量
    POSITION_NUMBER = "POSITION_NUMBER"
    #可用数量
    AVAILABLE_POSITION_NUMBER = "AVAILABLE_POSITION_NUMBER"
    #成本价格
    COST_PRICE = "COST_PRICE"
    #当前价格
    CURRENT_PRICE = "CURRENT_PRICE"
    #当日盈亏
    DAY_PROFIT = "DAY_PROFIT"
    #仓位占比
    POSITION_PROPORTION = "POSITION_PROPORTION"
    #持股天数
    HOLDING_DAY = "HOLDING_DAY"
    #标签
    REMARK = "REMARK"

    """成员变量"""
    stock_code = ""
    stock_name = ""
    market_value = ""
    profit = ""
    position_number = ""
    available_position_number = ""
    cost_price = ""
    current_price = ""
    day_profit = ""
    position_proportion = ""
    holding_day = ""
    remark = ""

    """构造方法"""
    def __init__(self,stock_code,stock_name=None,market_value=None,profit=None,position_number=None,
                 available_position_number=None,cost_price=None,current_price=None,day_profit=None,
                 position_proportion=None,holding_day=None,remark=None):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.market_value = market_value
        self.profit = profit
        self.position_number = position_number
        self.available_position_number = available_position_number
        self.cost_price = cost_price
        self.current_price = current_price
        self.day_profit = day_profit
        self.position_proportion = position_proportion
        self.holding_day = holding_day
        self.remark = remark

    def __str__(self):
        print(self)
