#Slideshow viewer
##A python-based slideshow viewer using Tkinter

This viewer allows you to run slideshows for multiple directories with support for stopping, starting, saving, and resetting your position.


##Requirements

All you need is python3 and Tkinter installed on your computer.

##Usage:

Run this program from the terminal with `python3 slideshow.py <directory>` for as many directories as you wish.

######Controls:

* Escape to exit program
* Left to go to previous slide. Activates manual mode.
* Right to go to next slide. Activates manual mode.
* S to stop and start the slideshow. When the slideshow starts again it will go back to your saved position.
* V to save your current position.
* N to go to the next slideshow
* P to go to the previous slideshow.

*Note:* When manual mode is set, the program will save the position of the last slide played. When you start the slideshow again, it will go to the last saved position. This also applies if you are going to the next or previous slideshow.

######Command line options:

* -h --help to see the program's help menu
* -t --transition Sets the time spent on each slide in seconds.
* -g --goToNextDir Automatically goes to the next directory/slideshow after the end of the current slideshow is reached
* -s --stopTime The number of seconds until the slideshow stops. Set to 0 if you want an infinite slideshow.

