# GUI for bottle reverse vending machine
import cv2
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import inputScreen
import machine
import numpy as np


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
    inputScreen.layout(inputFrame, root, thisMachine)
    inputFrame.pack()


# fetch this machines JWT
def fetchJWT():
    jwt = "gregregregreig9843g4387gh437gh34g"
    #
    #  HERE FETCH JWT FROM API
    url = "localhost:3000"

    return jwt


# main starter code
if __name__ == '__main__':
    root = tkinter.Tk()

    jwt = fetchJWT()

    thisMachine = machine.Machine(jwt) # create a machine class, this holds JWT and detector model

    s = ttk.Style()
    s.theme_use('winnative')

    startFrame = tkinter.Frame(root, height=900, width=1600, background='white')
    inputFrame = tkinter.Frame(root, height=900, width=1600, background='white')

    firstScreen()

    root.wm_geometry("1600x900")
    root.configure(background="white")
    root.title("Reverse Vending Machine")
    root.mainloop()
