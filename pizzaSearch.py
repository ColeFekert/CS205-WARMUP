# Nick Bouffard, Cole Fekert, Kyle Mac, and Henry Rice
# CS 205 - Warmup Project
# Pizza Search tool

import sqlite3, csv,string

def main():

    keepGoing = "y"

    # Introduction to program
    print("+==============================================+")
    print("|         Welcome to Pizza Search 3000         |")
    print("|               Brought to you by              |")
    print("|    Nick Bouffard, Cole Fekert, Henry Rice    |")
    print("|                      &                       |")
    print("|                   Kyle Mac                   |")
    print("+==============================================+")

    # # Call database integration function
    # createTables()

    while keepGoing == "y":
        # Call search function
        search()

        # Ask if user would like to search again
        keepGoing = input("Would you like to search again? (y/n)")


def createTables():
        #Create database
        conn = sqlite3.connect('pizzaCities.db')
        c = conn.cursor()

        #Create table 1 - Pizzas
        c.execute("CREATE TABLE pizzas (address text, categories text, city text, keys text, pizzaName text,"
                  " postalCode integer, price string, state string)")
        with open('pizza.csv', 'r') as pizzaTable:
            data = csv.DictReader(pizzaTable)
            toPizzaDB = [(i['address'], i['categories'], i['city'], i['keys'],
                i['pizzaName'], i['postalCode'], i['price'], i['state']) for i in data]
        c.executemany("INSERT INTO pizzas VALUES (?,?,?,?,?,?,?,?);", toPizzaDB)

        # Create table 2 - Cities
        c.execute("CREATE TABLE cities (rank integer, city text, state text, population integer, growth real," 
        "FOREIGN KEY(city) REFERENCES cities (city))")
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
    ignorableQueryElements = ["with", "in", "for", "places", "code", "place"]
    possibleQueryElements = ["price", "population", "cities", "postalcode"]
    priceElements = ["$", "$$", "$$$"]

    approved = False

    while not approved:
        query.clear()

        print("+==============================================+")
        print("|                 Query Format:                |")
        print("|                                              |")
        print("| Example Queries:                             |")
        print("|       - pizza in city Dallas                 |")
        print("|       - pizza in postal 11801                |")
        print("|       - cities with price $$                 |")
        print("|       - postal city Dallas                   |")
        print("|                                              |")
        print("| Syntax Considerations:                       |")
        print("|       - postal code can be entered as        |")
        print("|         postal/postal code.                  |")
        print("|                                              |")
        print("|       - Enter cities with no spaces and      |")
        print("|         capitalized (camelCase).             |")
        print("|                                              |")
        print("|       - You do not have to have in/with/etc. |")
        print("|         in your query.                       |")
        print("|                                              |")
        print("|       - pizza places can be written as pizza.|")
        print("|                                              |")
        print("|       - price has to be followed by $/$$/$$$.|")
        print("|                                              |")
        print("|       - population has to be followed by     |")
        print("|         an integer.                          |")
        print("|                                              |")
        print("|       - postal code has to be followed by    |")
        print("|         an integer that is 5 digits long.    |")
        print("|                                              |")
        print("| Rules:                                       |")
        print("|       - Queries must start with one of the   |")
        print("|         following: pizza, cities, postal.    |")
        print("|                                              |")
        print("|       - Queries can not be longer than 2     |")
        print("|         selections, an example of a query    |")
        print("|         that breaks this rule would be:      |")
        print("|         'pizza population 40000 price $$'    |")
        print("|         Because pizza, population, and price |")
        print("|         are each selections.                 |")
        print("|                                              |")
        print("|                                              |")
        print("+==============================================+")
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

            elif query[0] == "postal":
                query[0] = "postal code"


        #print(query)
        approvedQueryElements = []

        querySize = len(query)

        for i in range(querySize):
            if i == 0:
                # Skip the first element, since its already been handled
                approvedQueryElements.append(query[i])
                continue


            elif query[i] == "price":
                approvedQueryElements.append(query[i])
                continue

            elif query[i] == "population":
                approvedQueryElements.append(query[i])
                continue

            elif query[i] == "postal" or query[i].lower() == "postalcode":
                approvedQueryElements.append("postal code")
                continue

            elif query[i] == "cities" or query[i] == "city":
                approvedQueryElements.append("cities")
                continue

            elif query[i] in ignorableQueryElements:
                continue

            elif query[i] in priceElements:
                if approvedQueryElements[-1] == "price":
                    approvedQueryElements.append(query[i])
                else:
                    error = True

            elif query[i].isdigit():
                if approvedQueryElements[-1] == "population":
                    approvedQueryElements.append(query[i])
                elif approvedQueryElements[-1] == "postal code":
                    if (len(query[i]) > 5 or len(query[i]) < 0):
                        error = True
                    else:
                        approvedQueryElements.append(query[i])

            elif query[i - 1] == "cities" or query[i - 1] == "city":
                conn = sqlite3.connect('pizzaCities.db')
                c = conn.cursor()
                c.execute("SELECT city FROM cities")
                fetch = c.fetchall()

                cities = set()

                for row in fetch:
                    for city in row:
                        cities.add(city)

                cityApproved = False

                for city in cities:
                    if query[i] == city:
                        cityApproved = True

                if cityApproved:
                    approvedQueryElements.append(query[i])

                else:
                    error = True
                continue


            else:
                error = True
                # approvedQueryElements.append(query[i])

        if not error:
            approved = True

    return approvedQueryElements


def parseQuery(query):
    stringQuery = ""

    if query[0] == "cities":
        stringQuery = "SELECT cities.city FROM cities "
    elif query[0] == "pizza places":
        stringQuery = "SELECT pizzaName FROM pizzas "
    elif query[0] == "postal code":
        stringQuery = "SELECT postalCode FROM pizzas "

    for i in range(len(query)):
        if i == 0:
            # get past the first element - then continue query construction
            continue
        else:
            if query[i] == "price":
                if query[0] == "cities":
                    stringQuery += "INNER JOIN pizzas on pizzas.city = cities.city "
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
                    stringQuery += "WHERE price = '$$'"

            elif query[i] == "population":
                if query[0] == "pizza places":
                    stringQuery += "INNER JOIN cities on cities.city = pizzas.city "
                if query[i + 1].isdigit():
                    stringQuery += "WHERE population < " +str(query[i + 1]) + " "
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

            elif query[i] == "cities" or query[i] == "city":
                if len(query) <= (i + 1):
                    stringQuery += "INNER JOIN cities on cities.city = pizzas.city WHERE pizzas.city = 'New York' "

                else:
                    stringQuery += "INNER JOIN cities on cities.city = pizzas.city WHERE pizzas.city = '" + str(query[i + 1]) + "'"




    return stringQuery

def executeQuery(statement):
    #connects to data base and executes SQL statement
    conn = sqlite3.connect('pizzaCities.db')
    c = conn.cursor()
    c.execute(statement)
    fetch = c.fetchall()

    dataSet = set()

    for row in fetch:
         for element in row:
             dataSet.add(element)

    count = 1
    for element in dataSet:
        print(str(count) + ": " + str(element))
        count += 1
    print("Returned " + str(count-1) + " results.")

    c.close()

def search():
    # Receive search query and interact with database appropriately

    # Initializes the array to store the query elements in
    query = []

    theActualQuery = parseQuery(verifyQuery(query))
    # print(theActualQuery)
    executeQuery(theActualQuery)


main()


