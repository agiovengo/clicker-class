import tkinter as tk
from tkinter import ttk
import time
import csv
from tkinter import *
from tkinter import messagebox

formatMoney = "${:0,.2f}"
dividerLines = "----------------------------------------------------"
datafile = "data.csv"
padding = 20
window_size = "900x450"


class StoreTimer():
    UpdateFreq = 100

    def __init__(self, store):
        self.Timer = store.Timer
        self.store = store
        self.TimerRunning = False
        # self.StartTimer()

    def StartTimer(self):
        if self.TimerRunning is False:
            self.TimerRunning = True
            self.starttime = time.time()
            root.after(StoreTimer.UpdateFreq, self.UpdateTimer)

    def UpdateTimer(self):
        elapsed = time.time() - self.starttime
        if elapsed < self.Timer:
            self.store.progressbar["value"] = elapsed / self.Timer * 100
            root.after(StoreTimer.UpdateFreq, self.UpdateTimer)
        else:
            self.TimerRunning = False
            self.store.progressbar["value"] = 0
            self.store.MakeMoney()
            if self.store.ManagerUnlocked is True:
                self.StartTimer()

class Store:
    money = 5.00
    day = 1
    StoreList = []

    def __init__(self, storename, storeprofit, storecost, timer, managercost, image, growthfactor):

        self.storeName = storename
        self.storeCount = 0
        self.storeProfit = float(storeprofit)
        self.storeCost = float(storecost)
        self.Timer = float(timer)
        self.ManagerUnlocked = False
        self.ManagerCost = float(managercost)
        self.TimerObject = StoreTimer(self)
        self.Image = image
        self.growthfactor = float(growthfactor)

    @classmethod
    def display_stores(cls):
        Store_Label_col0 = tk.Label(root, text="Click", font="Helvetica 12")
        Store_Label_col0.grid(row=4, column=0, padx=padding)
        Store_Label_col1 = tk.Label(root, text="Store Name", font="Helvetica 12")
        Store_Label_col1.grid(row=4, column=1, padx=padding)
        Store_Label_col2 = tk.Label(root, text="Progress", font="Helvetica 12")
        Store_Label_col2.grid(row=4, column=2, padx=padding)
        Store_Label_col3 = tk.Label(root, text="Cost", font="Helvetica 12")
        Store_Label_col3.grid(row=4, column=3, padx=padding)
        Store_Label_col4 = tk.Label(root, text="Count", font="Helvetica 12")
        Store_Label_col4.grid(row=4, column=4, padx=padding)
        Store_Label_col5 = tk.Label(root, text="Buy", font="Helvetica 12")
        Store_Label_col5.grid(row=4, column=5, padx=padding)
        Store_Label_col6 = tk.Label(root, text="Unlock Manager", font="Helvetica 12")
        Store_Label_col6.grid(row=4, column=6, padx=padding)
        i = 1
        for store in cls.StoreList:
            store.display_store_info(i)
            i += 1
        print(dividerLines)

    def display_store_info(self, i):
        # Click Button
        self.clickbutton = tk.Button(root, command=lambda : self.ClickStore())
        photo = PhotoImage(file="images/" + self.Image)
        self.clickbutton.config(image=photo, width="40", height="40")
        self.clickbutton.image = photo
        self.clickbutton.grid(row=4 + i, column=0, padx=padding)

        # Store Label
        self.storecountlabel = tk.Label(root, text=self.storeName)
        self.storecountlabel.grid(row=4 + i, column=1, padx=padding)

        # Progress Bar
        self.progressbar = ttk.Progressbar(root, value=0, maximum=100, orient=tk.HORIZONTAL, length=190, mode='indeterminate')
        self.progressbar.grid(row=4 + i, column=2, padx=padding)

        # Store Cost
        self.storecostlabel = tk.Label(root, text=formatMoney.format(self.storeCost))
        self.storecostlabel.grid(row=4 + i, column=3, padx=padding)

        # Store Count
        self.storecountlabel = tk.Label(root, text=self.storeCount)
        self.storecountlabel.grid(row=4 + i, column=4, padx=padding)

        # Buy Button
        self.buybutton = tk.Button(root, text=formatMoney.format(self.storeCost), width=7, command=lambda: self.buy_store())
        self.buybutton.grid(row=4 + i, column=5, padx=padding)

        # Manager Button
        self.managerbutton = tk.Button(root, text=formatMoney.format(self.ManagerCost), width=10, command=lambda: self.UnlockManager())
        self.managerbutton.grid(row=4 + i, column=6, padx=padding)

    def buy_store(self):
        if self.storeCount == 0:
            NextStoreCost = self.storeCost
        else:
            NextStoreCost = self.storeCost * self.growthfactor * self.storeCount

        if NextStoreCost < Store.money:
            self.storeCount += 1

            Store.money -= NextStoreCost
            self.storecountlabel.config(text=self.storeCount)
            NextStoreCost = self.storeCost * self.growthfactor * self.storeCount
            self.buybutton.config(text=formatMoney.format(NextStoreCost))
            Game.UpdateUI()
        else:
            messagebox.showinfo("Not Enough Money", "Not Enough Money to Buy Store")

    def UnlockManager(self):
        if self.ManagerCost <= Store.money:
            self.ManagerUnlocked = True
            Store.money -= self.ManagerCost
            self.managerbutton.configure(state="disabled")
            Game.UpdateUI()
        else:
            messagebox.showinfo("Not Enough Money", "Not Enough Money to Buy Manager")

    def ClickStore(self):
        self.TimerObject.StartTimer()

    def MakeMoney(self):
        daily_profit = self.storeProfit * self.storeCount
        Store.money += daily_profit
        Game.UpdateUI()

    @classmethod
    def CreateStores(cls, gamemanager):
        _gamemanager = gamemanager
        # Read data from file
        with open(datafile, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                cls.StoreList.append(Store(*row))
        cls.display_stores()


class GameManager():
    def __init__(self):

        # Setup UI
        self._GameUI = GameUI()

        # Setup Stores
        Store.CreateStores(self)
        self._GameUI.DisplayGameHeader()

    def UpdateUI(self):
        self._GameUI.UpdateUI()

class GameUI():
    def DisplayGameHeader(self):
        root.title("Python Idle Tycoon Business Game")
        root.geometry(window_size)
        self.money_amount_label = tk.Label(root, text=formatMoney.format(Store.money), font="Helvetica 18 bold")
        self.money_amount_label.grid(row=1, column=0)

    def UpdateUI(self):
        self.money_amount_label.config(text=formatMoney.format(Store.money))

# Main Game

root = tk.Tk()

Game = GameManager()
root.mainloop()
