# !/usr/bin/python3
# -*- coding:utf-8 -*-

from aiomysql.sa import create_engine
from datacenter.models import BaseTable
import sqlalchemy as sa

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lniwn:xxxx@172.27.21.17:3307/proxy_pool?charset=utf8mb4'


def _create_all():
    engine = sa.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    # DBSession.configure(bind=engine)
    BaseTable.metadata.bind = engine
    BaseTable.metadata.create_all()


async def init_db(loop):
    engine = await create_engine(user='lniwn', loop=loop,
                                 host='172.27.21.17', port=3307,
                                 password='xxxx', charset='utf8mb4',
                                 autocommit=True)
    async with engine.acquire() as conn:
        await conn.execute('CREATE DATABASE IF NOT EXISTS proxy_pool;')
        await conn.execute('USE proxy_pool;')

        for table in BaseTable.metadata.tables.values():
            like_result = await conn.execute("SHOW TABLES LIKE '%s'" % table.name)
            if like_result.rowcount == 0:
                await conn.execute(sa.schema.CreateTable(table))
        # _create_all()
    return engine


async def shutdown_db(db):
    db.close()
    await db.wait_closed()
