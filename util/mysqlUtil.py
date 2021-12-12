import pymysql
from config import configManager

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
    # 获取一个光标
    cursor = conn.cursor()
    result = cursor.execute(sql,params)
    conn.commit()
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
