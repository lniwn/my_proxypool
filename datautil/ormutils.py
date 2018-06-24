# !/usr/bin/python3
# -*- coding:utf-8 -*-


class OrmUtil:
    @classmethod
    async def insert(cls, db, orm_cls, **kwargs):
        async with db.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(orm_cls.insert().values(**kwargs))
            except Exception:
                await trans.rollback()
                raise
            else:
                await trans.commit()

    @classmethod
    async def query(cls, db, orm_cls):
        async with db.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(orm_cls.select())
            except Exception:
                await trans.rollback()
                raise
            else:
                return await trans.commit()

    @classmethod
    async def delete(cls, db, orm_cls, **kwargs):
        async with db.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(orm_cls.delete(**kwargs))
            except Exception:
                await trans.rollback()
                raise
            else:
                return await trans.commit()

    @classmethod
    async def update(cls, db, orm_cls, **kwargs):
        async with db.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(orm_cls.update(**kwargs))
            except Exception:
                await trans.rollback()
                raise
            else:
                return await trans.commit()
