# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 22:12:33 2018

@author: Miao
"""

import numpy as np
import math 
import random
from math import pi, cos, sin

#some parameters
my_canvas = self.offline_canvas()
xc = 0#my_canvas.xcenter() 512? in opensesame 3, the center is 0,0
yc = 0#my_canvas.ycenter() 384?
disk_pixel =10

#get independent variables from block loop
eccentricity = exp.get("Eccentricity")  #in pixel e=7° 7,5
N_of_disks = 5 #exp.get("Number_of_disks") #3， 5
disk_size = exp.get("Disk_size") # 5,7,9
N_of_locations = 11#exp.get("Number_of_locations") # 6, 9, 12, 15, 18, 21; locations on the imaginary circle
crowding_zone = eccentricity/2
condition =  "tangential" #"radial"  #
distance_disk = 20

#some conditions to set
vary_disk_distance = "no" #whether distances between disks vary within trial


#show stimuli
my_canvas.fixdot() #(x=xc, y=yc,style=u'small-filled')

#target_disk 
imaginary_circle_position_c = calulateCirclePosition(xc, yc, eccentricity, N_of_locations)


for i in range(0,N_of_locations):
	x0 = imaginary_circle_position_c[i][0]#central disk x
	y0 = imaginary_circle_position_c[i][1]#central disk y	
	
	'''
	xi = x0 * (eccentricity-distance_disk)/eccentricity
	yi = y0 * (eccentricity-distance_disk)/eccentricity
	xo = x0 * (eccentricity+distance_disk)/eccentricity
	yo = y0 * (eccentricity+distance_disk)/eccentricity
	xi2 = x0 * (eccentricity-distance_disk*2)/eccentricity
	yi2 = y0 * (eccentricity-distance_disk*2)/eccentricity
	xo2 = x0 * (eccentricity+distance_disk*2)/eccentricity
	yo2 = y0 * (eccentricity+distance_disk*2)/eccentricity
	xi3 = x0 * (eccentricity-distance_disk*3)/eccentricity
	yi3 = y0 * (eccentricity-distance_disk*3)/eccentricity
	xo3 = x0 * (eccentricity+distance_disk*3)/eccentricity
	yo3 = y0 * (eccentricity+distance_disk*3)/eccentricity
	xi4 = x0 * (eccentricity-distance_disk*4)/eccentricity
	yi4 = y0 * (eccentricity-distance_disk*4)/eccentricity
	xo4 = x0 * (eccentricity+distance_disk*4)/eccentricity
	yo4 = y0 * (eccentricity+distance_disk*4)/eccentricity
		
	x1 = yo + x0 - y0
	y1 = x0 - xo + y0
	x2 = x0 + y0 - yo
	y2 = xo - x0 + y0
	x12= yo2 + x0 -y0
	y12 = x0 - xo2 + y0
	x22 = x0 + y0 - yo2
	y22 = xo2 -x0 + y0
	'''
	#get radial positions dictionary  radial_xy_dic = {"i":[xi, yi],"o":[xo, yo]}
	radial_xy_1 = computeRadialDiskCoordinate(x0, y0, 1)
	radial_xy_2 = computeRadialDiskCoordinate(x0, y0, 2)
	radial_xy_3 = computeRadialDiskCoordinate(x0, y0, 3)
	radial_xy_4 = computeRadialDiskCoordinate(x0, y0, 4)

	#get tangential positon dictionary  tan_xy_dic = {"l": [xl, yl], "r": [xr, yr]}
	tan_xy_1 = computeTangentialDiskCoordinate(x0, y0, 1)
	tan_xy_2 = computeTangentialDiskCoordinate(x0, y0, 2)
	tan_xy_3 = computeTangentialDiskCoordinate(x0, y0, 3)
	tan_xy_4 = computeTangentialDiskCoordinate(x0, y0, 4)

	#print(radial_xy_1['i'][0], tan_xy_1["l"][1])
	
	if condition == "radial":
		if vary_disk_distance== "no":
			if N_of_disks == 3:
				'''
				my_canvas.circle(x0, y0, disk_size, fill = True, color = 'white')
				my_canvas.circle(xi, yi, disk_size, fill = True, color = 'white')
				my_canvas.circle(xo, yo, disk_size, fill = True, color = 'white')
				'''
				my_canvas.circle(x0, y0, disk_size, fill = True, color = 'white')
				my_canvas.circle(radial_xy_1["i"][0], radial_xy_1["i"][1], disk_size, fill = True, color = 'white')
				my_canvas.circle(radial_xy_1["o"][0],radial_xy_1["o"][1], disk_size, fill = True, color = 'white')
				
				
			elif N_of_disks == 5:
				my_canvas.circle(x0, y0, disk_size, fill = True, color = 'white')
				my_canvas.circle(radial_xy_1["i"][0], radial_xy_1["i"][1], disk_size, fill = True, color = 'white')
				my_canvas.circle(radial_xy_1["o"][0],radial_xy_1["o"][1], disk_size, fill = True, color = 'white')
				my_canvas.circle(radial_xy_2["i"][0], radial_xy_2["i"][1], disk_size, fill = True, color = 'white')
				my_canvas.circle(radial_xy_2["o"][0],radial_xy_2["o"][1], disk_size, fill = True, color = 'white')
				#my_canvas.circle(xi2, yi2, disk_size, fill = True, color = 'white')
				#my_canvas.circle(xo2, yo2,disk_size, fill = True, color = 'white')
			else:
				my_canvas.circle(x0, y0, disk_size, fill = True, color = 'white')
		
		
		# vary_disk_distance within trails == yes
		else: 
			
			if N_of_disks == 3:
			
						
	else: #tangential condition

		if N_of_disks == 3:
			my_canvas.circle(x0, y0, disk_size, fill = True, color = 'white')
			my_canvas.circle(tan_xy_1["r"][0],tan_xy_1["r"][1], disk_size, fill = True, color = 'white')
			my_canvas.circle(tan_xy_1["l"][0],tan_xy_1["l"][1],  disk_size, fill = True, color = 'white')
			
		elif N_of_disks == 5:
			my_canvas.circle(x0, y0, disk_size, fill = True, color = 'white')
			my_canvas.circle(tan_xy_1["r"][0],tan_xy_1["r"][1], disk_size, fill = True, color = 'white')
			my_canvas.circle(tan_xy_1["l"][0],tan_xy_1["l"][1],  disk_size, fill = True, color = 'white')
			my_canvas.circle(tan_xy_2["r"][0],tan_xy_2["r"][1], disk_size, fill = True, color = 'white')
			my_canvas.circle(tan_xy_2["l"][0],tan_xy_2["l"][1],  disk_size, fill = True, color = 'white')
			#my_canvas.circle(x12, y12, disk_size, fill = True, color = 'white')
			#my_canvas.circle(x22, y22,disk_size, fill = True, color = 'white')
