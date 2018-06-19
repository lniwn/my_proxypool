# !/usr/bin/python3
# -*- coding:utf-8 -*-
from aiohttp import web
from datautil import generalutils


routes = web.RouteTableDef()
on_startup = []
on_shutdown = []


def _init_server(app: web.Application):
    modules = ('server.home',)
    for n in modules:
        generalutils.import_string(n)
    app.add_routes(routes)
    app.on_startup.extend(on_startup)
    app.on_shutdown.extend(on_shutdown)


def run_server(host=None, port=None, debug=False):
    app = web.Application(debug=debug)
    _init_server(app)
    web.run_app(app, host=host, port=port)
