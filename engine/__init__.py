# coding=utf-8

__all__ = ["app"]


# 
# 编码风格提示:
# 
#   1. 以 4 空格代替 TAB。
#   2. 模块成员间空 3 行，类成员空 2 行，代码块空 1 行。增大视觉分块效果。
#   3. 注释是注释，文档 (__doc__) 是文档，不可混为一谈。
#   4. 单行代码注释添加到后部，块注释使用单独行。
#   5. 避免在 globals 写太多 import 语句，一来不便于名字维护，二则不方便重构。除非性能需要。
#   6. 函数中的名字尽可能简短，和类型、方法名字分开，便于阅读。
#   7. 不要吝啬用括号，适当使用更利于阅读。
#   8. 模块中不被外部引用的名字以单下划线开始，在头部提供 __all__。
#   9. 类私有成员名字以单下划线开始。
# 
# 将想法(包括未实现)尽可能写到注释里面，可以添加特殊标记便于搜索。
# 


def _settings():
    # 
    # 合并系统配置
    # 
    # 系统将配置分成 system 和 user 两部分，分别放在不同的目录。
    # 其中 user settings 会覆盖 system settings 同名项。
    # 
    # 提示: 
    #   import 优先查找当前模块所在目录，__import__、import_module 从根路径查找。
    #   操控内置模块，最好显式引入 __builtin__。
    # 
    import __builtin__
    from importlib import import_module
    import settings                             # 导入包目录中的 system settings。

    user_settings = import_module("settings")   # 导入根目录 user settings。
    vars(settings).update(vars(user_settings))  # 合并 __dict__。
    __builtin__.settings = settings             # 添加到内置模块，便于访问。



def _set_signal():
    # 
    # 处理退出信号
    # 
    from signal import signal, SIGINT, SIGTERM

    def handler(signum, frame):
        print "bye..."
        exit(0)

    signal(SIGINT, handler)
    signal(SIGTERM, handler)



def init():
    # 
    # 初始化
    # 
    from utility import set_defaultencoding
    set_defaultencoding()

    _settings()
    _set_signal()



init()


