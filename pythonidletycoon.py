import tkinter as tk
from tkinter import ttk
import time

formatMoney = "${:0,.2f}"
dividerLines = "----------------------------------------------------"


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

    def __init__(self, storename, storeprofit, storecost, timer, managercost):

        self.storeName = storename
        self.storeCount = 0
        self.storeProfit = storeprofit
        self.storeCost = storecost
        self.Timer = timer
        self.ManagerUnlocked = False
        self.ManagerCost = managercost
        self.TimerObject = StoreTimer(self)


    @classmethod
    def display_stores(cls):
        Store_Label_col1 = tk.Label(root, text="Store Name")
        Store_Label_col1.grid(row=4, column=0)
        Store_Label_col2 = tk.Label(root, text="Progress")
        Store_Label_col2.grid(row=4, column=1)
        Store_Label_col3 = tk.Label(root, text="Store Cost")
        Store_Label_col3.grid(row=4, column=2)
        Store_Label_col4 = tk.Label(root, text="Store Count")
        Store_Label_col4.grid(row=4, column=3)
        Store_Label_col5 = tk.Label(root, text="Buy Store")
        Store_Label_col5.grid(row=4, column=4)
        i = 1
        for store in cls.StoreList:
            store.display_store_info(i)
            i += 1
        print(dividerLines)

    def display_store_info(self, i):
        self.clickbutton = tk.Button(root, text=self.storeName, command=lambda: self.ClickStore())
        self.clickbutton.grid(row=4 + i, column=0)
        self.progressbar = ttk.Progressbar(root, value=0, maximum=100, orient=tk.HORIZONTAL, length=190, mode='indeterminate')
        self.progressbar.grid(row=4 + i, column=1)
        self.storecostlabel = tk.Label(root, text=formatMoney.format(self.storeCost))
        self.storecostlabel.grid(row=4 + i, column=2)
        self.storecountlabel = tk.Label(root, text=self.storeCount)
        self.storecountlabel.grid(row=4 + i, column=3)
        self.buybutton = tk.Button(root, text="Buy", command=lambda: self.buy_store())
        self.buybutton.grid(row=4 + i, column=4)
        self.managerbutton = tk.Button(root, text="Unlock Manager", command=lambda: self.UnlockManager())
        self.managerbutton.grid(row=4 + i, column=5)

    def buy_store(self):
        if self.storeCost < Store.money:
            self.storeCount += 1

            Store.money -= self.storeCost
            self.storecountlabel.config(text=self.storeCount)
            Game.UpdateUI()
        else:
            print("You don't have enough money")

    def UnlockManager(self):
        self.ManagerUnlocked = True

    def ClickStore(self):
        self.TimerObject.StartTimer()

    def MakeMoney(self):
        daily_profit = self.storeProfit * self.storeCount
        Store.money += daily_profit
        Game.UpdateUI()


class GameManager():
    def __init__(self):
        self.CreateStores()
        self.DisplayGameHeader()
        Store.display_stores()

    def CreateStores(self):
        Store.StoreList.append(Store('Lemonade Stand', 1.50, 3, 3, 1))
        Store.StoreList.append(Store('Record Store', 5, 15, 10, 200))
        Store.StoreList.append(Store('Ice Cream Store', 10, 90, 30, 5000))

    def DisplayGameHeader(self):
        root.title("Python Idle Tycoon Business Game")

        root.geometry("700x300")

        money_label = tk.Label(root, text="Money")
        money_label.grid(row=0, column=0)

        self.money_amount_label = tk.Label(root, text=formatMoney.format(Store.money))
        self.money_amount_label.grid(row=1, column=0)

    def UpdateUI(self):
        self.money_amount_label.config(text=Store.money)


# Main Game

root = tk.Tk()

Game = GameManager()
root.mainloop()
