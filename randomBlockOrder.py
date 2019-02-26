# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 18:18:25 2019

@author: MiaoLi

This code generates the condition files for each participants.
"""

from numpy.random import shuffle
import copy, sys, csv


# Run multiple times
try:
    _, loop_number = sys.argv
except Exception as e:
    pass

# The block list I want 
myCons = ['condition0.3.xlsx', 'condition0.7.xlsx', 'condition0.6.xlsx', 'condition0.5.xlsx', 'condition0.4.xlsx']
shuffle(myCons)
myCons2 = copy.copy(myCons)
myCons2.reverse()
myCons.extend(myCons2)
print(myCons)

ref_image_1 = ['5_c_2_f_100_wS_0.7_eS_0.15811388300841897_0.15811388300841897_55.png',
              '32_c_2_f_100_wS_0.6_eS_0.15811388300841897_0.15811388300841897_51.png',
              '5_c_2_f_100_wS_0.5_eS_0.15811388300841897_0.15811388300841897_43.png',
              '10_c_2_f_100_wS_0.4_eS_0.15811388300841897_0.15811388300841897_33.png',
              '6_c_2_f_100_wS_0.3_eS_0.15811388300841897_0.15811388300841897_23.png']
Number_1 = [55,51,43,33,23]

ref_image_2 = ['6_c_2_f_100_wS_0.7_eS_0.15811388300841897_0.15811388300841897_54.png',
              '1_c_2_f_100_wS_0.6_eS_0.15811388300841897_0.15811388300841897_50.png',
              '1_c_2_f_100_wS_0.5_eS_0.15811388300841897_0.15811388300841897_42.png',
              '1_c_2_f_100_wS_0.4_eS_0.15811388300841897_0.15811388300841897_32.png',
              '1_c_2_f_100_wS_0.3_eS_0.15811388300841897_0.15811388300841897_22.png']
Number_2 = [54,50,42,32,22]

ref_image_3 = ['4_c_2_f_100_wS_0.7_eS_0.15811388300841897_0.15811388300841897_56.png',
              '3_c_2_f_100_wS_0.6_eS_0.15811388300841897_0.15811388300841897_52.png',
              '2_c_2_f_100_wS_0.5_eS_0.15811388300841897_0.15811388300841897_44.png',
              '3_c_2_f_100_wS_0.4_eS_0.15811388300841897_0.15811388300841897_34.png',
              '3_c_2_f_100_wS_0.3_eS_0.15811388300841897_0.15811388300841897_24.png']

Number_3 = [56,52,44,34,24]

myConsDic = {'condition0.3.xlsx': [ref_image_1[4], Number_1[4], ref_image_2[4], Number_2[4], ref_image_3[4], Number_3[4]],
             'condition0.7.xlsx': [ref_image_1[0], Number_1[0], ref_image_2[0], Number_2[0], ref_image_3[0], Number_3[0]],
             'condition0.6.xlsx': [ref_image_1[1], Number_1[1], ref_image_2[1], Number_2[1], ref_image_3[1], Number_3[1]],
             'condition0.5.xlsx': [ref_image_1[2], Number_1[2], ref_image_2[2], Number_2[2], ref_image_3[2], Number_3[2]],
             'condition0.4.xlsx': [ref_image_1[3], Number_1[3], ref_image_2[3], Number_2[3], ref_image_3[3], Number_3[3]]}

#write them to a csv
with open ('blockOrder%s.csv' %(loop_number), 'a+', newline='') as csvfile:
    fieldnames = ['winsize','ref_image1','Number1','ref_image2','Number2','ref_image3','Number3'] #headers
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for idx, condition in enumerate(myCons): #correct indexing
        if idx == 5:
            idx = 4
        elif idx == 6:
            idx = 3
        elif idx == 7:
            idx =2
        elif idx == 8:
            idx =1
        elif idx == 9:
            idx =0
        writer.writerow({'winsize':condition, 
                         'ref_image1': myConsDic.get(condition)[0],
                         'Number1':myConsDic.get(condition)[1], 
                         'ref_image2':myConsDic.get(condition)[2],
                         'Number2':myConsDic.get(condition)[3],
                         'ref_image3':myConsDic.get(condition)[4],
                         'Number3':myConsDic.get(condition)[5]})