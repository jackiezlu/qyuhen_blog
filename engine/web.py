# coding=utf-8

__all__ = []


from tornado.web import RequestHandler
from tornado.escape import url_escape, url_unescape


class BaseHandler(RequestHandler):
    # 
    # 通过继承，增加中间控制。
    # 
    # http://www.tornadoweb.org/documentation/web.html
    # 
    USER_TOKEN = "__token__"
    LOGIN_NEXT = "__next__"


    def prepare(self):
        #
        # 处理登录、缓存。
        # 
        self._save_next_url()
        self._set_nocache()


    def get_error_html(self, status_code, **kwargs):
        # 
        # 查找错误页面: <status_code>.html，或者返回 error.html。
        # 页面模板可以获取 status_code 值。
        #
        from os.path import exists
        from utility import app_path

        for name in (status_code, "error"):
            filename = app_path("{0}/{1}.html".format(settings.TEMPLATE, name))
            if exists(filename): return self.render_string(filename, status_code = status_code)

        return "Template file not found! {0}/{1}.html\n".format(settings.TEMPLATE, status_code)


    def get_current_user(self):
        # 
        # 使用不可逆的唯一标识。
        # 使用有过期时间和签名的安全Cookie。
        # 
        return self.get_secure_cookie(self.USER_TOKEN)


    def _set_nocache(self):
        # 
        # 阻止浏览器缓存。
        # 适用于访问 Ajax，避免无法刷新。
        # 
        if self.action.nocache: self.set_header("Cache-Control", "No-Cache")


    def _save_next_url(self):
        # 
        # 保存 login_url 页面的 next 参数，以便登录后跳回。
        # 
        if self.request.path == self.get_login_url():
            next = self.get_argument("next") or "/"
            self.set_secure_cookie(self.LOGIN_NEXT, next, expires_days = None)


    def signin(self, name, expires_days = None, redirect = True):
        # 
        # 写入登录凭证信息。
        # 
        # 访问登录页面时，会将 next 参数值写入 cookie。
        # 登录方法从 cookie 获取要跳转的页面。
        # 
        # 参数:
        #   name            用户标识
        #   expires_days    保留天数 (None 表示浏览器 Session)
        #   redirect        是否跳转回登录前的页面
        # 
        self.set_secure_cookie(self.USER_TOKEN, name, expires_days = expires_days)

        next = self.get_secure_cookie(self.LOGIN_NEXT) or "/"
        self.clear_cookie(self.LOGIN_NEXT)
        if redirect: self.redirect(next)


    def signout(self, redirect_url = "/"):
        # 
        # 清除全部信息。
        # 
        # 参数:
        #   redirect_url    注销后跳转的页面，None 不跳转。
        # 
        self.clear_all_cookies()
        if redirect_url: self.redirect(redirect_url)



# 
# 修改 tornado.web 默认错误处理方式
# 
from tornado.web import ErrorHandler
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
        from tornado.web import authenticated

        # 检查是否有效，过滤重复定义。
        if not enabled: return None                                      
        if not isfunction(func): return func

        # 类型成员
        kwargs["name"] = "{0}.{1}".format(func.__module__, func.__name__)
        attrs = { 
            method.lower(): auth and authenticated(func) or func,           # 添加 authenticated 装饰器处理
            "action": namedtuple("Action", kwargs.keys())(**kwargs) 
        }

        # 生成 RequestHandler 类型
        name = func.__name__.title() + "Handler"
        return type(name, (BaseHandler,), attrs)

    return gen_handler


