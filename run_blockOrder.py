# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 23:09:08 2019

@author: MiaoLi
"""


import os
import time

i_loop = 1

start = time.time()
while(i_loop <= 30):
    os.system('python randomBlockOrder.py' + ' ' + str(i_loop))
    i_loop += 1
end = time.time()

print('time', str(end-start))
# import virtual_ellipses_underPython
# virtual_ellipses_underPython.main()
