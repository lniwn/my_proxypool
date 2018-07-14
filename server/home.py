# !/usr/bin/python3
# -*- coding:utf-8 -*-
from aiohttp import web
from . import routes
from datautil import generalutils, ormutils
from datacenter import models


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
        return await impl().consume(r)


@routes.get('/proxy')
async def get_proxy(r: web.Request):
    results = await ormutils.OrmUtil.query(r.app['db'], models.ProxyTbl)
    return web.Response(text='to do...')
