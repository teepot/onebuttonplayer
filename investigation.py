import os
from pygame import mixer
import pygame
import pyudev
import time
import threading

# You can have several User Events, so make a separate Id for each one
END_MUSIC_EVENT = pygame.USEREVENT + 1    # ID for music Event
DEFAULT_DEVICES = (
    'RECOVERY',
    'None',
    'SETTINGS',
    'boot',
    'root',
    None)

def control_playback(filename):
    # this returns None since it hasn't been initialized
    #mixer.get_init()
    
    # initialize the mixer
    mixer.init()
    # this returns a tuple of metadata about the mixer
    mixer.get_init()
    # load the mp3
    mixer.music.load(filename)

    # play the mp3 for 10 seconds
    mixer.music.play()
    time.sleep(10)

    # pause the mp3 for 3 seconds
    mixer.music.pause()
    time.sleep(3)

    # unpause to restart and continue play for 10 seconds
    mixer.music.unpause()
    time.sleep(10)

    # stop, which will put us back to the beginning
    # and cease play
    mixer.music.stop()

    time.sleep(1) # wait a second before starting

    # we will start at the beginning because we had stopped
    # play for 10 seconds
    mixer.music.play()
    time.sleep(10)

    # check to see if the music is streaming
    # returns 1 if busy. This will be 1 if paused
    # it will return 0 if the music is stopped
    #mixer.music.get_busy()

    # quit the mixer, it is now uninitialized
    mixer.quit()


def control_playback2(filename):
    mixer.init()
##    pygame.init()

    # load the mp3
    mixer.music.load(filename)

    # play the mp3 
    mixer.music.play()


def reset_mixer():
    mixer.quit()


def py_game_event_checker():
    time.sleep(0.1)
    while True:
        events = pygame.event.get()
        if events:
            for event in events:
                if event.type == END_MUSIC_EVENT and event.code == 0:
                    mixer.quit()
                    break

def music_busy_checker():
    time.sleep(1)
    while True:
        if not mixer.music.get_busy():
            mixer.quit()
            break

def mount_usb():
    context = pyudev.Context()

    usb_devices = [
        device.device_node for device in context.list_devices(
            subsystem='block', DEVTYPE='partition')]
        #if device.device_node.startswith('/dev/sd')]

    print '\nThe device found are'
    for dev in usb_devices:
        print dev

    # grab the last one listed
    #usb_device = usb_devices[-1]

    mount_point = '/media/usb_stick'

##    os.system('sudo mount {} {}'.format(usb_device, mount_point))
              
    #return mount_point


def get_stick_directory1():
    '''Determine the name of the plugged in stick.
    Caution: This may not return the desired stick
    name if more than one stick is plugged into the pi.
    '''
    dname = None
    
    # get list of devices
    context = pyudev.Context()
    for device in context.list_devices(
        subsystem='block', DEVTYPE='partition'):
            device_name = device.get('ID_FS_LABEL')
            print device_name
            if device_name not in DEFAULT_DEVICES:
                dname = device_name
                break

    if not dname:
        dname = [dir for dir in os.listdir('/media/pi') if dir != 'SETTINGS'][0]

    stick_directory = '/media/pi/{}'.format(dname)

    return stick_directory

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

   
if __name__ == "__main__":
    dir = get_stick_directory()
    print dir
##    #pygame.mixer.music.set_endevent(END_MUSIC_EVENT)
##    #t = threading.Thread(target=py_game_event_checker)
##    control_playback2('/home/pi/Music/piano2-CoolEdit.mp3')
##    t = threading.Thread(target=music_busy_checker)
##    t.start()
##
##        
##    time.sleep(20)
##    #pygame.mixer.music.set_endevent()
    
