# !/usr/bin/python3
# -*- coding:utf-8 -*-

from .models import ProxyTbl
from datautil import ormutils
from sqlalchemy import and_


class ProxyTblManager:
    @classmethod
    async def get_proxy(cls, db, scheme=None, location=None):
        async with db.acquire() as conn:
            limit = None
            if isinstance(scheme, str):
                limit = (ProxyTbl.__table__.c.scheme == scheme)
            if isinstance(location, str):
                limit2 = ProxyTbl.__table__.like("%{}%".format(location))
                if limit is None:
                    limit = limit2
                else:
                    limit = and_(limit, limit2)

            return await ormutils.OrmUtil.query(conn, ProxyTbl, limit=limit)

    @classmethod
    async def set_proxy(cls, db, proxy):
        async with db.acquire() as conn:
            q_results = await ormutils.OrmUtil.query(
                conn, ProxyTbl,
                and_(ProxyTbl.__table__.c.ip == proxy.ip,
                     ProxyTbl.__table__.c.port == proxy.port))
            if len(q_results) == 0:
                return await ormutils.OrmUtil.insert(
                    conn,ProxyTbl, ip=proxy.ip, port=proxy.port,
                    scheme=proxy.scheme, location=proxy.location)
            else:
                assert len(q_results) == 1
                return await ormutils.OrmUtil.update(
                    conn, ProxyTbl,
                    limit=and_(ProxyTbl.__table__.c.ip == proxy.ip,
                               ProxyTbl.__table__.c.port == proxy.port),
                    scheme=proxy.scheme, location=proxy.location)

    @classmethod
    async def delete_proxy(cls, db, ip=None, port=None):
        async with db.acquire() as conn:
            limit = None
            if isinstance(ip, str):
                limit = (ProxyTbl.__table__.c.ip == ip)
            if isinstance(port, int):
                limit2 = (ProxyTbl.__table__.c.port == port)
                if limit is None:
                    limit = limit2
                else:
                    limit = and_(limit, limit2)
            return await ormutils.OrmUtil.delete(conn, ProxyTbl, limit)
