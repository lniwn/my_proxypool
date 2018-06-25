# !/usr/bin/python3
# -*- coding:utf-8 -*-
import aiohttp_jinja2
from aiohttp import web

__all__ = ['init_middlewares']


async def handle_404(request):
    return aiohttp_jinja2.render_template('404.html', request, {})


async def handle_500(request):
    return aiohttp_jinja2.render_template('500.html', request, {})


def create_error_middleware(overrides):
    @web.middleware
    async def error_middleware(request, handler):
        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override:
                return await override(request)
            return response
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)
            raise

    return error_middleware


def init_middlewares(app: web.Application):
    e_m = create_error_middleware(
        {404: handle_404,
         500: handle_500}
    )
    app.middlewares.append(e_m)