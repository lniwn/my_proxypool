# !/usr/bin/python3
# -*- coding:utf-8 -*-
import argparse
import proxy_sites
import server
from datacenter import datacenter
from aiohttp import web


async def on_startup(app: web.Application):
    await datacenter.init_center(app.loop)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='server running host, default is 127.0.0.1')
    parser.add_argument('--port', type=int, default=8080,
                        help='server running port, default is 8080')
    parser.add_argument('--debug', type=bool, default=False,
                        help='run server in debug mode')
    args = parser.parse_args()

    proxy_sites.register_all()

    server.on_startup.append(on_startup)
    server.run_server(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
