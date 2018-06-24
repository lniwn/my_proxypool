# !/usr/bin/python3
# -*- coding:utf-8 -*-
import importlib
import os
import glob


def import_string(dotted_path):
    try:
        # import_module can only import package but not class
        return importlib.import_module(dotted_path)
    except ModuleNotFoundError:
        pass

    try:
        split_pair = dotted_path.rsplit('.', 1)
        module_path = split_pair[0]
        if len(split_pair) == 2:
            class_name = split_pair[1]
        else:
            class_name = None
    except (ValueError, IndexError) as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = importlib.import_module(module_path)

    try:
        if class_name is None:
            return module
        else:
            return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err


def modules_in_current(current):
    files = glob.glob(os.path.join(current, '*.py'))
    modules = [os.path.basename(f)[:-3] for f in files if os.path.isfile(f) and not f.endswith('__init__.py')]
    return modules
