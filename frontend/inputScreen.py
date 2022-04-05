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
        self._inputFrame = tkinter.Frame(self._root, height=900, width=1600, background='white')
        self._bottleLabelImage = ""
        self._canLabelImage = ""
        self._moneyTotal = 0
        self._bottleVal = 0
        self._bottleCounter = tkinter.Label(self._inputFrame, text="0", background='white', font=("Helvetica", 40))
        self._totalLabel = tkinter.Label(self._inputFrame, text="0.00", background='white', font=("Helvetica", 50))
        self._emptyLabel = tkinter.Label(self._inputFrame, text="Please enter at least 1 container", background='white', font=("Helvetica", 35), fg="red")
        self._notabottleLabel = tkinter.Label(self._inputFrame,
                                        text="Not a valid item, please take it out and enter a valid bottle or can",
                                        font=("Helvetica", 25), fg="red", background='white')
        self._loginFrame = ""
        self._camera = cv2.VideoCapture(1)  # grab the camera
        self._kernel = np.ones((5,5),np.float32)/25

    def layout(self):
        self.loadImages()  # load images in

        # generate all of the items on screen
        counterLabel = tkinter.Label(self._inputFrame, text="Current Total:", background='white',
                                     font=("Helvetica", 45))
        bottleImageLabel = tkinter.Label(self._inputFrame, text="???", image=self._bottleLabelImage, background='white')
        canImageLabel = tkinter.Label(self._inputFrame, text="??????", image=self._canLabelImage, background='white')
        canCounter = tkinter.Label(self._inputFrame, text="0", background='white', font=("Helvetica", 40))
        bufferX = tkinter.Label(self._inputFrame, text="", background='white', padx=200)
        bufferY = tkinter.Label(self._inputFrame, text="", background='white', pady=80)
        addBottle = tkinter.Button(self._inputFrame, text="Check Inserted Item!", padx=50, pady=25,
                                   command=self.addBottles)
        finishButton = tkinter.Button(self._inputFrame, text="Finish Inserting", padx=50, pady=25,
                                      command=self.loginPage)

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
        # here there will be opencv code to run checker
        # image = cv2.imread('assets/bottle04.jpg')  # CHANGE THIS TO TAKING A PICTURE

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
        classes = self._machine.get_classes()

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > 0.85:
                    classIDs.append(classID)

        print(type(classIDs))
        if not classIDs:
            classIDs.append(1)

        print(classIDs)

        mostLikelyItem = classes[classIDs[0]]
        if mostLikelyItem == "bottle":
            print("is bottle")
            self._emptyLabel.place_forget()
            self._notabottleLabel.place_forget()
            self._moneyTotal += 0.25
            self._bottleVal += 1

            self._totalLabel.config(text=self._moneyTotal)
            self._bottleCounter.config(text=self._bottleVal)
        else:
            print("not a bottle")
            self._emptyLabel.place_forget()
            self._notabottleLabel.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER, bordermode='outside')

    def loginPage(self):
        if self._moneyTotal == 0:
            self._emptyLabel.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER, bordermode='outside')
        else:
            self._loginFrame = tkinter.Frame(self._root, height=900, width=1600, background='white')
            self._inputFrame.destroy()

    def getLoginFrame(self):
        return self._loginFrame

    def getmoneyTotal(self):
        return self._moneyTotal
