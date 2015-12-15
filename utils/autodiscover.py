# -*- coding: utf-8 -*-

import importlib
import logging
import os
import os.path


logger = logging.getLogger(__name__)


def get_services():
    return _services


def get_services_names():
    if not os.path.exists(_services_dir):
        return []
    return filter(
        lambda d: (d != '__pycache__' and os.path.isdir(os.path.join(_services_dir, d))),
        os.listdir(_services_dir)
    )

_cur_dir = os.path.dirname(os.path.dirname(__file__))
_services_dir = os.path.join(_cur_dir, 'services')
_services = []
for service_name in get_services_names():
    try:
        service = importlib.import_module('services.%s' % service_name)
    except ImportError as e:
        logger.debug(e)
        continue
    _services.append(service)
