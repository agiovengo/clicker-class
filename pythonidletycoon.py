print("Welcome to Python Idle Tycoon!")

formatMoney = "${:0,.2f}"
dividerLines = "----------------------------------------------------"


class Store:
    money = 25.00
    day = 1
    StoreList = []

    def __init__(self, storename, storeprofit, storecost):

        self.storeName = storename
        self.storeCount = 0
        self.storeProfit = storeprofit
        self.storeCost = storecost

    @classmethod
    def display_game_info(cls):
        print(dividerLines)
        print("Day #" + str(cls.day))
        print("Money = %s" % formatMoney.format(cls.money))

        print(dividerLines)
        print("Stores".ljust(25) + "Store Cost".ljust(15) + "Store Count")
        i = 1
        for store in cls.StoreList:
            store.display_store_info(i)
            i += 1
        print(dividerLines)

    def display_store_info(self, i):
        # print("%s      %d" % (self.storeName, self.storeCount))
        storeCostStr = formatMoney.format(self.storeCost).rjust(12)
        print(str(i) + ") " + self.storeName.ljust(20) + storeCostStr.ljust(25) + str(self.storeCount))

    @classmethod
    def buy_store(cls):
        try:
            whichstore = int(input("Which Store Do You Wish to Buy? (1-%s):" % len(Store.StoreList)))
        except:
            print("INVALID INPUT. Buy Aborted")
            return

        if whichstore >= 1 and whichstore <= len(Store.StoreList):
            store = Store.StoreList[whichstore - 1]
            if store.storeCost < Store.money:
                store.storeCount += 1

                Store.money -= store.storeCost
            else:
                print("You don't have enough money")
        else:
            print("INCORRECT INPUT: Enter a number 1-%s" % len(Store.StoreList))

    @classmethod
    def next_day(cls):
        cls.day += 1
        for store in cls.StoreList:
            daily_profit = store.storeProfit * store.storeCount
            cls.money += daily_profit

    @classmethod
    def advanceWeek(cls):
        for i in range(0, 7):
            # print("%s - nextdaycall" % i)
            cls.next_day()


# Create a New Store
Store.StoreList.append(Store('Lemonade Stand', 1.50, 3))
Store.StoreList.append(Store('Record Store', 5, 15))
Store.StoreList.append(Store('Ice Cream Store', 10, 90))


# Main Game
while True:
    # Call the Class Method to Display Game Info
    Store.display_game_info()

    # Display Store Info

    print("Available Options: (N)ext Day, (W)eek Advance, (B)uy Store, (Q)uit")
    result = input("Please Enter Your Selection: ")
    if result.upper() == "B":
        Store.buy_store()
    elif result.upper() == "N":
        Store.next_day()
    elif result.upper() == "W":
        Store.advanceWeek()
    elif result.upper() == "Q":
        break
    else:
        print("Bad input")
print("Thank you for playing Python Idle Tycoon")
