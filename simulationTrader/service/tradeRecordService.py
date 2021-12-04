from util import mysqlUtil


def getAll():
    # 定义要执行的SQL语句
    sql = """
          select * from trade_record
          """
    # 取到查询结果
    result = mysqlUtil.query(sql)
    print(result)
    return result


def insert(stock_code, stock_name=None, detail=None, trade_price=None, trade_amount=None):
    # 定义要执行的SQL语句
    sql = 'insert into trade_record (stock_code,stock_name,detail,trade_price,trade_amount) ' \
          'values (%s,%s,%s,%s,%s);'

    params = [stock_code, stock_name, detail, trade_price, trade_amount]

    result = mysqlUtil.execute(sql, params)
    return result
