# !/usr/bin/python3
# -*- coding:utf-8 -*-
import abc

sites = dict()


class Registerable(abc.ABC):
    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls, *args, **kwargs)
        sites[inst.__class__.__name__] = inst
        return inst

    @abc.abstractmethod
    def yield_proxy(self):
        yield None


def register_all():
    # option 1
    # step1: 指定__all__
    # step2: 导入所有模块from . import *
    # step3: 使用python3独有的方法__subclasses__获取所有子类
    # for sub in Registerable.__subclasses__():
    #     sub()

    # option 2
    # step1: 获取所有模块名
    # step2: 使用importlib.import_module显示导入所有模块
    # step3: 循环遍历所有class
    import importlib
    import inspect
    import glob
    import os

    files = glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))
    modules = [os.path.basename(f)[:-3] for f in files if os.path.isfile(f) and not f.endswith('__init__.py')]
    for n in modules:
        m = importlib.import_module(__name__ + '.' + n)
        for _, obj in inspect.getmembers(m, inspect.isclass):
            if issubclass(obj, Registerable) and (obj is not Registerable):
                obj()
