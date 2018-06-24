# !/usr/bin/python3
# -*- coding:utf-8 -*-
import argparse
import server
import processors
from datacenter import datacenter
from aiohttp import web
from datautil import generalutils


async def on_startup(app: web.Application):
    app['db'] = await datacenter.init_db(app.loop)

    for m in processors.entire():
        app.loop.call_soon(generalutils.import_string(m).process, app.loop)


async def on_shutdown(app: web.Application):
    await datacenter.shutdown_db(app['db'])
    app['db'] = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='server running host, default is 127.0.0.1')
    parser.add_argument('--port', type=int, default=8080,
                        help='server running port, default is 8080')
    parser.add_argument('--debug', type=bool, default=False,
                        help='run server in debug mode')
    args = parser.parse_args()

    server.on_startup.append(on_startup)
    server.on_shutdown.append(on_shutdown)
    server.run_server(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
