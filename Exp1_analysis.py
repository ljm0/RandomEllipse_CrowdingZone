# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import ast
from scipy.spatial import distance
from math import atan2, pi
import numpy as np
from shapely.geometry import Polygon, Point
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
# =============================================================================
# functions I need #TODO import custom write functions
# =============================================================================
ka = 0.25#The parameter of semi-major axis of ellipse.ka > kb, radial ellipse; ka < kb, tangential ellipse; ka = kb, circle
kb = 0.1
newWindowSize = 0.5
r = 100
loop_number = 1
def defineVirtualEllipses(coordinate):
# parameter for a and b; When adjust them, DO NOT forget to change in the drawEllipse
    '''
    This function defines the virtual ellipse. coordinate: the center of the ellipse
    ka and kb are parameters of semi-major axis and semi-minor axis of the ellipse, respectivly.
    ka and kb should be defined according to crowding zone areas. This function reutrns coordiante of ellipse(the center),
    ellipse_axis(a and b for ellipse) and 2 angles (radial and tangential direction)
    '''
    e = distance.euclidean(coordinate, (0,0)) #np.sqrt((coordinate[0])**2 + (coordinate[1])**2)    
    a = ka * e
    b = kb * e
    ellipse_axis = [a, b]
    #radial angle
    angle_rad = atan2(coordinate[1],coordinate[0])
    angle_radial = angle_rad*180/pi
    angle_tangential = angle_radial + 90
    V_ellipse = (coordinate[0],coordinate[1], ellipse_axis[0],ellipse_axis[1], angle_radial, angle_tangential)
    return V_ellipse
def ellipseToPolygon(ellipse, n=200):
    '''
    This function transfer an ellipse to Polygon in radial and tangential directions
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle, angle2 in ellipse: #angle2: tangential direction of the ellilpse, not used in intersection expectation
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        pointE = np.empty((n, 2))
        pointE[:, 0] = x0 + a * ca * ct - b * sa * st
        pointE[:, 1] = y0 + a * sa * ct + b * ca * st
        result.append(pointE)
    result2 = []
    for x0, y0, a, b, angle, angle2 in ellipse: #angle2: tangential direction of the ellilpse, not used in intersection expectation
        angle2 = np.deg2rad(angle2)
        sa2 = np.sin(angle2)
        ca2 = np.cos(angle2)
        pointE2 = np.empty((n, 2))
        pointE2[:, 0] = x0 + a * ca2 * ct - b * sa2 * st
        pointE2[:, 1] = y0 + a * sa2 * ct + b * ca2 * st
        result2.append(pointE2)
    #ellipseA, ellipseB are the dots of two ellipse
    ellipse1 = result[0]
    ellipse2 = result2[0]
#    ellipseB = result[1]
#    ellipse1 = Polygon(ellipse1)
#    ellipse2 = Polygon(ellipse2)
    return ellipse1, ellipse2
def drawEllipse_full(e_posi):
    """
    This function allows to draw more than one ellipse. The parameter is 
    a list of coordinate (must contain at least two coordinates)
    The radial and tangential ellipses for the same coordinates are drawn.
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0,0))
        eccentricities.append(eccentricities0)
    #radial
    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0 = angle_rad0*180/pi
        angle_deg.append(angle_deg0)
    my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j])
            for j in range(len(e_posi))]
    
    #tangential
    angle_deg2 = []
    for ang in range(len(e_posi)):
        angle_rad0_2 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0_2 = angle_rad0_2*180/pi + 90
        angle_deg2.append(angle_deg0_2)
    my_e2 = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j]+90)
            for j in range(len(e_posi))]
    
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(np.random.rand())
        e.set_facecolor(np.random.rand(3))
    for e2 in my_e2:
        ax.add_artist(e2)
        e2.set_clip_box(ax.bbox)
        e2.set_alpha(np.random.rand())
        e2.set_facecolor(np.random.rand(3))
    ax.set_xlim([-800, 800])
    ax.set_ylim([-500, 500])
    ax.set_title('f_%s_wS_%s_eS_%s_%s_E.png' %(r,newWindowSize,ka,kb))
    try:
        loop_number
    except NameError:
        var_exists = False
    else:
        var_exists = True
        plt.savefig('%s_f_%s_wS_%s_eS_%s_%s_E.png' %(loop_number,r,newWindowSize,ka,kb))
# =============================================================================
# import the stimuli display details
# =============================================================================
# file = r'\Users\MiaoLi\Desktop\SCALab\Crowding_in_percived_numerosity\Exp1_crowding_numerosity_direct_estimation_idea1\StimuliDetails\SelectedStimuliInfo.xlsx'
file = r'D:\MiaoProject\count\backup\SelectedStimuliInfo.xlsx'
stimuliInfo_df=pd.read_excel(file,header = None)
posi_lists_temp = stimuliInfo_df[4].tolist()

# df to list
posi_list=[]
for i in posi_lists_temp:
    i = ast.literal_eval(i)# megic! remore ' ' of the str
    posi_list.append(i)
# =============================================================================
# inspect disks fall into others crowding zones
# =============================================================================

dic_count_in_crowdingZone = {}
list_count_in_crowdingZone = []
for indexPosiList in range(0,len(posi_list)):
    display_posi = posi_list[indexPosiList]
    #final ellipses
    ellipses = []
    for posi in display_posi:
        e = defineVirtualEllipses(posi)
        ellipses.append(e)
    # final_ellipses = list(set(ellipses)) #if order doest matter
    final_ellipses = list(OrderedDict.fromkeys(ellipses)) #ordermatters
    count_in_crowdingZone = 0
        #crowding zones after reomve overlapping areas
    for count, i in enumerate(final_ellipses, start = 1):
        ellipsePolygon = ellipseToPolygon([i])[0] #radial ellipse
        # ellipsePolygonT = ellipseToPolygon([i])[1]#tangential ellipse
        epPolygon = Polygon(ellipsePolygon)
        # epPolygonT = Polygon(ellipsePolygonT)
        # radial_area_dic[(i[0],i[1])] = [] #set the keys of the dictionary--taken_posi
        for posi in display_posi:
            if epPolygon.contains(Point(posi)) == True:
                count_in_crowdingZone += 1
    count_number_end = count_in_crowdingZone-len(display_posi)
    dic_temp_item = {indexPosiList: count_number_end}
    dic_count_in_crowdingZone.update(dic_temp_item)
    list_count_in_crowdingZone.append(count_number_end)
# =============================================================================
# save count numbers to big totalData.xlsx
# SelectedStimuliInfo.xlsx 2 col - totalData.xlsx J col（imageFile）
# SelectedStimuliInfo.xlsx 3 col - totalData.xlsx L col （N_disk）
# we add two cols to totalData.xlsx
# one corresponding to index（key）,
# one corresponding to count（value）
# =============================================================================
file2 = r'D:\MiaoProject\count\backup\totalData.xlsx'
totalData_df = pd.read_excel(file2)
col_image = stimuliInfo_df.ix[:, [1]]
col_N_disk = stimuliInfo_df.ix[:, [2]]

#get imageFinne number
def imageFile_to_number(filename):
    tempFileNumber = ''
    for in_file in filename:
        tempFileNumber = tempFileNumber + in_file
        if not tempFileNumber.isdigit():
            tempFileNumber = tempFileNumber[0:len(tempFileNumber)-1]
            return int(tempFileNumber)
totalData_df['fileNumber'] = totalData_df['imageFile'].map(imageFile_to_number)

# change col name
name_list = list(range(0,62))
name_list = [str(x) for x in name_list]
name_list[0] = 'index_stimuliInfo'
name_list[2] = 'fileNumber'
name_list[3] = 'N_disk'
stimuliInfo_df.columns = name_list
# add count number to a new col
stimuliInfo_df.insert(1, 'count_number',list_count_in_crowdingZone)
# select three cols 'fileNumber','N_disk','count'
col_n = ['fileNumber','N_disk','index_stimuliInfo','count_number']
selected_df = pd.DataFrame(stimuliInfo_df,columns = col_n)
#merge two dataframe
#FIXME the number of row is different
final_df = pd.merge(totalData_df, selected_df, how='left', on=['fileNumber','N_disk'])
final_df.to_excel('addCount_totalData.xlsx')


#group_total_df = pd.pivot_table(totalData_df, index=['fileNumber','N_disk'])
#group_stimuliInfo_df = pd.pivot_table(stimuliInfo_df, index=['fileNumber','N_disk'])
# for big_cols in range(0,len(totalData_df)):
#     pass



























