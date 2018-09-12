# !/usr/bin/python3
# -*- coding:utf-8 -*-

from .models import ProxyTbl
from datautil import ormutils
from sqlalchemy import and_, or_


class ProxyTblManager:
    @classmethod
    async def get_proxy(cls, db, **limits):
        async with db.acquire() as conn:
            conds = []
            used_time = limits.pop('used_time', None)
            if used_time is not None:
                conds.append(or_(ProxyTbl.used_time == None, ProxyTbl.used_time < used_time))
            area = limits.pop('area', None)
            if area is not None:
                conds.append(ProxyTbl.__table__.c.area.like("%{}%".format(area)))
            limit = limits.pop('limit', None)

            for k, v in limits.items():
                in_expr = getattr(ProxyTbl.__table__.c, k) == v
                conds.append(in_expr)

            expr = None
            if conds:
                expr = and_(*conds)

            if limit is None:
                return await ormutils.OrmUtil.query(conn, ProxyTbl, limit=expr)
            else:
                return await (await ormutils.OrmUtil.execute(
                    conn, ProxyTbl.__table__.select().where(expr).limit(limit))).fetchall()

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
                    conn, ProxyTbl, ormutils.OrmUtil.model2dict(proxy))
            else:
                return await ormutils.OrmUtil.update(
                    conn, ProxyTbl, ormutils.OrmUtil.model2dict(proxy),
                    limit=and_(ProxyTbl.__table__.c.host == proxy.host,
                               ProxyTbl.__table__.c.port == proxy.port))

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
