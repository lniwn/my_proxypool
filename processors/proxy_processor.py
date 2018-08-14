# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import proxy_sites
from datautil import webutils
from datacenter.proxy_tbl_manager import ProxyTblManager
from sqlalchemy.exc import SQLAlchemyError
from . import mylog


async def do_work(app):
    mylog.info('%s开始执行', __name__)
    raw_proxy_list = []
    loop = app.loop
    tasks = [asyncio.ensure_future(s.yield_proxy(ev_loop=loop), loop=loop)
             for s in proxy_sites.entire()]
    for p in await asyncio.gather(*tasks, loop=loop):
        raw_proxy_list.extend(p)

    mylog.info('原始代理IP获取成功，总数为: %d', len(raw_proxy_list))
    async with webutils.ProxyValidator(loop) as validator:
        # aiohttp only support http proxy
        tasks = [asyncio.ensure_future(validator.is_useable(pp))
                 for pp in raw_proxy_list if pp.scheme == 'http']
        for able, pp in await asyncio.gather(*tasks, loop=loop):
            if able:
                try:
                    await ProxyTblManager.set_proxy(app['db'], pp)
                except SQLAlchemyError as er:
                    mylog.exception(er)

    # check ip location
    # http://ip.chinaz.com/getip.aspx

    mylog.info('原始代理IP筛选完成，创建下一次定时任务')
    # fetch proxy in period
    loop.call_later(app['config']['period'],
                    lambda param: asyncio.ensure_future(do_work(param), loop=param.loop),
                    app)


def process(app):
    proxy_sites.register_all()

    asyncio.ensure_future(do_work(app), loop=app.loop)
