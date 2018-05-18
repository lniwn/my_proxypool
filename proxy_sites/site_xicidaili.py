# !/usr/bin/python3
# -*- coding:utf-8 -*-
from . import Registerable
from datacenter import ProxyPair


class SiteXici(Registerable):
    def yield_proxy(self):
        yield ProxyPair(ip='1.1.1.1', port='80', location='中国', scheme='http')
