import asyncio
import logging


import jinja2

import aiohttp_jinja2
from aiohttp import web

from .middlewares import setup_middlewares
from .routes import setup_routes


def init(loop):

    app = web.Application(loop=loop)

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('src', 'templates'))

    # setup views and routes
    setup_routes(app)
    setup_middlewares(app)

    return app


def main():
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()

    app = init(loop)
    web.run_app(app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()