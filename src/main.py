'''
LIBRARIES: tkinter, cv2, PIL, mediapipe, time
RESOURCES USED: vin8rai, hand landmarker database/algorithm, @Denbergvanthijs on Github for donut
'''

#tkinter makes windows, PIL converts imgs, cv2 gets webcam, finally tkinter also displays img labels

import time
from tkinter import *
import cv2
from PIL import Image, ImageTk
import ctypes
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#hand landmarks - google colab hand landmarker
model_path = r"D:\usbD backup\detectCube\src\hand_landmarker.task" #WARNING: this file is local, and won't work on your device. instead, go to the official downloader for hand landmarker, and scroll down past the demonstration to find the .task file.


#create handlandmarker objects - SETUP
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(base_options=base_options,num_hands=2)

mp_hands = mp.tasks.vision.HandLandmarksConnections
mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles

#define landmark specifics
FONT_SIZE = 1
HANDEDNESS_TEXT_COLOR = (88,205,54) #green, change later
FONT_THICKNESS = 1


detector = vision.HandLandmarker.create_from_options(options)

#donut
screen_size = 40
theta_spacing = 0.07
phi_spacing = 0.02
illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

AT = False #true if fingers are touching
A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))

#check if cv2 is imported (safety line)
print(cv2.__version__)

#@Denbergvanthijs on Github
def render_frame(A: float, B: float) -> np.ndarray:
    """
    Returns a frame of the spinning 3D donut.
    Based on the pseudocode from: https://www.a1k0n.net/2011/07/20/donut-math.html
    """
    cos_A = np.cos(A)
    sin_A = np.sin(A)
    cos_B = np.cos(B)
    sin_B = np.sin(B)

    output = np.full((screen_size, screen_size), " ")  # (40, 40)
    zbuffer = np.zeros((screen_size, screen_size))  # (40, 40)

    cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, phi_spacing))  # (315,)
    sin_phi = np.sin(phi)  # (315,)
    cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, theta_spacing))  # (90,)
    sin_theta = np.sin(theta)  # (90,)
    circle_x = R2 + R1 * cos_theta  # (90,)
    circle_y = R1 * sin_theta  # (90,)

    x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T  # (90, 315)
    y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T  # (90, 315)
    z = ((K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T  # (90, 315)
    ooz = np.reciprocal(z)  # Calculates 1/z
    xp = (screen_size / 2 + K1 * ooz * x).astype(int)  # (90, 315)
    yp = (screen_size / 2 - K1 * ooz * y).astype(int)  # (90, 315)
    L1 = (((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi, cos_theta)) - sin_A * sin_theta)  # (315, 90)
    L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A))  # (315, 90)
    L = np.around(((L1 + L2) * 8)).astype(int).T  # (90, 315)
    mask_L = L >= 0  # (90, 315)
    chars = illumination[L]  # (90, 315)

    for i in range(90):
        mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])  # (315,)

        zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
        output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

    return output

#landmark visualization: official mediapipe hand landmarker setup
def draw_landmarks_on_image(rgb_image, detection_result):
    global AT
    VisionRunningMode  = mp.tasks.vision.RunningMode
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)
    
    #update label position
    if detection_result.hand_landmarks:
        labelx = int(hand_landmarks_list[0][8].x * 800) + 900
        labely = int(hand_landmarks_list[0][8].y * 650) + 320
        wind.geometry(f"+{labelx}+{labely}")
        if abs(hand_landmarks_list[0][8].x - hand_landmarks_list[0][4].x) < .05 and abs(hand_landmarks_list[0][8].y - hand_landmarks_list[0][4].y) < 0.05:
            AT = True
        else:
            AT = False
    
    #loop through detected hands
    for index in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[index]
        handedness = handedness_list[index]
        
        #actual drawing
        mp_drawing.draw_landmarks(annotated_image,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
        #top left corner of bounding box
        height, width, _ = annotated_image.shape
        x_coords = [landmark.x for landmark in hand_landmarks]
        y_coords = [landmark.y for landmark in hand_landmarks]
        text_x = int(min(x_coords) * width)
        text_y = int(min(y_coords) * height)
        
        #draw handedness
        cv2.putText(annotated_image, f"{handedness[0].category_name}",
                    (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX, FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)
    return annotated_image

#shows the donut
def show_donut():
    print("cop trap \"set\"")
    wind.attributes("-alpha", 1)
    
    #button_widget.config(text="Open camera", state="disabled")

def open_camera(): #function logical flow: vin8rai
    global A , B
    button_widget.configure(text="o(*≧▽≦)ツ┏━┓", command=show_donut)
    mainScreen.geometry("800x650")
    
    ret, frame = vid.read()
    
    if not ret:
        print("error: camera could not be read")
        return

    opencv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    #visualize hand landmarks
    
    #directly convert opencv numpy arr to a mp.Image
    hlimage = mp.Image(image_format=mp.ImageFormat.SRGB, data=opencv_img)
    detection_result = detector.detect(hlimage)#use the mp.Image in detection of landmarks
    
    annotated_image = draw_landmarks_on_image(hlimage.numpy_view(), detection_result)
    
    #convert for tkinter display
    final_img = Image.fromarray(annotated_image)
    photo_image = ImageTk.PhotoImage(image=final_img)

    label_widget.photo_image = photo_image
    label_widget.configure(image = photo_image)
    
    #donut
    if not AT: #if fingers are apart
        A+=theta_spacing #increment the A/B values
        B+=phi_spacing
        
        donut_frame = render_frame(A,B) #returns string
        txt = "\n".join([" ".join(row) for row in donut_frame]) #formats to join the elements of the list, adds a space in between characters.
        l.configure(text=txt, foreground='black') # sets the text color to white (counterintuitive I know)
    else:
        l.configure(foreground='magenta') # sets the text color to magenta
    for i in range(1):
        break
    wind.attributes('-topmost' , True)
    #update loop
    label_widget.after(10, open_camera)


mainScreen = Tk()
mainScreen.geometry("200x200+1000+320")

vid = cv2.VideoCapture(0) #default webcam, init webcam obj
#set webcam res
vid.set(cv2.CAP_PROP_FRAME_WIDTH,800)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT,600)



print("another window opened!")
wind = Toplevel(mainScreen)
wind.title("overlay window")
wind.geometry("200x250+1000+320")

x = mainScreen.winfo_x() + (mainScreen.winfo_width()//2)
y = mainScreen.winfo_y() + (mainScreen.winfo_height()//2)

wind.geometry(f"+{x}+{y}")

cat = "  ╱|、\n(˚ˎ 。7\n |、˜〵\n    じしˍ,)ノ"

#canvas = Canvas(mainUi, width=100, height=100)
#canvas.create_text(50,50, text=cat)
#canvas.configure(background='magenta')
#canvas.pack()

l = Label(wind, text=cat, background='white', foreground='black', font=('Courier New', 3, 'bold'))
l.pack()
#configure the colors of the donut, make the bg transparent etc
wind.configure(background='white')
wind.wm_attributes('-transparentcolor','white')
wind.overrideredirect(True)
wind.attributes('-alpha', 0)


label_widget = Label(mainScreen)
button_widget = Button(mainScreen, text = "Open camera", command=open_camera)

label_widget.pack()
button_widget.pack()
#loops on itself
mainloop()