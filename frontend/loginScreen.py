import json
import tkinter
from tkinter import ttk
import requests
import time
import main


class loginScreen:
    def __init__(self, machine, root, loginFrame, moneyTotal):
        self._machine = machine
        self._root = root
        self._moneyTotal = moneyTotal
        self._loginFrame = loginFrame
        self._nameInput = tkinter.Entry(self._loginFrame, borderwidth=3, width=25, font=("Helvetica", 30), exportselection=False, )
        self._numberInput = tkinter.Entry(self._loginFrame, borderwidth=3, width=25, font=("Helvetica", 30))
        # self._finalFrame = tkinter.Frame(self._root, height=900, width=1600, background='white')
        self._text = ""

    def layout(self):
        moneyString = "Total is: €" + str(self._moneyTotal)

        totalLabel = tkinter.Label(self._loginFrame, text=moneyString, background='white', font=("Helvetica", 50))
        promptLabel = tkinter.Label(self._loginFrame, text="Please now enter transaction details:", background='white', font=("Helvetica", 50))
        nameLabel = tkinter.Label(self._loginFrame, text="Name: ", background='white', font=("Helvetica", 50))
        numberLabel = tkinter.Label(self._loginFrame, text="Phone number: ", background='white', font=("Helvetica", 50))
        finishButton = tkinter.Button(self._loginFrame, text="Complete transaction!", padx=65, pady=35, command=self.processTransaction, font=("Helvetica", 50))
        bufferY = tkinter.Label(self._loginFrame, text="", background='white', pady=50)

        bufferY.grid(row=0, column=1)
        totalLabel.grid(row=1, column=0, columnspan=3)
        promptLabel.grid(row=2, column=0, columnspan=3, pady=(10, 35))
        nameLabel.grid(row=3, column=0)
        numberLabel.grid(row=4, column=0)
        self._nameInput.grid(row=3, column=2)
        self._numberInput.grid(row=4, column=2)
        finishButton.grid(row=5, column=0, columnspan=3, pady=(50, 0))

        return self._loginFrame

    def processTransaction(self):
        # VALIDATE ENTRIES i.e. if number and string
        # request the api to complete the transaction
        # post @ http://192.168.*:3000/payment, with jwt, username, number and amount
        url = "http://192.168:3000/payment"
        token = "Bearer " + self._machine.get_JWT()
        post_headers = {"Authorization": token, "Content-Type": "application/json"}
        post_content = {
            'username': self._nameInput.get(),
            'number': self._numberInput.get(),
            'amount': self._moneyTotal
        }

        response = requests.post(url, json=post_content, headers=post_headers)

        if response.ok:
            # send to success screen
            print("Worked!!!")

            self._text = response.text
            self._loginFrame.destroy()
        else:
            # add box saying it failed
            print("didn't work :(")

    def getText(self):
        return self._text

    def finalPage(self, text):
        print("in finalframe")

        finalFrame = tkinter.Frame(self._root, height=900, width=1600, background='white')

        completeText = tkinter.Label(finalFrame, text=text, background='white', font=("Helvetica", 50))
        thankyouText = tkinter.Label(finalFrame, text="Thank you for using the service", background='white',
                                     font=("Helvetica", 35))
        completeText.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        thankyouText.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        return finalFrame