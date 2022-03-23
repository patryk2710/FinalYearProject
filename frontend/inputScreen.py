import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import loginScreen


class inputScreen:
    def __init__(self, machine, root):
        self.loadImages()
        self._machine = machine
        self._root = root
        self._inputFrame = tkinter.Frame(self._root, height=900, width=1600, background='white')
        self._bottleLabelImage = ""
        self._canLabelImage = ""
        self._moneyTotal = 0
        self._bottleVal = 0
        self._bottleCounter = tkinter.Label(self._inputFrame, text="0", background='white', font=("Helvetica", 40))
        self._totalLabel = tkinter.Label(self._inputFrame, text="0.00", background='white', font=("Helvetica", 50))
        self._loginFrame = ""

    def layout(self):
        self.loadImages()  # load images in

        # generate all of the items on screen
        counterLabel = tkinter.Label(self._inputFrame, text="Current Total:", background='white',
                                     font=("Helvetica", 45))
        bottleImageLabel = tkinter.Label(self._inputFrame, text="???", image=self._bottleLabelImage, background='white')
        canImageLabel = tkinter.Label(self._inputFrame, text="??????", image=self._canLabelImage, background='white')
        canCounter = tkinter.Label(self._inputFrame, text="0", background='white', font=("Helvetica", 40))
        bufferX = tkinter.Label(self._inputFrame, text=" ", background='white', padx=200)
        bufferY = tkinter.Label(self._inputFrame, text=" ", background='white', pady=80)
        addBottle = tkinter.Button(self._inputFrame, text="Check Inserted Item!", padx=50, pady=25, command=self.addBottles)
        finishButton = tkinter.Button(self._inputFrame, text="Finish Inserting", padx=50, pady=25, command=self.loginPage)

        # draw the items on a grid
        bufferY.grid(row=0, column=1)
        bottleImageLabel.grid(row=1, column=0)
        canImageLabel.grid(row=1, column=1)
        canCounter.grid(row=2, column=1)
        bufferX.grid(row=2, column=2)
        self._bottleCounter.grid(row=2, column=0)
        counterLabel.grid(row=1, column=3)
        self._totalLabel.grid(row=2, column=3)
        addBottle.grid(row=3, column=2, pady=(0, 30))
        finishButton.grid(row=4, column=2)

        return self._inputFrame

    def loadImages(self):
        self._bottleLabelImage = Image.open('assets/bottle.png')
        self._bottleLabelImage = ImageTk.PhotoImage(self._bottleLabelImage)
        self._canLabelImage = Image.open('assets/can.png')
        self._canLabelImage = ImageTk.PhotoImage(self._canLabelImage)

    def addBottles(self):
        # here there will be opencv code to run checker

        self._bottleVal += 1
        self._moneyTotal += 0.25

        self._totalLabel.config(text=self._moneyTotal)
        self._bottleCounter.config(text=self._bottleVal)

    def loginPage(self):
        self._loginFrame = tkinter.Frame(self._root, height=900, width=1600, background='white')
        self._inputFrame.destroy()

    def getLoginFrame(self):
        return self._loginFrame

    def getmoneyTotal(self):
        return self._moneyTotal
