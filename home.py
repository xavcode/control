# from tkinter import *
import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
from PIL import Image, ImageTk

def show_home(frame, width, height):

    for widget in frame.winfo_children():
        widget.grid_forget()
    
    def resize_image():
        resized_image = original_image.resize((width, height)) # type: ignore
        new_image = ImageTk.PhotoImage(resized_image)
        label_image.configure(image=new_image)
        label_image.image = new_image # type: ignore
        
    frame_home = ttk.Frame(frame,   )
    frame_home.grid(row=0, column=0, sticky="")
    frame_home.grid_columnconfigure(0, weight=1)
    frame_home.grid_rowconfigure(0, weight=1)

    image_path = "assets/Home1.png"
    original_image = Image.open(image_path)

    canvas = ttk.Canvas(frame_home, width=width, height=height)
    canvas.grid(row=0, column=0,  sticky="nsew")

    label_image = ttk.Label(canvas)
    label_image.grid(row=0, column=0, sticky="nsew")
    
    resize_image()
