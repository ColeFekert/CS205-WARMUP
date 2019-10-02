# Nick Bouffard, Cole Fekert, Kyle Mac, and Henry Rice
# CS 205 - Warmup Project
# Pizza Search tool

import sqlite3, csv,string

def main():

    keepGoing = "y"

    # Introduction to program
    print("Welcome to PizzaSearch3000")
    print("Please enter search query")

    # # Call database integration function
    # createTables()

    while keepGoing == "y":
        # Call search function
        # search()

        # Ask if user would like to search again
        keepGoing = input("Would you like to search again? (y/n)")

        # try:
        #     keepGoing = input("Would you like to search again? (y/n)")
        #     if keepGoing != "y" or keepGoing != "n":
        #         raise ValueError
        # except ValueError:
        #     keepGoing = input("Please try again (y/n)")
        # else:
        #     print("I got here")


        # IF no, continue = 0

def createTables():
        #Create database
        conn = sqlite3.connect('pizzaCities.db')
        c = conn.cursor()

        #Create table 1 - Pizzas
        c.execute("CREATE TABLE pizzas (address text, categories text, city text, keys text, name text,"
                  " postalCode integer, price string, state string)")
        with open('pizza.csv', 'r') as pizzaTable:
            data = csv.DictReader(pizzaTable)
            toPizzaDB = [(i['address'], i['categories'], i['city'], i['keys'],
                i['name'], i['postalCode'], i['price'], i['state']) for i in data]
        c.executemany("INSERT INTO pizzas VALUES (?,?,?,?,?,?,?,?);", toPizzaDB)

        # Create table 2 - Cities
        c.execute("CREATE TABLE cities (rank integer, city text, state text, population integer, growth real) ")
        with open('cities.csv', 'r') as cityTable:
            data = csv.DictReader(cityTable)
            toCityDB = [(i['rank'], i['city'], i['state'], i['population'], i['growth']) for i in data]
        c.executemany("INSERT INTO cities VALUES (?,?,?,?,?);", toCityDB)
        conn.commit()
        conn.close()


# Iterate through each of the elements of the query and check that they are
# as they should be.
def verifyQuery(query):
    # What we're checking against
    possibleInitialQueryElements = ["cities", "pizza", "postal"]
    ignorableQueryElements = ["with", "in", "for", "places"]
    possibleQueryElements = ["price", "population", "cities", "pizza", "postalcode"]
    # cardinalDirections = ["north", "south", "east", "west", "northwest", "southwest", "northeast", "southeast"]
    priceElements = ["$", "$$", "$$$"]

    approved = False

    while not approved:
        query.clear()
        print()
        query = input("Enter the query: ").split()
        # print(query)
        # Where we iterate and check
        error = False

        # Make sure the query begins correctly
        if query[0] not in possibleInitialQueryElements:
            error = True
        else:
            if query[0] == "pizza":
                query[0] = "pizza places"
                #query.remove(query[1])
            elif query[0] == "postal":
                query[0] = "postal code"
                #query.remove(query[1])

        print(query)
        approvedQueryElements = []
        for i in range(len(query)):
            if i == 0:
                # Skip the first element, since its already been handled
                approvedQueryElements.append(query[i])
                continue
            if query[i] in possibleQueryElements:
                # Query element is approved, so continue to the next element
                approvedQueryElements.append(query[i])
                continue

            elif query[i] == "price" or query[i - 1] == "population":
                 continue
            if query[i] in ignorableQueryElements:
                continue
            if query[i] in possibleQueryElements:
                if query[i] == "pizza":
                    approvedQueryElements.append("pizza places")
                    continue
                elif query[i] == "postal":
                    approvedQueryElements.append("postal code")
                    continue
                elif query[i] == "price":
                    if query[i + 1] not in priceElements:
                        error = True
                    else:
                        approvedQueryElements.append("price")
                        approvedQueryElements.append(query[i+1])
                        continue
                elif query[i] == "population":
                    if not query[i + 1].isdigit():
                        error = True
                    else:
                        approvedQueryElements.append("population")
                        approvedQueryElements.append(query[i + 1])
                # Query element is approved, so continue to the next element
                #continue
            else:
                approvedQueryElements.append(query[i])

        if not error:
            approved = True
    print(approvedQueryElements)
    return approvedQueryElements


def parseQuery(query):
    stringQuery = ""

    if query[0] == "cities":
        stringQuery = "SELECT city FROM cities "
    elif query[0] == "pizza places":
        stringQuery = "SELECT name FROM pizzas "
    elif query[0] == "postal code":
        stringQuery = "SELECT postalCode FROM pizzas "

    for i in range(len(query)):
        if i == 0:
            # get past the first element - then continue query construction
            continue
        else:
            if query[i] == "price":
                prices = ['$', '$$', '$$$']
                if query[i + 1] in prices:
                    if query[i + 1] == '$':
                        stringQuery += "WHERE price = '$'"
                    elif query[i + 1] == '$$':
                        stringQuery += "WHERE price = '$$'"
                    elif query[i + 1] == '$$$':
                        stringQuery += "WHERE price = '$$$'"
                else:
                    # User didn't enter a price value after price - which is needed
                    # So we use a default value instead
                    print("ERROR: User did not enter value after price. Using default value of $$.")
                    stringQuery += "WHERE population = $$"

            elif query[i] == "population":
                if query[i + 1].isdigit():
                    stringQuery += "WHERE population < " +str(query[i + 1])
                else:
                    # User didn't enter a number after population - which is needed
                    # So we use a default value instead
                    print("ERROR: User did not enter number after population. Using default value of 50,000.")
                    stringQuery += "WHERE population < 50000"

            elif query[i] == "postal code":
                if query[i + 1].isdigit():
                    stringQuery += "WHERE postalCode = " + str(query[i + 1])
                else:
                    # User didn't enter a number after population - which is needed
                    # So we use a default value instead
                    print("ERROR: User did not enter number after postal code. Using default value of 10001.")
                    stringQuery += "WHERE postalCode = 10001"

    return stringQuery

def executeQuery(statement):
    conn = sqlite3.connect('pizzaCities.db')
    c = conn.cursor()
    c.execute(statement)
    fetch = c.fetchall
    print(fetch)

def search():
    # Receive search query and interact with database appropriately

    # Initializes the array to store the query elements in
    query = []

    theActualQuery = parseQuery(verifyQuery(query))
    print(theActualQuery)
    executeQuery(theActualQuery)


main()


