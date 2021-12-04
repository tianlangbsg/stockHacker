import pymysql
from config import configManager
from util import stockUtil

DATABASE_HOST = configManager.get(section='database', option='database_host')
DATABASE_PORT = configManager.get_int(section='database', option='database_port')
DATABASE_USERNAME = configManager.get(section='database', option='database_username')
DATABASE_PASSWORD = configManager.get(section='database', option='database_password')
DATABASE_NAME = configManager.get(section='database', option='database_name')
DATABASE_CHARSET = configManager.get(section='database', option='database_charset')

conn = pymysql.connect(
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    user =DATABASE_USERNAME, password = DATABASE_PASSWORD,
    database = DATABASE_NAME,
    charset =DATABASE_CHARSET)


# 执行SQL
def execute(sql,params):
    cursor = conn.cursor()  # 获取一个光标
    cursor.execute(sql,params)
    result = conn.commit()
    cursor.close()
    return result


# 查询SQL
def query(sql):
    cursor = conn.cursor()
    # 执行sql语句
    cursor.execute(sql)
    # 取到查询结果
    result = cursor.fetchall()
    return result


def getTickData():
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示

    # 定义要执行的SQL语句
    sql = """
          SELECT * from tick_data
          """
    # 拼接并执行sql语句
    cursor.execute(sql)
    # 取到查询结果
    ret1 = cursor.fetchall()
    print(ret1)
    return ret1


def insertTickData(stock_code,stock_name,buy=None,sell=None,now=None,open=None,close=None,high=None,low=None,turnover=None,volume=None,
                   ask1=None,ask1_volume=None,ask2=None,ask2_volume=None,ask3=None,ask3_volume=None,ask4=None,ask4_volume=None,
                   ask5=None,ask5_volume=None,bid1=None,bid1_volume=None,bid2=None,bid2_volume=None,bid3=None,bid3_volume=None,
                   bid4=None,bid4_volume=None,bid5=None,bid5_volume=None,date=None,time=None,timestamp=None):
    cursor = conn.cursor()  # 获取一个光标
    sql = 'insert into tick_data (stock_code,stock_name,buy,sell,now,open,close,high,low,turnover,volume,ask1,ask1_volume,ask2,ask2_volume,' \
          'ask3,ask3_volume,ask4,ask4_volume,ask5,ask5_volume,bid1,bid1_volume,bid2,bid2_volume,bid3,bid3_volume,bid4,bid4_volume,' \
          'bid5,bid5_volume,date,time,timestamp) ' \
          'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'

    cursor.execute(sql, [stock_code,stock_name,buy,sell,now,open,close,high,low,turnover,volume,ask1,ask1_volume,ask2,ask2_volume,
                         ask3,ask3_volume,ask4,ask4_volume,ask5,ask5_volume,bid1,bid1_volume,bid2,bid2_volume,bid3,bid3_volume,
                         bid4,bid4_volume,bid5,bid5_volume,date,time,timestamp])
    conn.commit()
    cursor.close()


def insertHistoryData(stock_code,stock_name,buy=None,sell=None,now=None,open=None,close=None,high=None,low=None,turnover=None,volume=None,
                   ask1=None,ask1_volume=None,ask2=None,ask2_volume=None,ask3=None,ask3_volume=None,ask4=None,ask4_volume=None,
                   ask5=None,ask5_volume=None,bid1=None,bid1_volume=None,bid2=None,bid2_volume=None,bid3=None,bid3_volume=None,
                   bid4=None,bid4_volume=None,bid5=None,bid5_volume=None,date=None,time=None,timestamp=None):
    cursor = conn.cursor()  # 获取一个光标
    sql = 'insert into tick_data (stock_code,stock_name,buy,sell,now,open,close,high,low,turnover,volume,ask1,ask1_volume,ask2,ask2_volume,' \
          'ask3,ask3_volume,ask4,ask4_volume,ask5,ask5_volume,bid1,bid1_volume,bid2,bid2_volume,bid3,bid3_volume,bid4,bid4_volume,' \
          'bid5,bid5_volume,date,time,timestamp) ' \
          'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'

    cursor.execute(sql, [stock_code,stock_name,buy,sell,now,open,close,high,low,turnover,volume,ask1,ask1_volume,ask2,ask2_volume,
                         ask3,ask3_volume,ask4,ask4_volume,ask5,ask5_volume,bid1,bid1_volume,bid2,bid2_volume,bid3,bid3_volume,
                         bid4,bid4_volume,bid5,bid5_volume,date,time,timestamp])
    conn.commit()
    cursor.close()

# insertTickData(stock_code=600111,open=59.56,close= 59.56,now=61.01)

# 获取全部股票列表
def getStockList():
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示

    # 定义要执行的SQL语句
    sql = """
          SELECT stock_code from stock_info
          """
    # 拼接并执行sql语句
    cursor.execute(sql)
    # 取到查询结果
    ret1 = cursor.fetchall()
    return ret1

# 获取所有主板（非ST）股票列表
def getMainBoardStockList():
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示

    # 定义要执行的SQL语句
    sql = """
          SELECT * FROM stock_info WHERE left(stock_code, 3) NOT IN ('300','301','688') AND stock_name NOT LIKE '%S%' AND stock_name NOT LIKE '%*%'
          """
    # 拼接并执行sql语句
    cursor.execute(sql)
    # 取到查询结果
    ret1 = cursor.fetchall()
    rawStockCodeList = []
    stockCodeList = []
    for stockCode in ret1:
        rawStockCodeList.append(stockCode[0])
        # 自动添加sh/sz前缀
        stockCodeList.append(stockUtil.get_complete_stock_code(stockCode[0]))
    return ret1