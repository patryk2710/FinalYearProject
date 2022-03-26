# GUI for bottle reverse vending machine
import cv2
import tkinter
import json
from tkinter import ttk
from PIL import Image, ImageTk
import time
import inputScreen
import loginScreen
import machine
import requests
from requests.auth import HTTPBasicAuth
import numpy as np


# this draws the initial screen for beginning interaction
def firstScreen():
    global startButtonImage
    global startFrame
    startFrame = tkinter.Frame(root, height=900, width=1600, background='white')
    startButtonImage = Image.open('assets/start.png')
    startButtonImage = ImageTk.PhotoImage(startButtonImage)

    startButton = tkinter.Button(startFrame, image=startButtonImage, text="???", command=inputs)
    startButton.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    text = tkinter.Label(startFrame, text="Press Start to begin return process!", background='white',
                         font=("Helvetica", 50))
    text.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

    startFrame.pack()


# send user to screen for inputting bottles and cans - also loop back around
def inputs():
    startFrame.pack_forget()  # hide but not delete first screen
    inputObj = inputScreen.inputScreen(thisMachine, root)  # create object for input page
    frame = inputObj.layout()  # draw input screen
    frame.pack()
    root.wait_window(frame)  # wait until this is deleted

    print(inputObj.getmoneyTotal())
    loginFrame = inputObj.getLoginFrame()
    moneyTotal = inputObj.getmoneyTotal()

    loginObj = loginScreen.loginScreen(thisMachine, root, loginFrame, moneyTotal)  # create object for login page
    frame2 = loginObj.layout()  # draw login page
    frame2.pack()

    root.wait_window(frame2)  # wait until login page is deleted
    text = loginObj.getText()  # get api response
    print(text)
    finalframe = loginObj.finalPage(text)  # call funtion to generate last page
    finalframe.pack()  # draw last page

    # waiting 3000 milliseconds
    var = tkinter.IntVar()
    root.after(3000, var.set, 1)
    print("waiting in finalpage")
    root.wait_variable(var)
    finalframe.destroy()  # delete last page

    startFrame.pack()  # show the first screen back, allowing to restart the cycle


# fetch this machines JWT
def fetchJWT():
    url = "http://192.168.1.84:3000/stations/login"  # url to fetch http://192.168.*:3000/stations/login
    username = "b8cd3d55-c3bc-4f19-b3f9-3d3f92d192d4"  # this machines username
    password = "$2a$12$LQf4l7AItghSghQjZVK6DOuZoW0nFcmYhHLS2gNxz45At4str6KIi"  # this machines password
    response = requests.get(url, auth=HTTPBasicAuth(username, password))  # fetch using HTTPBasicAuth
    asJson = json.loads(response.content)  # parse json string
    jwt = asJson["token"]
    return jwt


def createDNNnetwork():
    net = cv2.dnn.readNetFromDarknet('assets/yolo/yolov3.cfg', 'assets/yolo/yolov3.weights')
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    return net, ln


# main starter code
if __name__ == '__main__':
    global root
    root = tkinter.Tk()
    classes = open('assets/yolo/coco.names').read().strip().split('\n')

    jwt = fetchJWT()

    network = createDNNnetwork()

    thisMachine = machine.Machine(jwt, network[0], network[1], classes)  # create a machine class

    s = ttk.Style()
    s.theme_use('winnative')
    root.wm_geometry("1600x900")
    root.configure(background="white")
    root.title("Reverse Vending Machine")
    firstScreen()

    root.mainloop()
