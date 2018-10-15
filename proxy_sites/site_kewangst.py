# !/usr/bin/python3
# -*- coding:utf-8 -*-

import io
import urllib.parse
from . import Registerable, mylog
from datacenter import models
from datautil import webutils


class SiteKewangst(Registerable):
    async def yield_proxy(self, *args, **kwargs):
        ev_loop = kwargs.get('ev_loop')

        async with webutils.WebSpider(ev_loop) as spider:
            spider.header.update({'Host': 'www.kewangst.com', 'Referer': 'https://www.kewangst.com/ProxyList'})
            proxies = []
            status, resp_text = await spider.get('https://www.kewangst.com/ProxyList')
            if status != 200:
                mylog.error('%s 访问出错', __name__)
                return proxies
            with io.StringIO(resp_text) as fp:
                while True:
                    line = fp.readline()
                    if line:
                        line = line.strip()
                    else:
                        break
                    if line.startswith('http'):
                        try:
                            parse_result = urllib.parse.urlparse(line)
                            proxies.append(models.ProxyTbl(
                                host=parse_result.hostname, port=parse_result.port, scheme=parse_result.scheme,
                                country='未知'))
                        except ValueError as e:
                            mylog.warning(e)

        return proxies
