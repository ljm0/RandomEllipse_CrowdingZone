# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 15:16:18 2018

@author: Miao
"""

from psychopy import locale_setup, gui, visual, core, data, event, logging, sound, monitors

#win to show stimuli
win = visual.Window((1024, 786), units='pix', fullscr = True, allowStencil=True)

# fixation 
text_msg = visual.TextStim(win, text='message',color=(-1.0, -1.0, -1.0))
text_msg.setText('+')
text_msg.draw()
#win.flip()
core.wait(0.80)

trgt_disk = visual.Circle(win, radius = 2, lineColor = "black", fillColor = "black")

trgt_disk.setPos((725, 285)) 
trgt_disk.draw()



win.flip()
win.getMovieFrame()
win.saveMovieFrames('random_disks1.png') 
core.wait(0.80)


    
