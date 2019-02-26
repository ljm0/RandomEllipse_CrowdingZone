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

# # =============================================================================
# # some functions
# # =============================================================================
# # def getKeyboardResponse(validResponses,duration=0):
# #     """Returns keypress and RT. Specify a duration (in secs) if you want response collection to last that long. Unlike event.waitkeys(maxWait=..), this function will not exit until duration. Use waitKeys with a maxWait parameter if you want to have a response deadline, but exit as soon as a response is received."""

# #     event.clearEvents() 
# #     #not strictly necessary here, but good practice - 
# #     #will prevent buffer overruns if, for some reason there are too many responses in
# #     #between auto-clears (e.g., from mouse, eye tracking data)

# #     responded = False
# #     done = False
# #     rt = '*'
# #     responseTimer = core.Clock()
# #     while True: 
# #         if not responded:
# #             responded = event.getKeys(validResponses, responseTimer) 
# #         if duration>0:
# #             if responseTimer.getTime() > duration:
# #                 break
# #         else: #end on response
# #             if responded:
# #                 break
# #     if not responded:
# #         return ['*','*']
# #     else:
# #         return responded[0] #only get the first resp

# # def get_subj_info():
# #     subj_id = input('Number: ')
# #     subj_group = input('Group: ')
# #     subj_name = input('Name: ')
# #     subj_sex = input('0 for m; 1 for f: ')
# #     subj_age = input('Age: ')
# #     subj_handedness = input('0 for righthanded; 1 for lefthanded： ')
# #     return [subj_id, subj_group, subj_name, subj_sex, subj_age, subj_handedness]
# # subj = get_subj_info()

# # =============================================================================
# # get subject info
# # =============================================================================
# try:  # try to get a previous parameters file
#     expInfo = fromFile('lastParams.pickle')
# except:  # if not there then use a default set
#     expInfo = {'subj_id': '',
#                'group': 'please ask experimenter fill this column for you', 
#                'sex': '1 for male; 2 for female', 
#                'age': '',
#                'handedness': '1 for right; 0 for left'}
# expInfo['dateStr'] = data.getDateStr()  # add the current time

# # present a dialogue to change params
# dlg = gui.DlgFromDict(expInfo, title='Experiment1', fixed=['dateStr'])

# if dlg.OK:
#     toFile('lastParams.pickle', expInfo)  # save params to file for next time
# else:
#     core.quit()  # the user hit cancel so exit
#     print('user cancelled')

# # =============================================================================
# # monitors and windows
# # =============================================================================
# myMonitor= monitors.Monitor('asus17', width = 57, distance = 40.5)#TODO
# myMonitor.setSizePix([1024, 768])
# win = visual.Window(monitor=myMonitor, size = [1024, 768], screen = 0, units='pix', fullscr = False, allowGUI = False, winType = 'pyglet', color = (0,0,0))

# # =============================================================================
# # instructions
# # =============================================================================
# message1 = visual.TextStim(win, pos=[0,+30])
# message1.setText('Welcome to our experiment.')
# message2 = visual.TextStim(win, pos=[0, 0])
# message2.setText('Please give your best esimation.')
# message3 = visual.TextStim(win, pos=[0, -30])
# message3.setText('Hit spacebar when you are ready. ')
# message1.draw()
# message2.draw()
# message3.draw()
# win.flip()
# event.waitKeys(keyList = ['space'])

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

path_08_c = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.8\C\selected'
path_08_nc = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.8\NC\selected'
path_08_r = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.8\R\selected'
dirs_08_c = os.listdir(path_08_c)
dirs_08_nc = os.listdir(path_08_nc)
dirs_08_r = os.listdir(path_08_r)

path_07_c = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.7\C\selected'
path_07_nc = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.7\NC\selected'
path_07_r = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.7\R\selected'
dirs_07_c = os.listdir(path_07_c)
dirs_07_nc = os.listdir(path_07_nc)
dirs_07_r = os.listdir(path_07_r)

path_06_c = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.6\C\selected'
path_06_nc = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.6\NC\selected'
path_06_r = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.6\R\selected'
dirs_06_c = os.listdir(path_06_c)
dirs_06_nc = os.listdir(path_06_nc)
dirs_06_r = os.listdir(path_06_r)

path_05_c = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.5\C\selected'
path_05_nc = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.5\NC\selected'
path_05_r = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.5\R\selected'
dirs_05_c = os.listdir(path_05_c)
dirs_05_nc = os.listdir(path_05_nc)
dirs_05_r = os.listdir(path_05_r)


path_04_c = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.4\C\selected'
path_04_nc = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.4\NC\selected'
path_04_r = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.4\NC\selected'
dirs_04_c = os.listdir(path_04_c)
dirs_04_nc = os.listdir(path_04_nc)
dirs_04_r = os.listdir(path_04_r)

path_03_c = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.3\C\selected'
path_03_nc = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.3\NC\selected'
#path_03_r = r'\Users\MiaoLi\Desktop\SCALab\Programming\Crowding_and_numerosity\Stimuli190129\winSize0.3\R\selected'
dirs_03_c = os.listdir(path_03_c)
dirs_03_nc = os.listdir(path_03_nc)
#dirs_03_r = os.listdir(path_03_r)



# winsize0.8 crowding pool 
c_08_60, c_08_61, c_08_62, c_08_63,c_08_64 = ([] for i in range(5))
[c_08_60.append(img) for img in dirs_08_c if img.lower().endswith('60.png')]
[c_08_61.append(img) for img in dirs_08_c if img.lower().endswith('61.png')]
[c_08_62.append(img) for img in dirs_08_c if img.lower().endswith('62.png')]
[c_08_63.append(img) for img in dirs_08_c if img.lower().endswith('63.png')]
[c_08_64.append(img) for img in dirs_08_c if img.lower().endswith('64.png')]

#winsize0.8 nocrowding pool
nc_08_60, nc_08_61, nc_08_62, nc_08_63,nc_08_64 = ([] for i in range(5))
[nc_08_60.append(img) for img in dirs_08_nc if img.lower().endswith('60.png')]
[nc_08_61.append(img) for img in dirs_08_nc if img.lower().endswith('61.png')]
[nc_08_62.append(img) for img in dirs_08_nc if img.lower().endswith('62.png')]
[nc_08_63.append(img) for img in dirs_08_nc if img.lower().endswith('63.png')]
[nc_08_64.append(img) for img in dirs_08_nc if img.lower().endswith('64.png')]

#winsize0.8 ref pool
r_08_60, r_08_61, r_08_62, r_08_63,r_08_64 = ([] for i in range(5))
[r_08_60.append(img) for img in dirs_08_r if img.lower().endswith('60.png')]
[r_08_61.append(img) for img in dirs_08_r if img.lower().endswith('61.png')]
[r_08_62.append(img) for img in dirs_08_r if img.lower().endswith('62.png')]
[r_08_63.append(img) for img in dirs_08_r if img.lower().endswith('63.png')]
[r_08_64.append(img) for img in dirs_08_r if img.lower().endswith('64.png')]


# winsize0.7 crowding pool 
c_07_53, c_07_54, c_07_55, c_07_56,c_07_57 = ([] for i in range(5))
[c_07_53.append(img) for img in dirs_07_c if img.lower().endswith('53.png')]
[c_07_54.append(img) for img in dirs_07_c if img.lower().endswith('54.png')]
[c_07_55.append(img) for img in dirs_07_c if img.lower().endswith('55.png')]
[c_07_56.append(img) for img in dirs_07_c if img.lower().endswith('56.png')]
[c_07_57.append(img) for img in dirs_07_c if img.lower().endswith('57.png')] 

# winsize0.7 nocrowding pool 
nc_07_53, nc_07_54, nc_07_55, nc_07_56,nc_07_57 = ([] for i in range(5)) 
[nc_07_53.append(img) for img in dirs_07_nc if img.lower().endswith('53.png')]
[nc_07_54.append(img) for img in dirs_07_nc if img.lower().endswith('54.png')]
[nc_07_55.append(img) for img in dirs_07_nc if img.lower().endswith('55.png')]
[nc_07_56.append(img) for img in dirs_07_nc if img.lower().endswith('56.png')]
[nc_07_57.append(img) for img in dirs_07_nc if img.lower().endswith('57.png')]

#winsize0.7 ref pool
r_07_53, r_07_54, r_07_55, r_07_56,r_07_57 = ([] for i in range(5))
[r_07_53.append(img) for img in dirs_07_r if img.lower().endswith('53.png')]
[r_07_54.append(img) for img in dirs_07_r if img.lower().endswith('54.png')]
[r_07_55.append(img) for img in dirs_07_r if img.lower().endswith('55.png')]
[r_07_56.append(img) for img in dirs_07_r if img.lower().endswith('56.png')]
[r_07_57.append(img) for img in dirs_07_r if img.lower().endswith('57.png')]

# winsize0.6 crowding pool 
c_06_49, c_06_50, c_06_51, c_06_52,c_06_53 = ([] for i in range(5))
[c_06_49.append(img) for img in dirs_06_c if img.lower().endswith('49.png')]
[c_06_50.append(img) for img in dirs_06_c if img.lower().endswith('50.png')]
[c_06_51.append(img) for img in dirs_06_c if img.lower().endswith('51.png')]
[c_06_52.append(img) for img in dirs_06_c if img.lower().endswith('52.png')]
[c_06_53.append(img) for img in dirs_06_c if img.lower().endswith('53.png')]

# winsize0.6 no_crowding pool 
nc_06_49, nc_06_50, nc_06_51, nc_06_52,nc_06_53 = ([] for i in range(5))
[nc_06_49.append(img) for img in dirs_06_nc if img.lower().endswith('49.png')]
[nc_06_50.append(img) for img in dirs_06_nc if img.lower().endswith('50.png')]
[nc_06_51.append(img) for img in dirs_06_nc if img.lower().endswith('51.png')]
[nc_06_52.append(img) for img in dirs_06_nc if img.lower().endswith('52.png')]
[nc_06_53.append(img) for img in dirs_06_nc if img.lower().endswith('53.png')]

# winsize0.6 ref pool 
r_06_49, r_06_50, r_06_51, r_06_52, r_06_53 = ([] for i in range(5))
[r_06_49.append(img) for img in dirs_06_r if img.lower().endswith('49.png')]
[r_06_50.append(img) for img in dirs_06_r if img.lower().endswith('50.png')]
[r_06_51.append(img) for img in dirs_06_r if img.lower().endswith('51.png')]
[r_06_52.append(img) for img in dirs_06_r if img.lower().endswith('52.png')]
[r_06_53.append(img) for img in dirs_06_r if img.lower().endswith('53.png')]


# winsize0.5 crowding pool 
c_05_41,c_05_42, c_05_43, c_05_44,c_05_45 = ([] for i in range(5))
[c_05_41.append(img) for img in dirs_05_c if img.lower().endswith('41.png')]
[c_05_42.append(img) for img in dirs_05_c if img.lower().endswith('42.png')]
[c_05_43.append(img) for img in dirs_05_c if img.lower().endswith('43.png')]
[c_05_44.append(img) for img in dirs_05_c if img.lower().endswith('44.png')]
[c_05_45.append(img) for img in dirs_05_c if img.lower().endswith('45.png')]

# winsize0.5 nocrowding pool 
nc_05_41,nc_05_42, nc_05_43, nc_05_44,nc_05_45 = ([] for i in range(5))
[nc_05_41.append(img) for img in dirs_05_nc if img.lower().endswith('41.png')]
[nc_05_42.append(img) for img in dirs_05_nc if img.lower().endswith('42.png')]
[nc_05_43.append(img) for img in dirs_05_nc if img.lower().endswith('43.png')]
[nc_05_44.append(img) for img in dirs_05_nc if img.lower().endswith('44.png')]
[nc_05_45.append(img) for img in dirs_05_nc if img.lower().endswith('45.png')]

# winsize0.4 crowding pool 
c_04_31,c_04_32, c_04_33, c_04_34,c_04_35 = ([] for i in range(5))
[c_04_31.append(img) for img in dirs_04_c if img.lower().endswith('31.png')]
[c_04_32.append(img) for img in dirs_04_c if img.lower().endswith('32.png')]
[c_04_33.append(img) for img in dirs_04_c if img.lower().endswith('33.png')]
[c_04_34.append(img) for img in dirs_04_c if img.lower().endswith('34.png')]
[c_04_35.append(img) for img in dirs_04_c if img.lower().endswith('35.png')]

# winsize0.4 nocrowding pool 
nc_04_31,nc_04_32, nc_04_33, nc_04_34,nc_04_35 = ([] for i in range(5))
[nc_04_31.append(img) for img in dirs_04_nc if img.lower().endswith('31.png')]
[nc_04_32.append(img) for img in dirs_04_nc if img.lower().endswith('32.png')]
[nc_04_33.append(img) for img in dirs_04_nc if img.lower().endswith('33.png')]
[nc_04_34.append(img) for img in dirs_04_nc if img.lower().endswith('34.png')]
[nc_04_35.append(img) for img in dirs_04_nc if img.lower().endswith('35.png')]


# winsize0.3 crowding pool 
c_03_21,c_03_22, c_03_23, c_03_24,c_03_25 = ([] for i in range(5))
[c_03_21.append(img) for img in dirs_03_c if img.lower().endswith('21.png')]
[c_03_22.append(img) for img in dirs_03_c if img.lower().endswith('22.png')]
[c_03_23.append(img) for img in dirs_03_c if img.lower().endswith('23.png')]
[c_03_24.append(img) for img in dirs_03_c if img.lower().endswith('24.png')]
[c_03_25.append(img) for img in dirs_03_c if img.lower().endswith('25.png')]

# winsize0.3 nocrowding pool 
nc_03_21,nc_03_22, nc_03_23, nc_03_24,nc_03_25 = ([] for i in range(5))
[nc_03_21.append(img) for img in dirs_03_nc if img.lower().endswith('21.png')]
[nc_03_22.append(img) for img in dirs_03_nc if img.lower().endswith('22.png')]
[nc_03_23.append(img) for img in dirs_03_nc if img.lower().endswith('23.png')]
[nc_03_24.append(img) for img in dirs_03_nc if img.lower().endswith('24.png')]
[nc_03_25.append(img) for img in dirs_03_nc if img.lower().endswith('25.png')]




# # =============================================================================
# # A trial
# # =============================================================================

# fixation = visual.TextStim(win, text= '+', bold = True, color=(-1.0, -1.0, -1.0))
# fixation.setText('+')
# fixation.draw()
# # win.flip()
# # core.wait(2)

# imgstim = visual.ImageStim(win, image = str(path_c)+random.choice(c_60), units = 'pix')
# imgstim.draw()
# win.flip()
# core.wait(0.15)

# #screen for waiting response
# message4 = visual.TextStim(win)
# message4.setText('Please give your best estimation')
# message4.draw()
# win.flip()
# core.wait(2)

# #collecting response and present
# show_resp = visual.TextStim(win)

# keys = event.getKeys(keyList = ['1','2','3','4','5','6','7','8','9','0','return','backspace'])
# key_resp = event.BuilderKeyResponse()

# if 'escape' in keys:
#     endExpNow = True
# else:
#     if len(keys) > 0:
#         #allow backspace for editing
#         if 'backspace' in keys:
#             key_resp.keys = key_resp.keys[:-1]
#         #store pressed numbers
#         key_resp.keys.extend([key for key in keys if key != 'return' and key!= 'backspace'])
#         key_str = ''.join(key_resp.keys)
#         key_num = int(key_str)
#         #present numbers on screen
#         show_resp.setText(key_num)
#         show_resp.draw()
#         win.flip()
#         core.wait(2)
#     else:
#         show_resp.setText('missing response')
#         show_resp.draw()
#         win.flip()
#         core.wait(2)

# # # if 'return' in keys:#FIXME
# # #     show_resp.setText('missing response')
# # #     continueRoutine = False
# # #     show_resp.draw()
# # #     win.flip()
# # #     core.wait(2)


# def singal_trial(data_file):
#     #fixation
    
#     #stimuli
    
#     #response
    
#     pass

# win.close()
# core.quit()













