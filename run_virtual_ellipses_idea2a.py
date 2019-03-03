# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 12:49:29 2019

@author: MiaoLi
"""
import os
import time

i_loop=1

start = time.time()
while(i_loop <= 10):
    os.system('python virtual_ellipses_Idea2a.py' + ' ' + str(i_loop))
    i_loop += 1
end = time.time()

print('time', str(end-start))

