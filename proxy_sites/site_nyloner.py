# !/usr/bin/python3
# -*- coding:utf-8 -*-
import base64
import hashlib
import datetime
import json
from . import Registerable, mylog
from datautil import webutils
from datacenter import models


class SiteNyloner(Registerable):
    async def yield_proxy(self, *args, **kwargs):
        # https://www.nyloner.cn/proxy
        ev_loop = kwargs.get('ev_loop')

        async with webutils.WebSpider(ev_loop) as spider:
            spider.header.update({'Host': 'www.nyloner.cn', 'Referer': 'https://www.nyloner.cn/proxy'})
            proxies = []
            num = 15
            status, _ = await spider.get('https://www.nyloner.cn/proxy')
            if status != 200:
                mylog.error('%s 访问出错', __name__)
                return proxies
            for page in range(1, 50):
                t = int(datetime.datetime.now().timestamp())
                status, resp_html = await spider.get('https://www.nyloner.cn/proxy', params={
                    'page': page, 'num': num, 't': t, 'token': self.gen_token(page, num, t)})
                if status != 200:
                    continue
                try:
                    js_result = json.loads(resp_html, encoding='utf-8')
                    if js_result['status'].lower() == 'true':
                        for pd in json.loads(self.decode_str(js_result['list'])):
                            proxies.append(models.ProxyTbl(host=pd['ip'], port=int(pd['port']),
                                                           scheme='http', country='未知'))
                except json.JSONDecodeError as er:
                    mylog.warning('%s 解析返回值<%s>出错: %s', __name__, resp_html, er)
                    return proxies

        return proxies

    @staticmethod
    def gen_token(page, num, t):
        hasher = hashlib.md5('{}{}{}'.format(page, num, t).encode('utf-8'))
        return hasher.hexdigest()

    @staticmethod
    def decode_str(raw_str):
        raw_str = base64.b64decode(raw_str).decode('utf-8')
        key = 'nyloner'
        length = len(key)
        code = ''
        for i in range(len(raw_str)):
            index = i % length
            code += chr(ord(raw_str[i]) ^ ord(key[index]))
        return base64.b64decode(code).decode('utf-8')
