# !/usr/bin/python3
# -*- coding:utf-8 -*-
import os.path
import logging
from datautil import generalutils

mylog = logging.getLogger(__name__)


def entire() -> list:
    modules = generalutils.modules_in_current(os.path.dirname(__file__))
    return [(__name__ + '.' + m) for m in modules]
