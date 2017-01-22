from pygame import mixer
import pyudev
import time



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



def check_usb():
    context = pyudev.Context()


if __name__ == "__main__":
    filename = '/home/pi/Music/whitecoat_20160909_73602.mp3'
    control_playback(filename)
    
