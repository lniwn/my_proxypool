# !/usr/bin/python3
# -*- coding:utf-8 -*-
import abc
import logging
from aiohttp import web

mylog = logging.getLogger(__name__)


class DataConsumer(abc.ABC):
    @abc.abstractmethod
    async def consume(self, *args, **kwargs) -> web.Response:
        pass


class ConsumerError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
