# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 18:39:05 2019

Experiment1: crowding and numerosity
Conditions: crowding vs nocrowding
Task: direct estimate

@author: MiaoLi
"""

import sys, random, os, time
from psychopy import visual, core, gui, data, event, monitors
from psychopy.tools.filetools import fromFile, toFile
import numpy
from PIL import Image

# =============================================================================
# some functions
# =============================================================================
# def getKeyboardResponse(validResponses,duration=0):
#     """Returns keypress and RT. Specify a duration (in secs) if you want response collection to last that long. Unlike event.waitkeys(maxWait=..), this function will not exit until duration. Use waitKeys with a maxWait parameter if you want to have a response deadline, but exit as soon as a response is received."""

#     event.clearEvents() 
#     #not strictly necessary here, but good practice - 
#     #will prevent buffer overruns if, for some reason there are too many responses in
#     #between auto-clears (e.g., from mouse, eye tracking data)

#     responded = False
#     done = False
#     rt = '*'
#     responseTimer = core.Clock()
#     while True: 
#         if not responded:
#             responded = event.getKeys(validResponses, responseTimer) 
#         if duration>0:
#             if responseTimer.getTime() > duration:
#                 break
#         else: #end on response
#             if responded:
#                 break
#     if not responded:
#         return ['*','*']
#     else:
#         return responded[0] #only get the first resp

# def get_subj_info():
#     subj_id = input('Number: ')
#     subj_group = input('Group: ')
#     subj_name = input('Name: ')
#     subj_sex = input('0 for m; 1 for f: ')
#     subj_age = input('Age: ')
#     subj_handedness = input('0 for righthanded; 1 for lefthanded： ')
#     return [subj_id, subj_group, subj_name, subj_sex, subj_age, subj_handedness]
# subj = get_subj_info()

# =============================================================================
# get subject info
# =============================================================================
try:  # try to get a previous parameters file
    expInfo = fromFile('lastParams.pickle')
except:  # if not there then use a default set
    expInfo = {'subj_id': '',
               'group': 'please ask experimenter fill this column for you', 
               'sex': '1 for male; 2 for female', 
               'age': '',
               'handedness': '1 for right; 0 for left'}
expInfo['dateStr'] = data.getDateStr()  # add the current time

# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Experiment1', fixed=['dateStr'])

if dlg.OK:
    toFile('lastParams.pickle', expInfo)  # save params to file for next time
else:
    core.quit()  # the user hit cancel so exit
    print('user cancelled')

# =============================================================================
# monitors and windows
# =============================================================================
myMonitor= monitors.Monitor('asus17', width = 57, distance = 40.5)#TODO
myMonitor.setSizePix([1024, 768])
win = visual.Window(monitor=myMonitor, size = [1024, 768], screen = 0, units='pix', fullscr = False, allowGUI = False, winType = 'pyglet', color = (0,0,0))

# =============================================================================
# instructions
# =============================================================================
message1 = visual.TextStim(win, pos=[0,+30])
message1.setText('Welcome to our experiment.')
message2 = visual.TextStim(win, pos=[0, 0])
message2.setText('Please give your best esimation.')
message3 = visual.TextStim(win, pos=[0, -30])
message3.setText('Hit spacebar when you are ready. ')
message1.draw()
message2.draw()
message3.draw()
win.flip()
event.waitKeys(keyList = ['space'])

# =============================================================================
# Save data
# =============================================================================
# fileName = expInfo['subj_id'] + expInfo['group']+expInfo['dateStr']
# dataFile = open(fileName+'.csv', 'w')  # a simple text file with 'comma-separated-values'
# dataFile.write('targetSide,oriIncrement,correct\n')

# if crowding_cons == 0: 
#     with open('infoNC.csv', 'a+', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(csv_data)

# =============================================================================
# file pool
# =============================================================================
# path_c = '/users/MiaoLi/Desktop/SCALab/Programming/Crowding_and_numerosity/Stimuli20190125/C/selected/'
# path_nc = '/users/MiaoLi/Desktop/SCALab/Programming/Crowding_and_numerosity/Stimuli20190125/NC/selected/'
# path_ref = '/users/MiaoLi/Desktop/SCALab/Programming/Crowding_and_numerosity/Stimuli20190125/REF/selected/'

path_c =   'D:/MiaoProject/Stimuli20190125/C/selected/'
path_nc =  'D:/MiaoProject/Stimuli20190125/NC/selected/'
path_ref = 'D:/MiaoProject/Stimuli20190125/REF/selected/'
dirs_c = os.listdir(path_c)
dirs_nc = os.listdir(path_nc)
dirs_ref = os.listdir(path_ref)

#crowding pool
c_60, c_61, c_62, c_63,c_64 = ([] for i in range(5))
[c_60.append(img) for img in dirs_c if img.lower().endswith('60.png')]
[c_61.append(img) for img in dirs_c if img.lower().endswith('61.png')]
[c_62.append(img) for img in dirs_c if img.lower().endswith('62.png')]
[c_63.append(img) for img in dirs_c if img.lower().endswith('63.png')]
[c_64.append(img) for img in dirs_c if img.lower().endswith('64.png')]

#nocrowding pool
nc_60, nc_61, nc_62, nc_63,nc_64 = ([] for i in range(5))
[nc_60.append(img) for img in dirs_nc if img.lower().endswith('60.png')]
[nc_61.append(img) for img in dirs_nc if img.lower().endswith('61.png')]
[nc_62.append(img) for img in dirs_nc if img.lower().endswith('62.png')]
[nc_63.append(img) for img in dirs_nc if img.lower().endswith('63.png')]
[nc_64.append(img) for img in dirs_nc if img.lower().endswith('64.png')]

#reference pool
r_60, r_61, r_62, r_63,r_64 = ([] for i in range(5))
[r_60.append(img) for img in dirs_ref if img.lower().endswith('60.png')]
[r_61.append(img) for img in dirs_ref if img.lower().endswith('61.png')]
[r_62.append(img) for img in dirs_ref if img.lower().endswith('62.png')]
[r_63.append(img) for img in dirs_ref if img.lower().endswith('63.png')]
[r_64.append(img) for img in dirs_ref if img.lower().endswith('64.png')]

# =============================================================================
# A trial
# =============================================================================

fixation = visual.TextStim(win, text= '+', bold = True, color=(-1.0, -1.0, -1.0))
fixation.setText('+')
fixation.draw()
# win.flip()
# core.wait(2)

imgstim = visual.ImageStim(win, image = str(path_c)+random.choice(c_60), units = 'pix')
imgstim.draw()
win.flip()
core.wait(0.15)

#screen for waiting response
message4 = visual.TextStim(win)
message4.setText('Please give your best estimation')
message4.draw()
win.flip()
core.wait(5)

#collecting response and present
show_text = ''
show_resp = visual.TextStim(win)

# keys = event.getKeys(keyList = ['1','2','3','4','5','6','7','8','9','0','return','backspace'])
theseKeys3 = event.getKeys(keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'return', 'backspace'])
key_resp_3 = event.BuilderKeyResponse()

# check for quit:
if "escape" in theseKeys3:
    endExpNow = True
if len(theseKeys3) >0:  # at least one key was pressed
    #key_resp_3.keys.extend(theseKeys3)  # storing all keys
    if "backspace" in theseKeys3:
        key_resp_3.keys=key_resp_3.keys[:-1]
    key_resp_3.keys.extend([key for key in theseKeys3 if key != "return" and key != "backspace"])
    show_resp.setText("".join(key_resp_3.keys))
    # convert the list of strings into a single string
    key_str = "".join(key_resp_3.keys)
    if len(key_str) !=0:
    # then convert the string to a number
        key_num = int(key_str)
if "return" in theseKeys3:
    show_resp.setText('')
    continueRoutine=False

show_resp.setText(key_num)
show_resp.draw()
win.flip()
core.wait(2)

# if 'escape' in keys:
#     core.quit()
# else:
#     if keys:
#         if 'backspace' in keys:
#             show_text = show_text[:-1]
#         show_text = show_text.join(keys)
#     show_resp.setText(show_text)
#     show_resp.draw()
#     win.flip()
#     core.wait(2)
    

def singal_trial(data_file):
    #fixation
    
    #stimuli
    
    #response
    
    pass

#win.close()
#core.quit()