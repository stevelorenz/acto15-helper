#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #####################################
# Author : Xiang,Zuo
# E-Mail : xianglinks@gmail.com
# Date   :
# About  :
# #####################################


import numpy

a = [1, 2, 3, 4]
b = numpy.average(a)
c = numpy.std(a)

d = c * numpy.sqrt(4.0 / 3)
print(numpy.sqrt(4.0 / 3))

print b
print c
print d
