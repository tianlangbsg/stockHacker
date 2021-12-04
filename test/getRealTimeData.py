import easyquotation

quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀

stockInfo = quotation.real('600111') # 支持直接指定前缀，如 'sh000001'

print(stockInfo)