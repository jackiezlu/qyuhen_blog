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
