# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 15:28:15 2019

@author: MiaoLi
"""


import os 

for i in os.listdir('.'):
    if i.endswith('.png'):
        name_new = 'r_'+ i
        print(name_new)
        os.rename(i,name_new)