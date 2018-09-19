# !/usr/bin/python3
# -*- coding:utf-8 -*-
from aiohttp import web
from . import routes, mylog
from datautil import generalutils, ormutils
from datacenter import models
from consumer import ConsumerError


@routes.get('/')
async def hello(r: web.Request):
    return web.Response(text="Hello World")


@routes.view('/cs/{path}')
async def consumer(r: web.Request):
    try:
        impl = generalutils.import_string('consumer.{}.DataConsumerImpl'.format(r.match_info['path']))
    except ImportError as e:
        raise web.HTTPBadRequest() from e
    else:
        try:
            return await impl().consume(r)
        except ConsumerError as e:
            mylog.exception(e)
            return web.Response(text=e, status=200)


@routes.get('/proxy')
async def get_proxy(r: web.Request):
    results = await ormutils.OrmUtil.query(r.app['db'], models.ProxyTbl)
    return web.Response(text='to do...')
