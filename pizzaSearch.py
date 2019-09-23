# Nick Bouffard, Cole Fekert, Kyle Mac, and Henry Rice
# CS 205 - Warmup Project
# Pizza Search tool

import sqlite3, csv


def main():

    #continue = 1

    # Introduction to program
    print("Welcome to PizzaSearch3000")
    print("Please enter search query")

    # Call database integration function
    # createTables()

    #while continue == 1
        # Call search function
        # Ask if user would like to search again
        # IF no, continue = 0


def createTables():
        #Create database
        conn = sqlite3.connect('pizzaCities.db')
        c = conn.cursor()

        #Create table 1 - Pizzas
        c.execute("CREATE TABLE pizzas (address text, categories text, city text, keys text, menusAmountMax real,"
                  "menusAmountMin real, name text, postalCode integer, priceRangeMin integer, priceRangeMax integer,"
                  "province text) ")
        with open('pizza.csv', 'r') as pizzaTable:
                data = csv.DictReader(pizzaTable)
                toPizzaDB = [(i['address'], i['categories'], i['city'], i['keys'], i['menus.amountMax'],
                         i['menus.amountMin'], i['name'], i['postalCode'], i['priceRangeMin'], i['priceRangeMax'],
                         i['province']) for i in data]
        c.executemany("INSERT INTO pizzas VALUES (?,?,?,?,?,?,?,?,?,?,?);", toPizzaDB)

        # Create table 2 - Cities
        c.execute("CREATE TABLE cities (rank integer, city text, state text, population integer, growth real) ")
        with open('cities.csv', 'r') as cityTable:
            data = csv.DictReader(cityTable)
            toCityDB = [(i['rank'], i['city'], i['state'], i['population'], i['growth']) for i in data]
        c.executemany("INSERT INTO cities VALUES (?,?,?,?,?);", toCityDB)
        conn.commit()


# conn = sqlite3.connect('pizzaCities.db')
#         c = conn.cursor()
        
    # Load CSVs into database tables

def search(query):
    # Receive search query and interact with database appropriately
    x = 2


main()
