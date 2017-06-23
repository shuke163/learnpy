#!/usr/bin/python
# -*- coding:utf-8 -*-


class Foo:
    def __call__(self, *args, **kwargs):
        print('======>')

obj=Foo()
# print(type(obj))

obj()




# print(type(Foo))

