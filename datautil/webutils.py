# !/usr/bin/python3
# -*- coding:utf-8 -*-

import aiohttp
import asyncio
import random
from datacenter import ProxyPair
from . import UA_LIST


def user_agent():
    return random.choice(UA_LIST)


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
        self._sess = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=30),
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
            if pp.scheme.lower() == 'https':
                url = 'https://httpbin.org/ip'
            else:
                url = 'http://httpbin.org/ip'
            async with self._sess.get(url, proxy='{0}://{1}:{2}'.format(
                                         pp.scheme if pp.scheme is not None else 'http',
                                         pp.host,
                                         pp.port)) as resp:
                return resp.status == 200, pp
        except (asyncio.TimeoutError, aiohttp.ClientError):
            return False, pp


class WebSpider:
    def __init__(self, ev_loop, **kwargs):
        self._headers = {
            'User-Agent': user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache'
        }
        proxy = kwargs.pop('proxy', None)
        self._sess = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=5),
                                           loop=ev_loop, headers=self._headers, read_timeout=60*2,
                                           conn_timeout=60, **kwargs)
        if proxy is not None:
            self._proxy = '{0}://{1}:{2}'.format(
                proxy.scheme if proxy.scheme is not None else 'http',
                proxy.host,
                proxy.port)
        else:
            self._proxy = None

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
        proxy = kwargs.pop('proxy', None)
        if proxy is None:
            proxy = self._proxy
        async with self._sess.get(url, proxy=proxy, **kwargs) as resp:
            return resp.status, await resp.text()

    async def post(self, url, **kwargs):
        proxy = kwargs.pop('proxy', None)
        if proxy is None:
            proxy = self._proxy
        async with self._sess.post(url, proxy=proxy, **kwargs) as resp:
            return resp.status, await resp.text()
