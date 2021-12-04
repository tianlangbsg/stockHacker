from util import mysqlUtil


def getAll():
    # 定义要执行的SQL语句
    sql = """
          select * from trade_stock_positions
          """
    # 取到查询结果
    result = mysqlUtil.query(sql)
    print(result)
    return result


def insert(date,stock_code, stock_name=None, can_sell_amount=None,cost_price=None,current_price=None,pl=None,
           pl_ration=None,latest_market_value=None):
    # 定义要执行的SQL语句
    sql = 'insert into trade_stock_positions (date,stock_code, stock_name, can_sell_amount,cost_price,current_price,pl,pl_ration,latest_market_value) ' \
          'values (%s,%s,%s,%s,%s,%s,%s,%s,%s);'

    params = [date,stock_code, stock_name, can_sell_amount,cost_price,current_price,pl,pl_ration,latest_market_value]

    result = mysqlUtil.execute(sql, params)
    return result
