import win32con
import ctypes

import win32gui
from win32api import *
from win32process import *
import win32con

def get_text(hwnd):
    length = ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_GETTEXTLENGTH)
    buf = ctypes.create_unicode_buffer(100)
    ctypes.windll.user32.SendMessageW(hwnd, win32con.WM_GETTEXT, length, ctypes.byref(buf))
    return buf.value

# 获取窗体句柄
# hWnd = GetForegroundWindow()

hWnd = 263900
hwnd = win32gui.FindWindowEx(hWnd, None, u'RICHEDIT50W', None)
print(get_text(hwnd))

FormThreadID = GetCurrentThreadId()
print('FormThreadID: ', FormThreadID)

CWndThreadID = GetWindowThreadProcessId(hWnd)
print('CWndThreadID: ', CWndThreadID)

# AttachThreadInput(CWndThreadID[0], FormThreadID, True)

# 获取光标所在文本框句柄
# hWnd = GetFocus()
# print('hWnd: ', hWnd)

# AttachThreadInput(CWndThreadID[0], FormThreadID, False)

# SendMessage(hWnd, win32con.WM_SETTEXT, 0, "mextb1860 第一个文本框")

# 文本框内容长度
length = SendMessage(hWnd, win32con.WM_GETTEXTLENGTH)+1
print('Length: ', length)

buf = '0'*length
# 生成buffer对象
# buf = PyMakeBuffer(length)

# 获取文本框内容
print('get: ', SendMessage(hWnd, win32con.WM_GETTEXT, length, buf))

print('text: ', buf)