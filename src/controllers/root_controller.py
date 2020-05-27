import tkinter
from tkinter import ttk 
import logging 
logging.basicConfig(level=logging.INFO)


class RootController:

    def __init__(self, window_title, delay=15, video_source=0):
        self.root = tkinter.Tk()
        self.root.title(window_title)
        logging.info("window created")

    def get_window(self):
        return self.root

    def run(self):
        logging.info("window running")
        self.root.mainloop()



