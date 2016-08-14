from Tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
img = ImageTk.BitmapImage (Image.open("True1.gif"))
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
root.mainloop()