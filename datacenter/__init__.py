# !/usr/bin/python3
# -*- coding:utf-8 -*-
import trafaret
# from collections import namedtuple
from datacenter import models
# from sqlalchemy.orm import sessionmaker

# DBSession = sessionmaker()


# class ProxyPair(namedtuple('ProxyPair', models.ProxyTbl.__table__.columns.keys())):
#     __slots__ = ()
#
#     def __str__(self):
#         return str(self._asdict())


TRAFARET = trafaret.Dict({
    trafaret.Key('mysql'): trafaret.Dict({
        'database': trafaret.String(),
        'user': trafaret.String(),
        'password': trafaret.String(),
        'host': trafaret.String(),
        'port': trafaret.Int(),
        'minsize': trafaret.Int(),
        'maxsize': trafaret.Int(),
    }),
    trafaret.Key('host'): trafaret.IP,
    trafaret.Key('port'): trafaret.Int(),
    trafaret.Key('debug'): trafaret.Bool(),
    trafaret.Key('period'): trafaret.Int()
})
