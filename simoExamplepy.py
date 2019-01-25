# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 22:36:39 2019
PsychopySample_SimonEffect

@author: MiaoLi
"""
import sys, random, os, time
from psychopy import visual, core, event


def sendCode(code): pass

#get subject info
def get_subj_info():
    subj_id = input('Subject ID: ')
    subj_name = input('Subject Name: ')
    subj_sex = input('Subject Sex (m/f): ')
    subj_age = input('Subject Age: ')
    subj_handedness = input('right/left： ')
    return [subj_id, subj_name, subj_sex, subj_age, subj_handedness]
subj = get_subj_info()

#window
win = visual.Window((1024, 768), units ='pix', fullscr = False)

#some conditions
left = (-200, 0)
right = (200, 0)
red = (1.0, -1.0, -1.0)
blue = (-1.0, -1.0, 1.0)
black = (-1.0, -1.0, -1.0)
white = (1.0, 1.0, 1.0)

random.seed = 1000

#trail list
trials =[['L', 'R', 'z', 1],
         ['L', 'B', '/', 2],
         ['R', 'R', 'z', 3],
         ['R', 'B', '/', 4]]

text_msg = visual.TextStim(win, text ='message')
tar_stim =visual.GratingStim(win, tex = 'None', mask = 'circle', size = 60.0)

#run single trial
def run_trial(pars, data_file, subj_info):
    l, c, cor_resp, trig = pars
    if l == 'R': loc = right
    if l == 'L': loc = left
    if c == 'R': col = red
    if c == 'B': col = blue
    
    #present the fixation
    text_msg.setText('+')
    text_msg.draw()
    win.flip()
    core.wait(0.75)
    
    #present the target
    tar_stim.setColor(col)
    tar_stim.setPos(loc)
    tar_stim.draw()
    win.flip()
    sendCode(trig) #不需要
    tar_resp =event.waitKeys(1500, ['z','slash'],timeStamped = True)

    print (tar_resp) 
    
    #Write data to file
    trial_data = subj_info +pars + list(tar_resp[0])
    trial_data = map(str, trial_data)
    trial_data = ','.join(trial_data) + '\n'
    data_file.write(trial_data)
    
    win.setColor(black)
    win.flip()
    core.wait(0.5)

#real experiment starts here
#open a data file
if not os.path.exists('data_file'):
    os.mkdir('data_file')
d_file = open('data_file/'+'_'.join(subj[:2])+ '.csv', 'w')

#show the instructions
text_msg.setText('press z to red...')
text_msg.draw()
win.flip()
event.waitKeys(2, keyList =['space'])

test_trials = trials[:]*2
random.shuffle(test_trials)

for t in test_trials:
    run_trial(t, d_file, subj)
    
d_file.close()

sys.exit()














