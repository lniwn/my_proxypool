# !/usr/bin/python3
# -*- coding:utf-8 -*-
import abc
from aiohttp import web


class DataConsumer(abc.ABC):
    @abc.abstractmethod
    async def consume(self, *args, **kwargs) -> web.Response:
        pass


class ConsumerError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
