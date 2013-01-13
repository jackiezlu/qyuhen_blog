# coding=utf-8

from engine.web import action


@action(r"/test/(?P<name>\w+)")
def test(handler, name):
    handler.write("Test:" + name)


