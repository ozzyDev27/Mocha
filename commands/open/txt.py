from tkinter import *
from math import floor
class window:
    def __init__(self,file):
        self.app=Tk()
        self.app.title(f"{file.name} [{file.ID}]")
        self.app.geometry(f"{floor(self.app.winfo_screenwidth()/2)}x{floor(self.app.winfo_screenheight()/2)}")
        self.text=Text(self.app)
        self.text.pack(fill=BOTH,expand=True)
        self.app.mainloop()
    def data(self):
        return self.text.get("1.0","end-1c")