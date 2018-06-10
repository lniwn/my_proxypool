# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import proxy_sites
from datautil import webutils


async def run(ev_loop):
    proxy_sites.register_all()

    proxy_list = list()
    print('开始获取代理...')
    tasks = [asyncio.ensure_future(s.yield_proxy(ev_loop=ev_loop)) for s in proxy_sites.sites.values()]
    for p in await asyncio.gather(*tasks, loop=ev_loop):
        proxy_list.extend(p)
    print('获得原始代理个数：', len(proxy_list))
    print('开始筛选代理...')
    async with webutils.ProxyValidator(ev_loop) as validator:
        # aiohttp only support http proxy
        tasks = [asyncio.ensure_future(validator.is_useable(pp)) for pp in proxy_list if pp.scheme.lower() == 'http']
        for able, pp in await asyncio.gather(*tasks, loop=ev_loop):
            if able:
                print(pp)


def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(loop))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == '__main__':
    main()
