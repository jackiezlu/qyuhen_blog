# coding=utf-8

from engine.web import action


@action("/")
def index(handler):
    handler.render("index.html")



@action(r"/hello", auth = True, order = 10)
def hello(handler):
    # 
    # 演示
    # 
    handler.write("Hello, World!\n")
    handler.write(handler.current_user + "\n")



@action(r"/login", nocache = True)
def login(handler):
    # 
    # 显示登录页面
    # 
    handler.write('<a href="/signin">signin</a>\n'.format(next))



@action(r"/signin")
def signin(handler):    
    # 
    # 登录页面 submit，通常会传入 username, password 进行验证。
    # 
    handler.signin("yuhen")


