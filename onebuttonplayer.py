import datetime
import glob
from mpd import (MPDClient, CommandError)
import os
from pygame import mixer
import pyudev


DEFAULT_DEVICES = (
    'RECOVERY',
    'None',
    'SETTINGS',
    'boot',
    'root',
    None)


def get_stick_directory():
    '''Determine the name of the plugged in stick.
    Caution: This may not return the desired stick
    name if more than one stick is plugged into the pi.
    '''
    # get list of devices
    context = pyudev.Context()
    for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
        device_name = device.get('ID_FS_LABEL')
        if device_name not in DEFAULT_DEVICES:
            return '/media/pi/{}'.format(device_name) 

    return None


def get_latest_mp3():

    stick_dir = get_stick_directory()
    # loop through the mp3 files on the stick and find the most current file
    mp3_files = []
    for fname in glob.glob(os.path.join(stick_dir,'*.mp3')):
        file_mtime = datetime.datetime.fromtimestamp(os.stat(fname).st_mtime)
        mp3_file.append([file_mtime, fname])
                           
    latest_file = sorted(mp3_files)[0]

    retrun latest_file
    

def control_playback():
    '''Called by the button when it is pressed'''
    init = mixer.get_init()

    # if the mixer has been initialized figure out what is going
    # on and perform the appropriate action
    if init:
        # if the mixer is streaming music then pause
        if mixer.get_busy():
            mixer.music.pause()

        else:
            mixer.music.unpause()

    # the mixer has not been initialized
    # initialize it, load music and play it
    else:
        init_load_play()
       
    
def init_load_play():
    mixer.init()
    mixer.music.load(get_latest_mp3())
    mixer.music.play()


if __name__ == '__main__':
    print get_stick_directory()
