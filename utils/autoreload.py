# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import sys
import subprocess
import types

try:
    import signal
except ImportError:
    signal = None

from functools import partial

logger = logging.getLogger(__name__)

_has_execv = sys.platform != 'win32'


def start(check_time=0.5, modify_times=None):
    loop = asyncio.get_event_loop()

    if modify_times is None:
        modify_times = {}
    callback = partial(_reload_on_update, modify_times)
    loop.call_later(check_time, callback)


def _reload_on_update(modify_times):
    for module in list(sys.modules.values()):
        if not isinstance(module, types.ModuleType):
            continue

        path = getattr(module, '__file__', None)
        if path is None:
            continue

        if path.endswith('.pyc') or path.endswith('.pyo'):
            path = path[:-1]
        _check_file(modify_times, path)

    start(modify_times=modify_times)


def _check_file(modify_times, path):
    try:
        modified = os.stat(path).st_mtime
    except Exception:
        return
    if path not in modify_times:
        modify_times[path] = modified
        return
    if modify_times[path] != modified:
        logger.info('%s modified: restarting server' % path)
        _reload()


def _reload():
    global _reload_attempted
    _reload_attempted = True

    loop = asyncio.get_event_loop()
    loop.stop()

    if hasattr(signal, "setitimer"):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)

    path_prefix = '.' + os.pathsep
    if (sys.path[0] == '' and
            not os.environ.get("PYTHONPATH", "").startswith(path_prefix)):
        os.environ["PYTHONPATH"] = (path_prefix + os.environ.get("PYTHONPATH", ""))
    if not _has_execv:
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(0)
    else:
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except OSError:
            os.spawnv(os.P_NOWAIT, sys.executable, [sys.executable] + sys.argv)
            os._exit(0)
