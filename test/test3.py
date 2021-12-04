import easyquotation
from util import mysqlUtil
from time import strftime, localtime


quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# 异步获取股票数组数据
def get_real_and_save(stockCodeList):
    stockRealInfoList = quotation.get_stock_data(stockCodeList)
    # 将数据插入到DB中
    for stockRealInfo in stockRealInfoList:
        v = stockRealInfoList[stockRealInfo]
        mysqlUtil.insertTickData(stockRealInfo, None, v['buy'], v['sell'], v['now'], v['open'], v['close'],
                                 v['high'], v['low'], v['turnover'], v['volume'], v['ask1'], v['ask1_volume'], v['ask2'],
                                 v['ask2_volume'], v['ask3'], v['ask3_volume'], v['ask4'], v['ask4_volume'], v['ask5'],
                                 v['ask5_volume'], v['bid1'], v['bid1_volume'], v['bid2'], v['bid2_volume'], v['bid3'],
                                 v['bid3_volume'], v['bid4'], v['bid4_volume'], v['bid5'], v['bid5_volume'], v['date'],
                                 v['time'], None)


# 切割数组
def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]


# quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
print('mysql耗时')
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
stockCodeInfo = mysqlUtil.getStockList()

# for stockInfo in stockList:
#     print(stockInfo[0])
#     stockInfo = quotation.real(stockInfo[0])  # 支持直接指定前缀，如 'sh000001'

# stockCodeList = []
#
# for stockInfo in stockList:
#     stockCodeList.append(str(stockInfo))
#
# stockCodeList = ['sz000001','sz000002','sz000004','sz000005','sz000006']
print('代码拼接处理耗时')
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
i = 0
stockCodeList = []
for stockCode in stockCodeInfo:
    i = i+1
    if i==1000:
        break
    stockCodeList.append(easyquotation.helpers.get_stock_type(stockCode[0]) + stockCode[0])

# stockPartList = list_split(stockCodeList, 7000)
# for stockPart in stockPartList:
#     t = threading.Thread(target=get_real_and_save, args=(stockPart,))
#     t.start()
#
#
# print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
# stockCodeList = ['000001','000002','000004','000005','000006']
# stock_list = quotation.gen_stock_list(stockCodeList)

stockRealInfoList = quotation.get_stock_data(stockCodeList)

print(stockRealInfoList)

# 将数据插入到DB中
# for stockRealInfo in stockRealInfoList:
#     v = stockRealInfoList[stockRealInfo]
#     mysqlUtil.insertTickData(stockRealInfo,None,v['buy'],v['sell'],v['now'],v['open'],v['close'],
#                              v['high'],v['low'],v['turnover'],v['volume'],v['ask1'],v['ask1_volume'],v['ask2'],
#                              v['ask2_volume'],v['ask3'],v['ask3_volume'],v['ask4'],v['ask4_volume'],v['ask5'],
#                              v['ask5_volume'],v['bid1'],v['bid1_volume'],v['bid2'],v['bid2_volume'],v['bid3'],
#                              v['bid3_volume'],v['bid4'],v['bid4_volume'],v['bid5'],v['bid5_volume'],v['date'],
#                              v['time'],None)
#
# print(stockRealInfo)
# print('请求数据耗时')
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))



# stockInfo = quotation.real('000006')  # 支持直接指定前缀，如 'sh000001'
# print(stockInfo)