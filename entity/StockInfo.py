class TradeRecord:

    """数据库字段名常量"""
    # 股票代码
    STOCK_CODE = "STOCK_CODE"
    # 股票名字
    STOCK_NAME = "STOCK_NAME"

    """成员变量"""
    stock_code = ""
    stock_name = ""

    """构造方法"""
    def __init__(self,stock_code, stock_name):
        self.stock_code = stock_code
        self.stock_name = stock_name

    def __str__(self):
        print(self)
