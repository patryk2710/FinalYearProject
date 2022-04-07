import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import loginScreen
import cv2
import numpy as np


class inputScreen:
    def __init__(self, machine, root):
        self.loadImages()
        self._machine = machine
        self._root = root
        self._inputFrame = tkinter.Frame(self._root, height=900, width=1600, background='lightgrey')
        self._bottleLabelImage = ""
        self._canLabelImage = ""
        self._moneyTotal = 0
        self._bottleVal = 0
        self._bottleCounter = tkinter.Label(self._inputFrame, text="0", background='lightgrey', font=("Calibri", 40))
        self._totalLabel = tkinter.Label(self._inputFrame, text="0.00", background='lightgrey', font=("Calibri", 50))
        self._whatWasInserted = tkinter.Label(self._inputFrame, text="", background='lightgrey', font=("Calibri", 25))
        self._emptyLabel = tkinter.Label(self._inputFrame, text="Please enter at least 1 container", background='lightgrey', font=("Helvetica", 35), fg="red")
        self._notabottleLabel = tkinter.Label(self._inputFrame,
                                        text="Not a valid item, please input a valid bottle or move it slightly and try again",
                                        font=("Calibri", 25), fg="red", background='lightgrey')
        self._loginFrame = ""
        self._camera = cv2.VideoCapture(1)  # grab the camera
        self._kernel = np.ones((5,5),np.float32)/25

    def layout(self):
        self.loadImages()  # load images in

        # generate all of the items on screen
        counterLabel = tkinter.Label(self._inputFrame, text="Current Total:", background='lightgrey',
                                     font=("Calibri", 45))
        bottleImageLabel = tkinter.Label(self._inputFrame, text="???", image=self._bottleLabelImage, background='lightgrey')
        canImageLabel = tkinter.Label(self._inputFrame, text="??????", image=self._canLabelImage, background='lightgrey')
        canCounter = tkinter.Label(self._inputFrame, text="0", background='lightgrey', font=("Calibri", 40))
        bufferX = tkinter.Label(self._inputFrame, text="", background='lightgrey', padx=200)
        bufferY = tkinter.Label(self._inputFrame, text="", background='lightgrey', pady=40)
        addBottle = tkinter.Button(self._inputFrame, text="Check Inserted Item!", padx=50, pady=15,
                                   command=self.addBottles, font=("Calibri, 35"))
        finishButton = tkinter.Button(self._inputFrame, text="Finish Inserting", padx=50, pady=15,
                                      command=self.loginPage, font=("Calibri, 35"))

        # draw the items on a grid
        bufferY.grid(row=0, column=0)
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
        # here there is opencv code to run bottle checker

        # works with bottle
        (check, image) = self._camera.read()

        # rotate image for recognition - 90 deg clockwise + add filter
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image = cv2.filter2D(src=image, ddepth=-1, kernel=self._kernel)  # averaging

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net = self._machine.get_net()
        ln = self._machine.get_layerNames()

        net.setInput(blob)
        layerOutputs = net.forward(ln)

        classIDs = []
        confScores = []
        heights = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > 0.7:
                    if classID == 39:
                        classIDs.append(classID)
                        confScores.append(confidence)
                        thisBox = detection[0:4] * np.array([480, 640, 480, 640])
                        height = thisBox[3].astype("int")
                        heights.append(height)

        if not classIDs:
            classIDs.append(1)
            confScores.append(0.9999)
            heights.append(500)

        # here have to only get the largest in the
        highestConfIndex = np.argmax(confScores)
        mostLikelyItem = classIDs[highestConfIndex]
        mostLikelyHeight = heights[highestConfIndex]
        self._emptyLabel.place_forget()
        if mostLikelyItem == 39:
            self._notabottleLabel.place_forget()
            # here check length of bottle to determine size (small bottles are around 270-300)
            print(mostLikelyHeight)
            if mostLikelyHeight < 310:
                print("small bottle")
                item = "Small Bottle worth 25c"
                self._moneyTotal += 0.25
            else:
                print("large bottle")
                item = "Large Bottle worth 50c"
                self._moneyTotal += 0.50

            self._bottleVal += 1
            inserted = "You inserted: " + item
            self._whatWasInserted.place_forget()
            self._whatWasInserted.config(text=inserted)
            self._whatWasInserted.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER, bordermode='outside')
            self._totalLabel.config(text=self._moneyTotal)
            self._bottleCounter.config(text=self._bottleVal)
        else:
            print("not a bottle")
            self._notabottleLabel.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER, bordermode='outside')

    def loginPage(self):
        if self._moneyTotal == 0:
            self._emptyLabel.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER, bordermode='outside')
        else:
            self._loginFrame = tkinter.Frame(self._root, height=900, width=1600, background='lightgrey')
            self._inputFrame.destroy()

    def getLoginFrame(self):
        return self._loginFrame

    def getmoneyTotal(self):
        return self._moneyTotal
