# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import proxy_sites
from datautil import webutils
from datacenter.proxy_tbl_manager import ProxyTblManager


async def do_work(app):
    raw_proxy_list = []
    loop = app.loop
    tasks = [asyncio.ensure_future(s.yield_proxy(ev_loop=loop), loop=loop)
             for s in proxy_sites.entire()]
    for p in await asyncio.gather(*tasks, loop=loop):
        raw_proxy_list.extend(p)

    async with webutils.ProxyValidator(loop) as validator:
        # aiohttp only support http proxy
        tasks = [asyncio.ensure_future(validator.is_useable(pp))
                 for pp in raw_proxy_list if pp.scheme == 'http']
        for able, pp in await asyncio.gather(*tasks, loop=loop):
            if able:
                await ProxyTblManager.set_proxy(app['db'], pp)

    # fetch proxy in period
    loop.call_later(app['config']['period'],
                    lambda param: asyncio.ensure_future(do_work(param), loop=param.loop),
                    app)


def process(app):
    proxy_sites.register_all()

    asyncio.ensure_future(do_work(app), loop=app.loop)
