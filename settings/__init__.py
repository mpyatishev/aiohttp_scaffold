# -*- coding: utf-8 -*-


try:
    from settings.local import *
except ImportError:
    from settings.defaults import *
