# !/usr/bin/python3
# -*- coding:utf-8 -*-


class OrmUtil:
    @classmethod
    async def insert(cls, conn, orm_cls, **kwargs):
        return await conn.execute(orm_cls.__table__.insert().values(**kwargs))

    @classmethod
    async def query(cls, conn, orm_cls, limit=None):
        sql_stat = orm_cls.__table__.select()
        if limit is not None:
            sql_stat = sql_stat.where(limit)
        q_set = await conn.execute(sql_stat)
        return await q_set.fetchall()

    @classmethod
    async def delete(cls, conn, orm_cls, limit=None):
        sql_stat = orm_cls.__table__.delete()
        if limit is not None:
            sql_stat = sql_stat.where(limit)
        return await conn.execute(sql_stat)

    @classmethod
    async def update(cls, conn, orm_cls, limit=None, **kwargs):
        assert limit is not None
        return await conn.execute(
            orm_cls.__table__.update().where(limit).values(**kwargs))

    @classmethod
    async def exists(cls, conn, orm_cls, limit=None):
        assert limit is not None
        return await (await conn.execute(orm_cls.__table__.select().where(limit))).scalar()
