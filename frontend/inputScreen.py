import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import loginScreen

moneyTotal = 0
bottleVal = 0
global totalLabel


# function for loading in external images
def loadImages():
    global bottleLabelImage
    global canLabelImage

    bottleLabelImage = Image.open('assets/bottle.png')
    bottleLabelImage = ImageTk.PhotoImage(bottleLabelImage)
    canLabelImage = Image.open('assets/can.png')
    canLabelImage = ImageTk.PhotoImage(canLabelImage)


# add a bottle to the counter
def addBottles():
    global moneyTotal
    global bottleCounter
    global totalLabel
    global bottleVal

    # here there will be opencv code to run checker

    bottleVal += 1
    moneyTotal += 0.25

    totalLabel.config(text=moneyTotal)
    bottleCounter.config(text=bottleVal)


# user clicked finish, send to login page - pass amount of money as argument
def loginPage():
    loginFrame = tkinter.Frame(rootFrame, height=900, width=1600, background='white')
    thisFrame.destroy()
    loginScreen.layout(loginFrame, moneyTotal)
    loginFrame.pack()


# this function loads the layout for the frame
def layout(inputFrame, root):
    loadImages() # load images in

    # global variables, for being visible to other functions
    global thisFrame
    global rootFrame
    rootFrame = root
    thisFrame = inputFrame
    global totalLabel
    global bottleCounter

    # generate all of the items on screen
    counterLabel = tkinter.Label(inputFrame, text="Current Total:", background='white', font=("Helvetica", 45))
    totalLabel = tkinter.Label(inputFrame, text="0.00", background='white', font=("Helvetica", 50))
    bottleImageLabel = tkinter.Label(inputFrame, text="???", image=bottleLabelImage, background='white')
    canImageLabel = tkinter.Label(inputFrame, text="??????", image=canLabelImage, background='white')
    canCounter = tkinter.Label(inputFrame, text="0", background='white', font=("Helvetica", 40))
    bottleCounter = tkinter.Label(inputFrame, text="0", background='white', font=("Helvetica", 40))
    bufferX = tkinter.Label(inputFrame, text=" ", background='white', padx=200)
    bufferY = tkinter.Label(inputFrame, text=" ", background='white', pady=80)
    addBottle = tkinter.Button(inputFrame, text="Check Inserted Item!", padx=50, pady=25, command=addBottles)
    finishButton = tkinter.Button(inputFrame, text="Finish Inserting", padx=50, pady=25, command=loginPage)

    # draw the items on a grid
    bufferY.grid(row=0, column=1)
    bottleImageLabel.grid(row=1, column=0)
    canImageLabel.grid(row=1, column=1)
    canCounter.grid(row=2, column=1)
    bufferX.grid(row=2, column=2)
    bottleCounter.grid(row=2, column=0)
    counterLabel.grid(row=1, column=3)
    totalLabel.grid(row=2, column=3)
    addBottle.grid(row=3, column=2, pady=(0, 30))
    finishButton.grid(row=4, column=2)
