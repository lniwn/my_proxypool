# !/usr/bin/python3
# -*- coding:utf-8 -*-

from aiomysql.sa import create_engine
from datacenter.models import BaseTable
import sqlalchemy as sa

__all__ = ['init_db', 'shutdown_db']

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'


def _create_all(config):
    db_cfg = config['mysql']
    engine = sa.create_engine(SQLALCHEMY_DATABASE_URI.format(
        user=db_cfg['user'], password=db_cfg['password'],
        host=db_cfg['host'], port=db_cfg['port'],
        database=db_cfg['database']
    ), echo=True)
    # DBSession.configure(bind=engine)
    BaseTable.metadata.bind = engine
    BaseTable.metadata.create_all()


async def init_db(loop, config):
    engine_cfg = config['mysql']
    engine = await create_engine(user=engine_cfg['user'], loop=loop, echo=config['debug'],
                                 host=engine_cfg['host'], port=engine_cfg['port'],
                                 password=engine_cfg['password'], charset='utf8mb4',
                                 autocommit=True, minsize=engine_cfg['minsize'],
                                 maxsize=engine_cfg['maxsize'])
    async with engine.acquire() as conn:
        sql_stat = 'CREATE DATABASE IF NOT EXISTS {} ' \
                   'DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'.format(engine_cfg['database'])
        await conn.execute(sql_stat)
        await conn.execute('USE {};'.format(engine_cfg['database']))

        for table in BaseTable.metadata.tables.values():
            like_result = await conn.execute("SHOW TABLES LIKE '%s'" % table.name)
            if like_result.rowcount == 0:
                await conn.execute(sa.schema.CreateTable(table))
        # _create_all(config)
    return engine


async def shutdown_db(db):
    db.close()
    await db.wait_closed()
