##### Intro Stroop Task #####
'''
task description: red, green, blue, congruent, incongruent
'''
# import modules
from psychopy import data, event, visual, core
import os
import csv
import random

# set our relative path
pwd = os.getcwd()

# timing parameters
display_time = 3
feedback_time = .5
fix_time = 1

timer = core.Clock()
globalClock = core.Clock()

# response parameters
resp = ['1', '2']

# color parameters
# window setup
win = visual.Window([800,600], monitor="testMonitor", units="deg", fullscr=False,
    allowGUI=False, screen=0) #set screen to 1 for dual monitor

#colors
colors = ['red', 'green', 'blue']

# visual stim setup
word = visual.TextStim(win, height=1, alignHoriz='center', alignVert='center')
fixation = visual.TextStim(win, text="+", height=2)

# setting up the trial handler
trial_data = [r for r in csv.DictReader(open('%s/misc/PsychoPy_Intro-stim.csv' % pwd, 'rU'))]
print(trial_data)
trials = data.TrialHandler(trial_data, nReps=3, method="random") # we want 12 trials, so we'll repeat the process twice
# let's loop through the task!

# this will be the FIRST AND ONLY TIME YOU RESET THE GLOBAL CLOCK
globalClock.reset()

# create a task start variable so we can calculate RT
task_onset = globalClock.getTime()

for trial in trials:
    # let's clear any events that were stored from the previous trial
    event.clearEvents()
    
    # first we need to set the text!
    word.setText(trial['color'])
    
    # now we'll set the color 
    if trial['congruent'] == 'Y':
        color = trial['color']
        word.setColor(color)
    else:
        # let's randomly select an 'incongruent' color
        random.shuffle(colors)
        
        # if they shuffle accidentally matches, we'll take the next one
        if colors[0] == trial['color']:
            color = colors[1]
        else:
            color = colors[0]
            
        word.setColor(color)
    
    # let's record in our data what 'color' was selected
    trials.addData('text_color', color)
    
    # let's show people some data and wait for their response!
    
    # always be sure to reset your timer!
    
    while timer.getTime() < display_time:
        word.draw()
        win.flip()
        response = event.getKeys(keyList = resp, timeStamped = globalClock)
        
        # if there's a response, let's keep the screen online for .5 more seconds
        if len(response) > 0: 
            resp_val = int(response[0][0])
            rt_onset = response[0][1]
            
            core.wait(feedback_time)
            break
        
        else: #if the subject doesn't respond
            resp_val = 'NA'
            rt_onset = 'NA'
            
    
    # now let's add record the data we collected
    trials.addData('resp', resp_val)
    trials.addData('rt', rt_onset)
    
    # let's display a fixation between trials
    
    # first we have to reset the clock
    timer.reset()
    
    while timer.getTime() < fix_time:
        fixation.draw()
        win.flip()

# let's save out the data
trials.saveAsWideText('%s/misc/task_data.csv' % pwd, delim = ',', appendFile=True)
