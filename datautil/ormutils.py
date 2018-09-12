# !/usr/bin/python3
# -*- coding:utf-8 -*-


class OrmUtil:
    @classmethod
    async def insert(cls, conn, orm_cls, *args, **kwargs):
        return await conn.execute(orm_cls.__table__.insert().values(*args, **kwargs))

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
    async def update(cls, conn, orm_cls, *args, limit=None, **kwargs):
        assert limit is not None
        return await conn.execute(
            orm_cls.__table__.update().where(limit).values(*args, **kwargs))

    @classmethod
    async def exists(cls, conn, orm_cls, limit=None):
        assert limit is not None
        return (await (await conn.execute(orm_cls.__table__.select().where(limit))).scalar()) is not None

    @classmethod
    async def execute(cls, conn, sql):
        return await conn.execute(sql)

    @classmethod
    def model2dict(cls, m):
        # from sqlalchemy.orm import class_mapper
        # columns = [c.key for c in class_mapper(model.__class__).columns]
        columns = [c.key for c in m.__table__.c]
        return dict((c, getattr(m, c, None)) for c in columns)
