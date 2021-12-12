class AccountStatus:

    """数据库字段名常量"""
    # 日期
    DAY = "DAY"
    # 总资产
    TOTAL_ASSETS = "TOTAL_ASSETS"
    #资金金额
    FUND_BALANCE = "FUND_BALANCE"
    #股票市值
    STOCK_MARKET_VALUE = "STOCK_MARKET_VALUE"
    #当日盈亏
    DAY_PROFIT_LOSS = "DAY_PROFIT_LOSS"
    #当日盈亏比
    DAY_PROFIT_LOSS_RATIO = "DAY_PROFIT_LOSS_RATIO"
    #可用金额
    AVAILABLE_AMOUNT = "AVAILABLE_AMOUNT"
    #持仓盈亏
    POSITION_PROFIT_LOSS = "POSITION_PROFIT_LOSS"
    #冻结金额
    FROZEN_AMOUNT = "FROZEN_AMOUNT"
    #冻结金额
    WITHDRAWABLE_AMOUNT = "WITHDRAWABLE_AMOUNT"

    """成员变量"""
    day = ""
    total_assets = ""
    fund_balance = ""
    stock_market_value = ""
    day_profit_loss = ""
    day_profit_loss_ratio = ""
    available_amount = ""
    position_profit_loss = ""
    frozen_amount = ""
    withdrawable_amount = ""

    """构造方法"""
    def __init__(self,day,total_assets=None,fund_balance=None,stock_market_value=None,day_profit_loss=None,
                 day_profit_loss_ratio=None,available_amount=None,position_profit_loss=None,frozen_amount=None,withdrawable_amount=None,):
        self.day = day
        self.total_assets = total_assets
        self.fund_balance = fund_balance
        self.stock_market_value = stock_market_value
        self.day_profit_loss = day_profit_loss
        self.day_profit_loss_ratio = day_profit_loss_ratio
        self.available_amount = available_amount
        self.position_profit_loss = position_profit_loss
        self.frozen_amount = frozen_amount
        self.withdrawable_amount = withdrawable_amount

    def __str__(self):
        print(self)
