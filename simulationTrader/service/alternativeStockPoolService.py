from util import mysqlUtil


def getAll():
    # 定义要执行的SQL语句
    sql = """
          select * from alternative_stock_pool
          """
    # 取到查询结果
    result = mysqlUtil.query(sql)
    print(result)
    return result


def insert(alternativeStockPool):
    # 定义要执行的SQL语句
    sql = 'insert into alternative_stock_pool (stock_code,stock_name,buy,sell,now,open,close,high,low,turnover,volume,ask1,ask1_volume,ask2,ask2_volume,ask3,ask3_volume,ask4,ask4_volume,ask5,ask5_volume,bid1,bid1_volume,bid2,bid2_volume,bid3,bid3_volume,bid4,bid4_volume,bid5,bid5_volume,date,time,timestamp) ' \
          'values ' \
          '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
          '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
          '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
          '%s,%s,%s,%s);'

    params = [alternativeStockPool.stock_code, alternativeStockPool.stock_name, alternativeStockPool.buy,
              alternativeStockPool.sell, alternativeStockPool.now, alternativeStockPool.open,
              alternativeStockPool.close, alternativeStockPool.high, alternativeStockPool.low,
              alternativeStockPool.turnover, alternativeStockPool.volume, alternativeStockPool.ask1,
              alternativeStockPool.ask1_volume, alternativeStockPool.ask2, alternativeStockPool.ask2_volume,
              alternativeStockPool.ask3, alternativeStockPool.ask3_volume, alternativeStockPool.ask4,
              alternativeStockPool.ask4_volume, alternativeStockPool.ask5, alternativeStockPool.ask5_volume,
              alternativeStockPool.bid1, alternativeStockPool.bid1_volume, alternativeStockPool.bid2,
              alternativeStockPool.bid2_volume, alternativeStockPool.bid3, alternativeStockPool.bid3_volume,
              alternativeStockPool.bid4, alternativeStockPool.bid4_volume, alternativeStockPool.bid5,
              alternativeStockPool.bid5_volume, alternativeStockPool.date, alternativeStockPool.time,
              alternativeStockPool.timestamp]

    result = mysqlUtil.execute(sql, params)
    return result
