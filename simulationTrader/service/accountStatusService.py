from entity.AccountStatus import AccountStatus
from util import mysqlUtil


# 查询所有记录
def getAll():
    # 定义要执行的SQL语句
    sql = """
          SELECT * FROM account_status
          """
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


# 查询指定日期记录
def getByDate(date):
    # 定义要执行的SQL语句
    sql = "SELECT * FROM account_status WHERE DATE_FORMAT(timestamp, '%Y%m%d')='" + date + "';"
    # 取到查询结果
    result = mysqlUtil.query(sql)
    return result


# 插入记录
def insert(accountStatus):
    # 定义要执行的SQL语句
    sql = 'INSERT INTO account_status (day,total_assets,fund_balance,stock_market_value,day_profit_loss,' \
          'day_profit_loss_ratio,available_amount,position_profit_loss,frozen_amount,withdrawable_amount) ' \
          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'

    params = [accountStatus.day, accountStatus.total_assets, accountStatus.fund_balance,
              accountStatus.stock_market_value,
              accountStatus.day_profit_loss, accountStatus.day_profit_loss_ratio, accountStatus.available_amount,
              accountStatus.position_profit_loss, accountStatus.frozen_amount, accountStatus.withdrawable_amount]

    result = mysqlUtil.execute(sql, params)
    return result


# 更新记录
def update(accountStatus):
    # 定义要执行的SQL语句
    sql = 'UPDATE account_status SET ' \
          'total_assets=%s,fund_balance=%s,stock_market_value=%s,day_profit_loss=%s,day_profit_loss_ratio=%s,' \
          'available_amount=%s,position_profit_loss=%s,frozen_amount=%s,withdrawable_amount=%s  ' \
          'WHERE day=%s'

    params = [accountStatus.total_assets, accountStatus.fund_balance,
              accountStatus.stock_market_value,
              accountStatus.day_profit_loss, accountStatus.day_profit_loss_ratio, accountStatus.available_amount,
              accountStatus.position_profit_loss, accountStatus.frozen_amount, accountStatus.withdrawable_amount,accountStatus.day, ]

    result = mysqlUtil.execute(sql, params)
    return result

