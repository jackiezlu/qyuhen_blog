#!/usr/bin/env python
# coding=utf-8


def do_hello(line):
	print "Hello, World!"
	print line



def main():
	from engine.shell import run
	run(__name__)



if __name__ == "__main__":
	main()