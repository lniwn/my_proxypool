# !/usr/bin/python3
# -*- coding:utf-8 -*-
import os.path
from datautil import generalutils


def entire() -> list:
    modules = generalutils.modules_in_current(os.path.dirname(__file__))
    return [(__name__ + '.' + m) for m in modules]
