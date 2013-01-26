# coding=utf-8

from engine.web import action


@action("/")
def index(handler):
    handler.render("index.html")