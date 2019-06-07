print("Welcome to Python Idle Tycoon!")

money = 25.00
day = 1
storeName = "Lemonade Stand"
storeCount = 1
storeProfit = 1.50


def display_store_info():
    print("------------------------------------")
    print("Day #" + str(day))
    print("Money = $" + str(money))
    print("Store Count = " + str(storeCount))
    print("------------------------------------")


def buy_store(store_count_var, money_var):
    store_count_var += 1
    money_var -= 3.0
    return store_count_var, money_var


def next_day(date, daily_money):
    date += 1
    daily_profit = storeProfit * storeCount
    daily_money += daily_profit
    return date, daily_money


while True:
    display_store_info()

    print("Available Options: (N)ext Day, (B)uy Store, (Q)uit")
    result = input("Please Enter Your Selection: ")
    if result is "B" or result is "b":
        storeCount, money = buy_store(storeCount, money)
    if result is "N" or result is "n":
        day, money = next_day(day, money)
    if result is "Q" or result is "q":
        break
