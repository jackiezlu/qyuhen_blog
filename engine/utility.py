# coding=utf-8

__all__ = []


def app_path(name):
    # 
    # 返回子目录全路径
    # 
    from sys import argv
    from os.path import abspath, dirname, normpath, join

    root = dirname(abspath(argv[0]))
    return normpath(join(root, name))



def set_defaultencoding():
    # 
    # 设置默认编码
    # 
    import sys
    reload(sys)

    from sys import setdefaultencoding
    from locale import getdefaultlocale

    setdefaultencoding(getdefaultlocale()[1])



def get_module_members(module, predicate):
    # 
    # 获取模块成员
    # 
    from inspect import getmembers

    members = getmembers(module, predicate)
    return map(lambda m: m[1], members)


    
def get_package_members(package, predicate):
    # 
    # 获取包成员 (包中所有模块)
    # 
    from pkgutil import iter_modules
    from importlib import import_module

    members = []

    for _, name, ispkg in iter_modules(package.__path__, package.__name__ + "."):
        if ispkg: continue
        members.extend(get_module_members(import_module(name), predicate))

    return members









