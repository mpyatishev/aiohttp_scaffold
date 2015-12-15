# -*- coding: utf-8 -*-

from settings.defaults import *

DB_SETTINGS = {
    'driver': 'mysql+pymysql',
    'name': 'auto',
    'host': 'localhost',
    'user': 'auto',
    'passwd': 'secret',
}

DB_DSN = DSN % DB_SETTINGS

DB_OPTIONS = {
    'pool_size': 20
}
