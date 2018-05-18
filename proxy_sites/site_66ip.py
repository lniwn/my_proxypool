# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
from lxml import etree
from . import Registerable
from datacenter import ProxyPair
from datautil import webutils


class Site66IP(Registerable):
    async def yield_proxy(self, *args, **kwargs):
        ev_loop = kwargs.get('ev_loop')
        async with webutils.WebSpider(ev_loop) as spider:
            spider.header.update({'Host': 'www.66ip.cn'})

            area = 33
            page = 1
            proxies = []
            for area_index in range(1, area + 1):
                asyncio.sleep(1, loop=ev_loop)
                for i in range(1, page + 1):
                    url = "http://www.66ip.cn/areaindex_{}/{}.html".format(area_index, i)
                    status, resp_html = await spider.get(url)
                    if status != 200:
                        continue
                    html_tree = etree.HTML(resp_html)
                    tr_list = html_tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                    if len(tr_list) == 0:
                        continue
                    for tr in tr_list:
                        proxies.append(ProxyPair(ip=tr.xpath("./td[1]/text()")[0],
                                                 port=tr.xpath("./td[2]/text()")[0],
                                                 location=tr.xpath("./td[3]/text()")[0],
                                                 scheme='http'))
            return proxies
