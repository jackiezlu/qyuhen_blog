# coding=utf-8

__all__ = []


from tornado.web import RequestHandler, ErrorHandler



class BaseHandler(RequestHandler):
    # 
    # 通过继承，增加中间控制。
    # 
    # http://www.tornadoweb.org/documentation/web.html
    # 
    def prepare(self):
        #
        # 处理登录、缓存。
        # 
        pass



# 
# 修改 tornado.web 默认错误处理方式
# 
ErrorHandler.__bases__ = (BaseHandler,)



def action(url, method = "GET", enabled = True, order = 0, auth = False, nocache = False):
    # 
    # 装饰器: 动态创建 RequestHandler 类型
    # 
    # 参数:
    #   url         路由正则表达式。
    #   method      GET、POST、PUT、DELETE、HEAD。
    #   enabled     是否有效。
    #   order       路由规则排列顺序 (升序)。
    #   auth        必须登录。
    #   nocache     禁用浏览器端缓存，通常用于返回 JSON。
    #    
    kwargs = locals().copy()

    def gen_handler(func):
        from collections import namedtuple
        from inspect import isfunction

        # 检查是否有效，多虑重复定义。
        if not enabled: return None                                      
        if not isfunction(func): return func

        # 类型成员
        kwargs["name"] = "{0}.{1}".format(func.__module__, func.__name__)
        attrs = { 
            method.lower(): func, 
            "action": namedtuple("Action", kwargs.keys())(**kwargs) 
        }

        # 生成 RequestHandler 类型
        name = func.__name__.title() + "Handler"
        return type(name, (BaseHandler,), attrs)

    return gen_handler



@action(r"/hello", order = 10)
def hello(handler):
    # 
    # 演示
    # 
    handler.write("Hello, World!")


