感谢yuhen带我这个py白菜来学习python这门语言和他的重构过程

在此记录学习过程中遇到的问题

问题1：

函数set_defaultencoding()中我为何刚刚import sys又reload(sys)一次呢？
@ set_defaultencoding 函数在虚拟机初始化过程中被 site.py 删掉了。



