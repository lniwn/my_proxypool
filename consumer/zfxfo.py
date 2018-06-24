# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
code url: http://zr.zfxfo.com/lib/code.js
"""
from aiohttp import web, ClientError
from multidict import CIMultiDictProxy
from . import DataConsumer, ConsumerError
from datautil import webutils
from datacenter import datacenter
import uuid
import time
import re
import json
import urllib.parse
import random
import asyncio
import queue


class DataConsumerImpl(DataConsumer):
    def __init__(self):
        super().__init__()
        self._user_arg = None
        self._main_url = 'http://zr.zfxfo.com/mobile/url545/index.html?k=051612'
        self._k = '051612'
        self._cb = 'jQuery{0}_{1}'.format(uuid.uuid4().int, int(time.time() * 1000))

    @staticmethod
    def resp_2_json(text):
        js = re.search('(\{.*\})', text).group(1)
        return json.loads(js)

    async def consume(self, user_arg: CIMultiDictProxy, **kwargs) -> web.Response:
        self._user_arg = user_arg
        while True:
            try:
                proxy = datacenter.get_proxy(lambda p: p.location != '香港')
            except queue.Empty:
                return web.Response(text='目前没有可用代理，请稍候再试', charset='utf-8')
            async with webutils.WebSpider(ev_loop=None, proxy=proxy) as client:
                try:
                    stock = random.choice(await self.get_stock(client))
                    stock = re.search('c:"(\d+)"', stock).group(1)
                    spldid = await self.open_page(client)
                    await self.page_loading(client, spldid)
                    msg = await self.set_pageoperinfo(client, spldid, stock)
                    await self.page_close(client, spldid)
                except ConsumerError as err:
                    return web.Response(text=err.expression)
                except AttributeError as err:
                    raise web.HTTPInternalServerError() from err
                except (ClientError, asyncio.TimeoutError) as err:
                    pass  # timeout error, continue
                else:
                    return web.Response(text=msg, charset='utf-8')

    async def get_stock(self, client) -> list:
        url = "http://zr.zfxfo.com/lib/code.js"
        client.header.update(
            {
                'Referer': self._main_url,
                'Host': 'zr.zfxfo.com'
            }
        )
        status, text = await client.get(url, params={
            '_': int(time.time() * 1000)
        })
        if status != 200:
            raise ConsumerError(str(status), '<http://zr.zfxfo.com/lib/code.js> failed')
        return re.findall('(\{[^\}]+\})', text)

    async def open_page(self, client: webutils.WebSpider):
        url = 'http://119.23.58.158:8081/control/addData/openPage'
        client.header.update(
            {
                'Referer': self._main_url,
                'Host': '119.23.58.158:8081'
            }
        )
        _, text = await client.get(url, params={
            'callback': self._cb,
            'kname': 'undefined',
            'k': self._k,
            '_': int(time.time() * 1000)
        })

        try:
            js = self.resp_2_json(text)
            if js['status'].lower() != 'success':
                raise ConsumerError(text, 'openpage failed') from None
            return js['data']
        except AttributeError as err:
            raise ConsumerError(text, 'openpage failed') from err

    async def page_loading(self, client, id):
        url = 'http://119.23.58.158:8081/control/addData/pageLoding'
        client.header.update(
            {
                'Referer': self._main_url,
                'Host': '119.23.58.158:8081'
            }
        )
        _, text = await client.get(url, params={
            'callback': self._cb,
            'id': id,
            '_': int(time.time() * 1000)
        })
        try:
            js = self.resp_2_json(text)
            if js['status'].lower() != 'success':
                raise ConsumerError(text, 'pageloading failed') from None
        except AttributeError as err:
            raise ConsumerError(text, 'pageloading failed') from err

    async def set_pageoperinfo(self, client, spldid, stock):
        url = 'http://119.23.58.158:8081/control/addData/setpageoperinfo'
        client.header.update(
            {
                'Referer': self._main_url,
                'Host': '119.23.58.158:8081'
            }
        )
        _, text = await client.get(url, params={
            'callback': self._cb,
            'SPLDID': spldid,
            'OperID': '1',
            'StockCode': stock,
            'WXNumber': 'undefined',
            'URLParams': urllib.parse.quote('kname=undefined&k={0}'.format(self._k)),
            'PhoneNumber': self._user_arg['phone'],
            '_': int(time.time() * 1000)
        })
        try:
            js = self.resp_2_json(text)
            if js['status'].lower() != 'success':
                raise ConsumerError(text, 'setpageoperinfo failed') from None
            return js['msg']
        except AttributeError as err:
            raise ConsumerError(text, 'setpageoperinfo failed') from err

    async def page_close(self, client, id):
        url = 'http://119.23.58.158:8081/control/addData/pageclose'
        client.header.update(
            {
                'Referer': self._main_url,
                'Host': '119.23.58.158:8081'
            }
        )
        _, text = await client.get(url, params={
            'callback': self._cb,
            'id': id,
            '_': int(time.time() * 1000)
        })
        try:
            js = self.resp_2_json(text)
            if js['status'].lower() != 'success':
                raise ConsumerError(text, 'pageclose failed') from None
        except AttributeError as err:
            raise ConsumerError(text, 'pageclose failed') from err
