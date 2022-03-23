import tkinter
from tkinter import ttk


def processTransaction():
    # VALIDATE ENTRIES i.e. if number and string
    print(totalMoney)
    print(nameInput.get())
    print(numberInput.get())
    print(myMachine.get_JWT())


def layout(inputFrame, moneyTotal, thisMachine):
    global totalMoney
    global nameInput
    global numberInput
    global myMachine

    myMachine = thisMachine
    totalMoney = moneyTotal
    moneyString = "Total is: €" + str(moneyTotal)

    totalLabel = tkinter.Label(inputFrame, text=moneyString, background='white', font=("Helvetica", 50))
    promptLabel = tkinter.Label(inputFrame, text="Please now enter transaction details:", background='white', font=("Helvetica", 50))
    nameLabel = tkinter.Label(inputFrame, text="Name: ", background='white', font=("Helvetica", 50))
    numberLabel = tkinter.Label(inputFrame, text="Phone number: ", background='white', font=("Helvetica", 50))
    nameInput = tkinter.Entry(inputFrame, borderwidth=3, width=25, font=("Helvetica", 30), exportselection=False, )
    numberInput = tkinter.Entry(inputFrame, borderwidth=3, width=25, font=("Helvetica", 30))
    finishButton = tkinter.Button(inputFrame, text="Complete transaction!", padx=65, pady=35, command=processTransaction, font=("Helvetica", 50))
    bufferY = tkinter.Label(inputFrame, text="", background='white', pady=50)

    bufferY.grid(row=0,column=1)
    totalLabel.grid(row=1, column=0, columnspan=3)
    promptLabel.grid(row=2, column=0, columnspan=3, pady=(10, 35))
    nameLabel.grid(row=3, column=0)
    numberLabel.grid(row=4, column=0)
    nameInput.grid(row=3, column=2)
    numberInput.grid(row=4, column=2)
    finishButton.grid(row=5, column=0, columnspan=3, pady=(50, 0))
