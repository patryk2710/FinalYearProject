# GUI for bottle reverse vending machine
import cv2
import tkinter
import json
from tkinter import ttk
from PIL import Image, ImageTk
import inputScreen
import machine
import requests
from requests.auth import HTTPBasicAuth
import numpy as np


# this draws the initial screen for beginning interaction
def firstScreen():
    global startButtonImage
    startButtonImage = Image.open('assets/start.png')
    startButtonImage = ImageTk.PhotoImage(startButtonImage)

    startButton = tkinter.Button(startFrame, image=startButtonImage, text="???", command=inputs)
    startButton.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    text = tkinter.Label(startFrame, text="Press Start to begin return process!", background='white',
                         font=("Helvetica", 50))
    text.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

    startFrame.pack()


# send user to screen for inputting bottles and cans
def inputs():
    startFrame.destroy()
    inputScreen.layout(inputFrame, root, thisMachine)
    inputFrame.pack()


# fetch this machines JWT
def fetchJWT():
    url = ""  # url to fetch
    username = "b8cd3d55-c3bc-4f19-b3f9-3d3f92d192d4"  # this machines username
    password = "$2a$12$LQf4l7AItghSghQjZVK6DOuZoW0nFcmYhHLS2gNxz45At4str6KIi"  # this machines password
    response = requests.get(url, auth=HTTPBasicAuth(username, password))  # fetch using HTTPBasicAuth
    asJson = json.loads(response.content)  # parse json string
    jwt = asJson["token"]
    return jwt


# main starter code
if __name__ == '__main__':
    root = tkinter.Tk()

    jwt = fetchJWT()

    thisMachine = machine.Machine(jwt)  # create a machine class, this holds JWT and detector model

    s = ttk.Style()
    s.theme_use('winnative')

    startFrame = tkinter.Frame(root, height=900, width=1600, background='white')
    inputFrame = tkinter.Frame(root, height=900, width=1600, background='white')

    firstScreen()

    root.wm_geometry("1600x900")
    root.configure(background="white")
    root.title("Reverse Vending Machine")
    root.mainloop()
