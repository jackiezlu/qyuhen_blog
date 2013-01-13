# coding=utf-8

__all__ = []


from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    # 
    # 通过继承，增加中间控制。
    # 
    # http://www.tornadoweb.org/documentation/web.html
    # 
    pass



def action(url, method = "GET", enabled = True):
    # 
    # 装饰器: 动态创建 RequestHandler 类型
    # 
    def gen_handler(func):
        if not enabled: return None

        name = func.__name__.title() + "Handler"
        handler = type(name, (BaseHandler,), { method.lower(): func })
        handler.__url__ = url
        handler.__action__ = "{0}, {1}.{2}, {3}".format(method, func.__module__, func.__name__, url)
        return handler

    return gen_handler



@action(r"/hello", enabled = True)
def hello(handler):
    # 
    # 演示
    # 
    handler.write("Hello, World!")


