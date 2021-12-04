# -*- coding: utf-8 -*-
import win32gui

from autoTrader.thsauto import ThsAuto
import ctypes
import win32con
import win32ui

# 获取窗口文本框
from const2 import RADAR_CONTROL_ID_GROUP


def get_text(hwnd):
    length = ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_GETTEXTLENGTH)
    buf = ctypes.create_unicode_buffer(100)
    ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_GETTEXT, length, ctypes.byref(buf))
    return buf.value

if __name__ == '__main__':
    
    # auto = ThsAuto()                                        # 连接客户端

    # radar_hwnd = auto.get_radar_hwnd()
    # print(radar_hwnd)  1316052
    # print(get_text(auto.get_radar_hwnd()))
    # hwnd = win32gui.FindWindow(None, '短线精灵')
    # print(get_text(hwnd))
    # print(hwnd.GetDlgItemText(0x6054C))
    # ctrl = win32gui.GetDlgItem(hwnd, 0x6054C)
    # data = get_text(ctrl)

    w = win32ui.FindWindow(None, '短线精灵')
    print(w.GetDlgItemText(0x60540))  # 获得弹窗里的消息文字

    # print(data)
    # print('可用资金')
    # print(auto.get_balance())                               # 获取当前可用资金
    # print('持仓')
    # print(auto.get_position())                              # 获取当前持有的股票



    # print('卖出')
    # print(auto.sell(stock_no='162411', amount=200, price=0.4035))   # 卖出股票
    #
    # print('买入')
    # result = auto.buy(stock_no='162411', amount=100, price=0.41)    # 买入股票
    # print(result)
    #
    # print('已成交')
    # print(auto.get_filled_orders())                                 # 获取已成交订单
    #
    # print('未成交')
    # print(auto.get_active_orders())                                 # 获取未成交订单
    #
    # if result and result['code'] == 0:                                # 如果买入下单成功，尝试撤单
    #     print('撤单')
    #     print(auto.cancel(entrust_no=result['entrust_no']))

