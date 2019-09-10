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
    createTables()

    #while continue == 1
        # Call search function
        # Ask if user would like to search again
        # IF no, continue = 0

def createTables():
        #Create database
        conn = sqlite3.connect('pizzaCities.db')
        c = conn.cursor()
        
        #Create table 1 - Pizzas
        c.execute("CREATE TABLE pizzas (address text, categories text, city text, keys text, menusAmountMax real, menusAmountMin real, name text, postalCode integer, priceRangeMin integer, priceRangeMax integer, province text) ")
        with open('pizza.csv', 'r') as pizzaTable:
                data = csv.DictReader(pizzaTable)
                toDB = [(i['address'], i['categories'], i['city'], i['keys'], i['menus.AmountMax'], i['menus.AmountMin'], i['name'], i['postalCode'], i['priceRangeMin'], i['priceRangeMax'], i['province']) for i in data]
        c.executemany("INSERT INTO pizzaCities VALUES (?,?,?,?,?,?,?,?,?,?,?);", toDB)
        conn.commit()



        
    # Load CSVs into database tables

def search(query):
    # Receive sarch query and interact with database appropriately


main()
