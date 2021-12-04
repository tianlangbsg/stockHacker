import logging.config
import os
from datetime import datetime

from util.commonUtil import get_root_path

DEBUG = True
log_level = logging.DEBUG if DEBUG else logging.INFO

# log config here
root_path = get_root_path()
log_path = os.path.join(root_path, 'logs')
if not os.path.exists(log_path):
    os.makedirs(log_path)

curdate = datetime.now().strftime('%Y%m%d')

InfoLogPath = log_path + '\\log_' + curdate + '.log'
# WarnLogPath = log_path + '\\warn' + curdate + '.log'
# ErrorLogPath = log_path + '\\error' + curdate + '.log'
# AccessLogPath = log_path + '\\access' + curdate + '.log'
# RootLogPath = log_path + '\\root' + curdate + '.log'

log_config_dict = {
    "version": 1,
    'disable_existing_loggers': False,

    'loggers': {
        'log.info': {
            'handlers': ['info', 'console'],  # 列表类型，可以控制打印到文件和控制台
            'level': log_level,
            'propagate': False,  # 是否传递给父记录器
        },
        # 'log.warn': {
        #     'handlers': ['warn', 'console'],
        #     'level': logging.WARN,
        #     'propagate': False,  # 是否传递给父记录器
        # },
        # 'log.error': {
        #     'handlers': ['error', 'console'],
        #     'level': logging.ERROR,
        #     'propagate': False,  # 是否传递给父记录器
        # },
        # 'log.access': {
        #     'handlers': ['access', 'console'],
        #     'level': logging.INFO,
        #     'propagate': False,  # 是否传递给父记录器
        # },
    },

    'handlers': {
        # 输出到控制台
        'console': {
            'level': log_level,
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出到文件
        'info': {
            'level': log_level,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': InfoLogPath,
            'when': "midnight",  # 切割日志的时间
            'backupCount': 7,  # 备份份数
            'encoding': 'utf-8'
        },
        # 'warn': {
        #     'level': logging.WARN,
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     'formatter': 'standard',
        #     'filename': WarnLogPath,
        #     'when': "midnight",  # 切割日志的时间
        #     'backupCount': 7,  # 备份份数
        #     'encoding': 'utf-8'
        # },
        # 'error': {
        #     'level': logging.ERROR,
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     'formatter': 'standard',
        #     'filename': ErrorLogPath,
        #     'when': "midnight",  # 切割日志的时间
        #     'backupCount': 7,  # 备份份数
        #     'encoding': 'utf-8',
        # },
        # 'access': {
        #     'level': logging.INFO,
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     'formatter': 'standard',
        #     'filename': AccessLogPath,
        #     'when': "midnight",  # 切割日志的时间
        #     'backupCount': 7,  # 备份份数
        #     'encoding': 'utf-8'
        # }
    },

    'filters': {},

    'formatters': {
        # 标准输出格式
        'standard': {
            # 'format': '[%(asctime)s] - %(levelname)s %(module)s:%(funcName)s(%(lineno)d) - %(message)s'
            # 'format': '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
            'format': '%(asctime)s - %(levelname)s: %(message)s',
        }
    }
}

logging.config.dictConfig(log_config_dict)

log_info = logging.getLogger("log.info")


# log_warn = logging.getLogger("log.warn")
# log_error = logging.getLogger("log.error")
# log_access = logging.getLogger("log.access")

def info(message):
    log_info.info(message)


def warning(message):
    log_info.warning(message)


def error(message):
    log_info.error(message)
