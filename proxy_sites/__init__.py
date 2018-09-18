# !/usr/bin/python3
# -*- coding:utf-8 -*-
import abc
import logging

sites = dict()
mylog = logging.getLogger(__name__)


class Registerable(abc.ABC):
    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls, *args, **kwargs)
        sites[inst.__class__.__name__] = inst
        return inst

    @abc.abstractmethod
    async def yield_proxy(self, *args, **kwargs):
        yield None


def register_all(condition=None):
    """
    注册proxy_sites文件夹下所有插件，插件增删之后，需要重新调用此函数
    外部可通过condition回调进行过滤，原型为bool condition(class name, class)
    :param condition: 过滤条件，callable对象，返回True/False来控制是否注册对应插件
    :return: None
    """
    # option 1 静态加载
    # step1: 指定__all__
    # step2: 导入所有模块from . import *
    # step3: 使用python3独有的方法__subclasses__获取所有子类
    # for sub in Registerable.__subclasses__():
    #     sub()

    # option 2 动态加载
    # step1: 获取所有模块名
    # step2: 使用importlib.import_module显示导入所有模块
    # step3: 循环遍历所有class
    import importlib
    import inspect
    import glob
    import os

    files = glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))
    modules = [os.path.basename(f)[:-3] for f in files if os.path.isfile(f) and not f.endswith('__init__.py')]
    sites.clear()
    for n in modules:
        m = importlib.import_module(__name__ + '.' + n)
        for name, obj in inspect.getmembers(m, inspect.isclass):
            if (not callable(condition)) or condition(name, obj):
                if issubclass(obj, Registerable) and (obj is not Registerable):
                    obj()


def entire() -> list:
    return list(sites.values())
