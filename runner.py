# !/usr/bin/python3
# -*- coding:utf-8 -*-
import argparse
import logging
import server
import processors
from trafaret_config import commandline
from datacenter import datacenter, TRAFARET
from aiohttp import web
from datautil import generalutils


async def on_startup(app: web.Application):
    app['db'] = await datacenter.init_db(app.loop, app['config'])

    for m in processors.entire():
        app.loop.call_soon(generalutils.import_string(m).process, app)


async def on_shutdown(app: web.Application):
    await datacenter.shutdown_db(app['db'])
    app['db'] = None


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)-12s - %(levelname)-5s - %(message)s',
        datefmt='%y-%m-%d %H:%M:%S'
    )

    parser = argparse.ArgumentParser()
    commandline.standard_argparse_options(parser, default_config='config/config.yaml')

    options, unknown = parser.parse_known_args()
    config = commandline.config_from_options(options, TRAFARET)

    server.on_startup.append(on_startup)
    server.on_shutdown.append(on_shutdown)
    server.run_server(config)


if __name__ == '__main__':
    main()
