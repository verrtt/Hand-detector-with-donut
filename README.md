# Hand-detector-with-donut
APCSP final project: a python-based hand detector with a spinning donut graphic. This project opens a window where it'll detect your hand landmarks and assign a donut to your pointer finger, which you can then manipulate freely by pinching your fingers together and moving your pointer finger around. Fun and not complicated (other than the donut).

# How to run on your own device:
- Download all files in src
- Install PIP libraries: tkinter, pillow, mediapipe
- in 'src\main.py,' go to line 20 and change PATH to the path that handlandmarker.task is in
### and you're done!

## if you want to do more..
- to reconfigure where the window shows up, change the last two numbers on line 199
- to reconfigure where the donut shows up, change the last '+ xxx' numbers to what you want.
- to make the donut stay in one specific x/y value and not be effected by hand movements, change line 109 based on the tkinter geometry values (and remove the variables)
