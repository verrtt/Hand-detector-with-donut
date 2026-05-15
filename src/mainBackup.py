'''
To-do:
    - test
    - debug/look at code snippets again
    - listen for info back from admins on school computers
IMPORTED LIBRARIES: tkinter, cv2, PIL, mediapipe, time
CODE/RESOURCES USED: vin8rai for some function logic, hand landmarker database/algorithm

'''

#tkinter makes windows, PIL converts imgs, cv2 gets webcam, finally tkinter also displays img labels

import time
from tkinter import *
import cv2
from PIL import Image, ImageTk

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


#hand landmarks - google colab hand landmarker
model_path = "D:\detectCube\src\hand_landmarker.task"

#create handlandmarker objects - SETUP
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=2)

detector = vision.HandLandmarker.create_from_options(options)

#check if cv2 is imported (safety line)
print(cv2.__version__)

#open webcam in tkinter window

def close_camera():
    button_widget.config(text="Open camera", state="disabled")

def open_camera(): #function logical flow: vin8rai
    button_widget.configure(text="o(*≧▽≦)ツ┏━┓", command=close_camera)
    mainScreen.geometry("800x650")
    
    ret, frame = vid.read()
    
    if not ret:
        print("error: camera could not be read")

    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_img)

    tk_img = ImageTk.PhotoImage(image = pil_img)
    
    label_widget.photo_image = tk_img
    label_widget.configure(image = tk_img)
    label_widget.img = tk_img
    
    label_widget.after(10, open_camera)


mainScreen = Tk()
mainScreen.geometry("200x200")

vid = cv2.VideoCapture(0) #default webcam, init webcam obj
#set webcam res
vid.set(cv2.CAP_PROP_FRAME_WIDTH,800)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT,600)

label_widget = Label(mainScreen)
button_widget = Button(mainScreen, text = "Open camera", command=open_camera)

label_widget.pack()
button_widget.pack()

mainloop()


'''
HAND DETECTION - https://pyseek.com/2024/09/create-a-finger-counter-using-python-opencv/
'''