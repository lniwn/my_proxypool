# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
from lxml import etree
from . import Registerable
from datacenter import ProxyPair
from datautil import webutils


class SiteXici(Registerable):
    async def yield_proxy(self, *args, **kwargs):
        ev_loop = kwargs.get('ev_loop')
        async with webutils.WebSpider(ev_loop) as spider:
            spider.header.update({'Host': 'www.xicidaili.com'})

            proxies = []

            url_list = [
                'http://www.xicidaili.com/nn/',  # 高匿
                'http://www.xicidaili.com/nt/',  # 透明
                'http://www.xicidaili.com/wn/',  # 国内https
                'http://www.xicidaili.com/wt/',  # 国内普通
            ]
            page = 2
            for url in url_list:
                for i in range(1, page + 1):
                    asyncio.sleep(1, loop=ev_loop)
                    url = url + str(i)
                    status, resp_html = await spider.get(url)
                    if status != 200:
                        continue
                    html_tree = etree.HTML(resp_html)
                    ip_list = html_tree.xpath('//table[@id="ip_list"]//tr[position()>1]')
                    for tr in ip_list:
                        tds = tr.xpath("td")
                        if len(tds) < 5:
                            continue

                        location = tds[3].xpath('a')
                        if len(location) >= 1:
                            location = location[0].text
                        else:
                            location = tds[3].text
                        proxies.append(ProxyPair(ip=str(tds[1].text),
                                                 port=str(tds[2].text),
                                                 location=str(location),
                                                 scheme=str(tds[5].text).lower()))

            return proxies
