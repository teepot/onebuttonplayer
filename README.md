# onebuttonplayer
One button mp3 player.

## Background

There is a lady (client) in our church who has has seeing and mobility challenges. She does not attend church as it is very difficult for her to do so.
A member of the congregation (helper) visits her after church and brings a USB stick with an MP3 of that day's sermon. 
Once the everything is setup and playback is initiated by the helper, the client can pause and unpause playback by pressing the spacebar on the netbook.

The old netbook is used for playback of the MP3 but there are issues:

- the netbook is old and has a limited life expectancy
- the netbook has technical issues from time to time.
- it's a pain for the helper to set up.
- it is small but it still takes up space.
  
We want to replace this system with something that's more reliable and easy to use.

## Requirements

1. Keep the same basic playback control.
2. Have an easy to setup: The helper should be able to remove last week's usb stick, insert the new stick, press a button and playback should start.
3. Provide a simple system reset if there are issues with playback.
4. Provide sufficient visual feedback that both the client and helper can determine that the system is running or paused. 

## Implementation

1. Use a Staples *Easy* button for playback control. The client will press it to start play, pause and unpause play.
someone to help her get things set up. 


## Coding notes

1. Took advantage of the auto login on the RPi. This enabled easy determination of the USB stick's name that is mounted by the system automatically.
Basically you just have to look in the /dev/pi folder to see the name that that system is using.

## Set up

To have the program run automatically add the following line to the `/etc/rc.local`: `/usr/bin/python /home/pi/onebuttonplayer/onebuttonplayer.py`
