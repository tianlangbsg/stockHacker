import configparser

#  实例化configParser对象
from util.commonUtil import get_root_path

config = configparser.ConfigParser()

config_path = get_root_path() + '\\config\\config.ini'
# -read读取ini文件
config.read(config_path, encoding='GB18030')


# 根据section和option名字获取对应值
def get(section, option):
    return config.get(section, option)


# 根据section和option名字获取对应值
def get_int(section, option):
    return config.getint(section, option)


# 根据section和option名字获取对应值
def get_float(section, option):
    return config.getfloat(section, option)


# 根据section和option名字获取对应值
def get_boolean(section, option):
    return config.getboolean(section, option)
