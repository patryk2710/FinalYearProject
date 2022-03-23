# GUI for bottle reverse vending machine
import cv2
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import inputScreen
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as image


# this draws the initial screen for beginning interaction
def firstScreen():
    global startButtonImage
    startButtonImage = Image.open('assets/start.png')
    startButtonImage = ImageTk.PhotoImage(startButtonImage)

    startButton = tkinter.Button(startFrame, image= startButtonImage, text="???", command=inputs)
    startButton.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    text = tkinter.Label(startFrame, text="Press Start to begin return process!", background='white', font=("Helvetica", 50))
    text.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

    startFrame.pack()


# send user to screen for inputting bottles and cans
def inputs():
    startFrame.destroy()
    inputScreen.layout(inputFrame, root)
    inputFrame.pack()


# main starter code
if __name__ == '__main__':
    root = tkinter.Tk()

    s = ttk.Style()
    s.theme_use('winnative')

    startFrame = tkinter.Frame(root, height=900, width=1600, background='white')
    inputFrame = tkinter.Frame(root, height=900, width=1600, background='white')

    firstScreen()

    root.wm_geometry("1600x900")
    root.configure(background="white")
    root.title("Reverse Vending Machine")
    root.mainloop()
