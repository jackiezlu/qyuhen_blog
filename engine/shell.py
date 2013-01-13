# coding=utf-8


__all__ = ["run"]


from cmd import Cmd
from shlex import split


class Shell(Cmd, object):
    #
    # 交互式命令行工具
    # 
    # 支持常用快捷键。
    # 支持命令和参数补全。
    # 
    # TODO:
    # 
    intro = "Q.yuhen shell, version 0.0.0.1\n"
    prompt = ":: "


    def default(self, line):
        # 
        # 退出或显示未知命令提示。
        # EOF 是 <ctrl> + d。
        # 
        if line in ("exit", "quit", "bye", "EOF"):
            print "bye..."
            return True

        super(Shell, self).default(line)


    def postcmd(self, stop, line):
        # 
        # 每次命令执行完成输出空行分隔。
        # 
        print
        return super(Shell, self).postcmd(stop, line)   


    def do_python(self, line):
        # 
        # 执行 Python 交互环境，并导入当前名字空间，以便进行控制。
        # 通常用于调试。
        # 
        from code import interact
        interact(local = globals())


    def do_clean(self, line):
        #
        # 清理垃圾文件
        # 
        # 种类: .py[co]
        #
        from os import popen
        popen('find . -name "*.py[co]" | xargs rm -rf')


    @staticmethod
    def set_do_funcs(name):
        # 
        # 动态绑定外部方法
        #
        # 从 sys.modules[name] 中查找所有符合签名的函数，动态绑定到 SHELL。
        # 采用 lambda 包装，提供 self 参数。
        # 函数签名: do_*(line)
        #
        from sys import modules
        from inspect import getmembers, isfunction

        module = modules.get(name, None)
        if module:
            funcs = getmembers(module, lambda m: isfunction(m) and m.__name__.startswith("do_"))
            for name, func in funcs:
                f = lambda self, line: func(line)   # 包装函数，符合签名需要。
                setattr(Shell, name, f)             # 添加 do_* 实例方法



def run(name):
    # 
    # 运行 SHELL
    # 
    # 支持命令行参数和交互式两种方式操作。
    # $ ./shell.py test arg1
    # 
    from sys import argv
    from subprocess import list2cmdline
    
    Shell.set_do_funcs(name)
    shell = Shell()

    if len(argv) > 1:
        # 命令行方式
        cmd, line = "do_" + argv[1], list2cmdline(argv[2:])
        do = getattr(shell, cmd, None)
        if do: do(line)
    else:
        # REPL
        shell.cmdloop()



