# !/usr/bin/python3
# -*- coding:utf-8 -*-

import aiohttp
import random
from datacenter import ProxyPair


def user_agent():
    ua_list = (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    )
    return random.choice(ua_list)


class ProxyValidator:
    def __init__(self, ev_loop):
        self._loop = ev_loop
        self._headers = {
            'User-Agent': user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'httpbin.org',
            'Pragma': 'no-cache'
        }
        self._sess = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=10),
                                           loop=ev_loop, headers=self._headers, read_timeout=60, conn_timeout=30)

    def __enter__(self):
        raise TypeError("Use async with instead")

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._sess.close()

    async def is_useable(self, pp: ProxyPair):
        try:
            async with self._sess.get('https://httpbin.org/ip',
                                      proxy='{0}://{1}:{2}'.format(
                                         pp.scheme if pp.scheme is not None else 'http',
                                         pp.ip,
                                         pp.port)) as resp:
                return resp.status == 200, pp
        except (aiohttp.ServerTimeoutError, aiohttp.ClientError):
            return False, pp


class WebSpider:
    def __init__(self, ev_loop):
        self._headers = {
            'User-Agent': user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache'
        }
        self._sess = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=5),
                                           loop=ev_loop, headers=self._headers, read_timeout=60*2, conn_timeout=60)

    def __enter__(self):
        raise TypeError("Use async with instead")

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._sess.close()

    @property
    def header(self):
        return self._headers

    @header.setter
    def header(self, value):
        self._headers.update(value)

    async def get(self, url, **kwargs):
        async with self._sess.get(url, **kwargs) as resp:
            return resp.status, await resp.text()

    async def post(self, url, **kwargs):
        async with self._sess.post(url, **kwargs) as resp:
            return resp.status, await resp.text()
