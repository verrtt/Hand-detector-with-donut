from tkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk


mainUi = Tk()
mainUi.geometry("800x600")
mainUi.title("mainUi window")
mainUi.configure(background="blue")

def open_window():
    print("another window opened!")
    wind = Toplevel(mainUi)
    wind.title("overlay window")
    wind.geometry("100x100")
    
    x = mainUi.winfo_x() + (mainUi.winfo_width()//2)
    y = mainUi.winfo_y() + (mainUi.winfo_height()//2)
    
    wind.geometry(f"+{x}+{y}")
    
    cat = "  ╱|、\n(˚ˎ 。7\n |、˜〵\n    じしˍ,)ノ"
    
    #canvas = Canvas(mainUi, width=100, height=100)
    #canvas.create_text(50,50, text=cat)
    #canvas.configure(background='magenta')
    #canvas.pack()
    
    Label(wind, text=cat).pack()
    
    wind.configure(background='magenta')
    wind.wm_attributes('-transparentcolor','magenta')
    wind.overrideredirect(True)
    
    
    

Label(mainUi, text="This is the main window").pack()
Button(mainUi,text="Open new window",command = open_window).pack(pady=10)

# Tkinter event loop
mainUi.mainloop()