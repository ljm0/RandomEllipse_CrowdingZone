# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 17:28:02 2019

@author: MiaoLi
"""


import os
import time

i_loop=1

start = time.time()
while(i_loop <= 1):
    os.system('python virtual_ellipses_Idea2b_1.py' + ' ' + str(i_loop))
    i_loop += 1
end = time.time()

print('time', str(end-start))
