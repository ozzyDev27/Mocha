from tkinter import *
def openTXT(file): #!TODO: everything
    app=Tk()
    app.title=file["name"]
    app.size=(750,500)
    app.minsize=(40,30)
    text=Entry(app)
    app.mainloop()
openTXT({"name":"hello world"})