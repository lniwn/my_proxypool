# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import proxy_sites
import random
from datautil import webutils

_useable_proxies = []


async def init_center(loop):
    raw_proxy_list = []
    tasks = [asyncio.ensure_future(s.yield_proxy(ev_loop=loop), loop=loop)
             for s in proxy_sites.sites.values()]
    for p in await asyncio.gather(*tasks, loop=loop):
        raw_proxy_list.extend(p)

    async with webutils.ProxyValidator(loop) as validator:
        # aiohttp only support http proxy
        tasks = [asyncio.ensure_future(validator.is_useable(pp))
                 for pp in raw_proxy_list if pp.scheme == 'http']
        for able, pp in await asyncio.gather(*tasks, loop=loop):
            if able:
                _useable_proxies.append(pp)


def get_proxy():
    return random.choice(_useable_proxies)
