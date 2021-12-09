from util import mysqlUtil


def getAll():
    # 定义要执行的SQL语句
    sql = """
          SELECT * FROM trade_record
          """
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


def getByDate(date):
    # 定义要执行的SQL语句
    sql = "SELECT * FROM trade_record WHERE DATE_FORMAT(timestamp, '%Y%m%d')='"+date+"';"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


def insert(tradeRecord):
    # 定义要执行的SQL语句
    sql = 'INSERT INTO trade_record (stock_code,stock_name,detail,trade_price,trade_amount,timestamp) ' \
          'VALUES (%s,%s,%s,%s,%s,%s);'

    params = [tradeRecord.stock_code, tradeRecord.stock_name, tradeRecord.detail, tradeRecord.trade_price, tradeRecord.trade_amount,tradeRecord.timestamp]

    result = mysqlUtil.execute(sql, params)
    return result
