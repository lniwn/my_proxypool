# !/usr/bin/python3
# -*- coding:utf-8 -*-
from . import Registerable
from datacenter import ProxyPair


class SiteXici(Registerable):
    async def yield_proxy(self, *args, **kwargs):
        return []
