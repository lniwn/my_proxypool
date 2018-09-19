# !/usr/bin/python3
# -*- coding:utf-8 -*-
import aiohttp_jinja2
import jinja2
import logging
from aiohttp import web
from datautil import generalutils
from server.middlewares import init_middlewares


routes = web.RouteTableDef()
on_startup = []
on_shutdown = []
mylog = logging.getLogger(__name__)


def _init_server(app: web.Application):
    modules = ('server.home',)
    for n in modules:
        generalutils.import_string(n)

    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('server', 'templates'))
    routes.static('/static/', 'server/static/', name='static', show_index=True, append_version=True)

    init_middlewares(app)

    app.on_startup.extend(on_startup)
    app.on_shutdown.extend(on_shutdown)

    app.add_routes(routes)


def run_server(config):
    app = web.Application(debug=config['debug'])
    app['config'] = config
    _init_server(app)
    web.run_app(app, host=config['host'], port=config['port'])
