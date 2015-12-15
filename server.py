# -*- coding: utf-8 -*-

import asyncio
import logging
import logging.config

from aiohttp import web
from sqlalchemy import create_engine

from utils import autoreload, autodiscover
import settings

logging.config.dictConfig(settings.LOGGING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Application(web.Application):
    def __init__(self, ds=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ds = ds

    def init_routes(self, services):
        for service in services:
            if not hasattr(service, 'get_routes'):
                continue
            for route in service.get_routes():
                self.router.add_route(*route)

    @property
    def ds(self):
        return self._ds


def init_ds():
    return create_engine(settings.DB_DSN, **settings.DB_OPTIONS)


if __name__ == '__main__':
    logger.info('STARTING')
    loop = asyncio.get_event_loop()

    autoreload.start()

    services = autodiscover.get_services()

    ds = init_ds()

    app = Application(ds=ds)
    app.init_routes(services)
    handler = app.make_handler()

    f = loop.create_server(handler, settings.HOST, settings.PORT)
    srv = loop.run_until_complete(f)
    logger.info('SERVING ON: %s:%s' % srv.sockets[0].getsockname())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('STOPPING')
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()
