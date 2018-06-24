# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import proxy_sites
from datautil import webutils


async def do_work(loop):
    raw_proxy_list = []
    q = list()
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
                q.append(pp)
    return q


def process(loop):
    proxy_sites.register_all()

    asyncio.ensure_future(do_work(loop), loop=loop)
