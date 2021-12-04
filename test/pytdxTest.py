from pytdx.hq import TdxHq_API   # pip install pytdx

# 创建API对象
from util import mysqlUtil

api = TdxHq_API()

# if api.connect('119.147.212.81', 7709):
#     # ... some codes...
#     api.disconnect()


# 连接服务器
with api.connect('119.147.212.81', 7709):
    # print(api.get_minute_time_data(1, '600300'))

    stockCodeInfo = mysqlUtil.getMainBoardStockList()

    # 查询分时
    i = 0
    for stockCode in stockCodeInfo:
        realData = api.get_minute_time_data(i, stockCode[0])
        i = i + 1
        print(i)
        print(realData)