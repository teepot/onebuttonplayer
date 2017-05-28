#!/usr/bin/python

import datetime
import glob
from gpiozero import LED
from gpiozero import Button
import os
from pygame import mixer
import pyudev
from signal import pause
import threading
import time


# assign gpio number to constant value
RESET_GPIO = 26     # pin 37
CONTROL_GPIO = 2    # pin  3
LED_READY_GPIO = 6  # pin 31
LED_GPIO = 13       # pin 33

IS_PAUSED = False

##DEFAULT_DEVICES = (
##    'RECOVERY',
##    'None',
##    'SETTINGS',
##    'boot',
##    'root',
##    None)


##def reset_mixer():
##    '''Reset the mixer for loading a new mp3'''
##    global IS_PAUSED
##
##    init = mixer.get_init()
##
##    IS_PAUSED = False
##
##    if init:
##        mixer.quit()
##
##    led.off()

def reset_pi():
    '''This will reboot the pi so everything is setup properly '''
    os.system('sudo shutdown -r now')


def get_stick_directory():
    '''Determine the name of the plugged in stick.
    Caution: This may not return the desired stick
    name if more than one stick is plugged into the pi.
    '''
    try:
        dname = [dir for dir in os.listdir('/media/pi') if dir != 'SETTINGS'][0]

    except IndexError:
        return none

    stick_directory = '/media/pi/{}'.format(dname) 
    
    return stick_directory


def get_latest_mp3():
    '''Glob the USB stick directory and determine the most currrent mp3'''
    stick_dir = get_stick_directory()

    #import pdb; pdb.set_trace()
    # loop through the mp3 files on the stick and find the most current file
    mp3_files = []
    for fname in glob.glob(os.path.join(stick_dir,'*.mp3')):
        file_mtime = datetime.datetime.fromtimestamp(os.stat(fname).st_mtime)
        mp3_files.append([file_mtime, fname])
                           
    # sort by date and return the first file which is the most current
    mp3_files.sort()
    # the file name will be the last date-fname list in the list "-1",
    # second element of the date-fname list "1" 
    latest_file = mp3_files[-1][1]

    return latest_file
    

def control_playback():
    '''Called by the control button when it is pressed'''
    global IS_PAUSED

    # check to see if we can get a USB directory
    # if we can't don't return
    if not bool(get_stick_directory()):
        return
    
    # get initialization status of the mixer
    init = bool(mixer.get_init())

    # if the mixer has been initialized, figure out what is going
    # on and perform the appropriate action
    if init:
        # if the mixer is paused then unpause it.
        if IS_PAUSED:
            mixer.music.unpause()
            led.on()
            IS_PAUSED = False

        # if the mixer is streaming music then pause it.
        else:
            mixer.music.pause()
            led.blink()
            IS_PAUSED = True

    # the mixer has not been initialized
    # initialize it, load music and play it
    else:
        init_load_play()

    
def init_load_play():
    mixer.init()
    mixer.music.load(get_latest_mp3())
    mixer.music.play()
    led.on()

    # create the thread that will monitor and quit the mixer when it has
    # completed playback
    t = threading.Thread(target=music_busy_checker)
    t.start()


def music_busy_checker():
    '''This is spun off as a thread and checks the state of the mixer.music'''
    global IS_PAUSED
    time.sleep(20)
    while True:
        try:
            # this will only be False if the mp3 has completed playback
            # it will still register busy if it is paused
            music_busy = bool(mixer.music.get_busy())

        except:
            continue

        if not music_busy:
            led.off()
            IS_PAUSED = False
            mixer.quit()
            break


if __name__ == '__main__':
    # assign gpio pins to components
    reset_button = Button(RESET_GPIO)
    control_button = Button(CONTROL_GPIO)
    led = LED(LED_GPIO)
    ready_led = LED(LED_READY_GPIO)
    ready_led.on()
    
    # assign the when_pressed functions of the buttons to event handlers
    #reset_button.when_pressed = reset_mixer
    reset_button.when_pressed = reset_pi
    control_button.when_pressed = control_playback

    pause()

