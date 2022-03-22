# GUI for bottle reverse vending machine
import cv2
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import inputScreen
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as image


def firstScreen():
    startButton = tkinter.Button(startFrame, image= startButtonImage, text="???", command=inputs)
    startButton.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    text = tkinter.Label(startFrame, text="Press Start to begin return process!", background='white', font=("Helvetica", 50))
    text.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

    startFrame.pack()


def inputs():
    startFrame.pack_forget()
    inputScreen.layout(inputFrame)
    inputFrame.pack()


def readImages():
    global startButtonImage
    global bottleImage
    global canImage
    global finishImage

    startButtonImage = Image.open('assets/start.png')
    startButtonImage = ImageTk.PhotoImage(startButtonImage)


if __name__ == '__main__':
    root = tkinter.Tk()
    readImages()

    s = ttk.Style()
    s.theme_use('winnative')

    startFrame = tkinter.Frame(root, height=900, width=1600, background='white')
    inputFrame = tkinter.Frame(root)

    firstScreen()

    root.wm_geometry("1600x900")
    root.configure(background="white")
    root.title("Gaming???")
    root.mainloop()
