import json
import requests

from config import configManager

IG507_LICENCE = configManager.get(section='ig507', option='ig507_licence')


# 从IG507获得最新股票列表(主板)
def get_main_stock_list_from_ig507():
    # 设置要访问的地址（这里是get请求）
    url = 'http://ig507.com/data/base/gplist?licence=' + IG507_LICENCE
    # 用自带的json工具把字符串转成字典
    dictinfo = json.loads(requests.get(url).text)
    stockCodeList = []
    for stockInfo in dictinfo:
        if (stockInfo['dm'].startswith('0') or stockInfo['dm'].startswith('6')) and not stockInfo['dm'].startswith(
                '688') \
                and not stockInfo['dm'].startswith('ST') and not stockInfo['dm'].startswith('*'):
            stockCodeList.append(stockInfo['jys'] + stockInfo['dm'])
    return stockCodeList
