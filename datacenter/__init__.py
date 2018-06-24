# !/usr/bin/python3
# -*- coding:utf-8 -*-

from collections import namedtuple
# from sqlalchemy.orm import sessionmaker

# DBSession = sessionmaker()


class ProxyPair(namedtuple('ProxyPair', ('ip', 'port', 'location', 'scheme'))):
    __slots__ = ()

    def __str__(self):
        return str({'ip': self.ip, 'port': self.port, 'location': self.location, 'scheme': self.scheme})
