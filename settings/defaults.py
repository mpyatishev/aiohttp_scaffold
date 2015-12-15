# -*- coding: utf-8 -*-

HOST = '0.0.0.0'
PORT = '8080'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s.' +
                      '%(funcName)s at %(lineno)d: %(message)s',
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    }
}

DSN = '%(driver)s://%(user)s:%(passwd)s@%(host)s/%(name)s'
