# !/usr/bin/python3
# -*- coding:utf-8 -*-

from .models import ProxyTbl
from datautil import ormutils
from sqlalchemy import and_
from aiomysql.cursors import SSCursor


class ProxyTblManager:
    @classmethod
    async def get_proxy(cls, db, **limit):
        async with db.acquire() as conn:
            expr = None
            area = limit.pop('area', None)
            if area is not None:
                expr = ProxyTbl.__table__.c.area.like("%{}%".format(area))

            for k, v in limit.items():
                in_expr = getattr(ProxyTbl.__table__.c, k) == v
                if expr is not None:
                    expr = and_(expr, in_expr)
                else:
                    expr = in_expr

            return await ormutils.OrmUtil.query(conn, ProxyTbl, limit=expr)

    @classmethod
    async def get_proxy_stream(cls, db, on_proxy, **limit):
        async with db.acquire() as conn:
            # async with conn.cursor(SSCursor) as cur:
            expr = None
            area = limit.pop('area', None)
            if area is not None:
                expr = ProxyTbl.__table__.c.area.like("%{}%".format(area))

            for k, v in limit.items():
                in_expr = getattr(ProxyTbl.__table__.c, k) == v
                if expr is not None:
                    expr = and_(expr, in_expr)
                else:
                    expr = in_expr

            result = await ormutils.OrmUtil.query(conn, ProxyTbl, limit=expr)
            # while True:
            #     fetched_list = await result.fetchmany(10000)
            #     if fetched_list is None:
            #         break
            await on_proxy(result)

    @classmethod
    async def set_proxy(cls, db, proxy):
        async with db.acquire() as conn:
            if not await ormutils.OrmUtil.exists(
                conn, ProxyTbl,
                limit=and_(ProxyTbl.__table__.c.host == proxy.host,
                           ProxyTbl.__table__.c.port == proxy.port)):
                return await ormutils.OrmUtil.insert(
                    conn, ProxyTbl, host=proxy.host, port=proxy.port,
                    scheme=proxy.scheme, country=proxy.country, area=proxy.area)
            else:
                return await ormutils.OrmUtil.update(
                    conn, ProxyTbl,
                    limit=and_(ProxyTbl.__table__.c.host == proxy.host,
                               ProxyTbl.__table__.c.port == proxy.port),
                    scheme=proxy.scheme, country=proxy.country, area=proxy.area)

    @classmethod
    async def delete_proxy(cls, db, **limit):
        expr = None
        for k, v in limit.items():
            in_expr = getattr(ProxyTbl.__table__.c, k) == v
            if expr is not None:
                expr = and_(expr, in_expr)
            else:
                expr = in_expr

        async with db.acquire() as conn:
            return await ormutils.OrmUtil.delete(conn, ProxyTbl, expr)
