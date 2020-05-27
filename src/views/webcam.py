import tkinter
from tkinter import ttk
import PIL.Image, PIL.ImageTk

class Webcam:

    def __init__(self, window, video_width, video_height, update_callback, delay=15):
        self.window = window
        self.video_width = video_width
        self.video_height = video_height
        self.canvas = None
        self._delay = delay
        self.update_callback = update_callback
        
        self.canvas = tkinter.Canvas(self.window, 
                                    width=self.video_width + 10, 
                                    height=self.video_height + 10)
        self.canvas.grid(row=0, column=3) 
        
        self.update_canvas()


    def update_canvas(self):

        ret, frame = self.update_callback()
        
        if ret:
            color_convert_img = PIL.Image.fromarray(frame)
            self.photo = PIL.ImageTk.PhotoImage(image = color_convert_img)

            self.canvas.create_image(0,
                                     0,
                                     image=self.photo,
                                     anchor = tkinter.NW )
                                     
        self.window.after(self._delay, self.update_canvas)