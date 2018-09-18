#!/usr/bin/python3
# -*- encoding:utf-8 -*-
"""
Name: schedule_processor
Date: 2018/7/15 12:49
Author: lniwn
E-mail: lniwn@live.com

"""
import asyncio
from . import mylog
from datacenter.proxy_tbl_manager import ProxyTblManager
from datautil import webutils
from sqlalchemy.exc import SQLAlchemyError


def process(app):
    asyncio.ensure_future(scan_database(app), loop=app.loop)


async def scan_database(app):
    mylog.info('%s开始执行', __name__)

    try:
        await on_get_proxy(await ProxyTblManager.get_proxy(app['db']), app)
    finally:
        mylog.info('服务器数据清洗完成，创建下一次定时任务')
        app.loop.call_later(app['config']['period'] * 5.5,
                            lambda param: asyncio.ensure_future(scan_database(param), loop=param.loop),
                            app)


async def on_get_proxy(proxy_list, app):
    loop = app.loop
    async with webutils.ProxyValidator(loop) as validator:
        tasks = []
        for p in proxy_list:
            fu = asyncio.ensure_future(scan_one_proxy(app, validator, p), loop=loop)
            tasks.append(fu)
        await asyncio.gather(*tasks, loop=loop)


async def scan_one_proxy(app, validator, p):
    useable, p = await validator.is_useable(p)
    try:
        if not useable:
            await ProxyTblManager.delete_proxy(app['db'], host=p.host, port=p.port)
        else:
            await ProxyTblManager.set_proxy(app['db'], p)
    except SQLAlchemyError as er:
        mylog.exception(er)