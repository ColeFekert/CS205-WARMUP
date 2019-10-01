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
        search()

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
        conn.close()


# Iterate through each of the elements of the query and check that they are
# as they should be.
def verifyQuery(query):
    # What we're checking against
    possibleInitialQueryElements = ["cities", "pizza", "postal"]
    ignorableQueryElements = ["with", "in", "for"]
    possibleQueryElements = ["price", "population", "cities", "pizza places", "postal code"]
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
                query.remove(query[1])
            elif query[0] == "postal":
                query[0] = "postal code"
                query.remove(query[1])

        print(query)

        for i in range(len(query)):
            if i == 0:
                # Skip the first element, since its already been handled
                continue

            elif query[i - 1] == "price" or query[i - 1] == "population":
                continue

            elif query[i] in possibleQueryElements:
                if query[i] == "pizza":
                    query[i] = "pizza places"
                    query.remove(query[i + 1])
                elif query[i] == "postal":
                    query[i] = "postal code"
                    query.remove(query[i + 1])
                elif query[i] == "price":
                    if query[i + 1] not in priceElements:
                        error = True
                elif query[i] == "population":
                    if not query[i + 1].isdigit():
                        error = True

                # Query element is approved, so continue to the next element
                #continue
            elif query[i] in ignorableQueryElements:
                # Query element can be stripped out
                query.remove(query[i])
                error = False
            else:
                # Query element was not approved
                error = True

        if not error:
            approved = True

    return query


def parseQuery(query):
    stringQuery = ""

    if query[0] == "cities":
        stringQuery = "SELECT city FROM cities "
    elif query[0] == "pizza places":
        stringQuery = "SELECT name FROM pizza "
    elif query[0] == "postal code":
        stringQuery = "SELECT postalCode FROM pizza "

    for i in range(len(query)):
        if i == 0:
            # get past the first element - then continue query construction
            continue
        else:
            if query[i] == "price":
                prices = ['$', '$$', '$$$']

                if query[i + 1] in prices:
                    if query[i + 1] == '$':
                        stringQuery += "WHERE price = $"
                    elif query[i + 1] == '$$':
                        stringQuery += "WHERE price = $$"
                    elif query[i + 1] == '$$$':
                        stringQuery += "WHERE price = $$$"
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

def search():
    # Receive search query and interact with database appropriately
    c = sqlite3.connect('pizzaCities.db')
    cur = c.cursor()

    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%& GET INPUT FROM USER %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&

    continueQuery = True
    queryApproved = False

    query = []

    theActualQuery = parseQuery(verifyQuery(query))
    print(theActualQuery)

    # execute query
    cur.execute(theActualQuery)
    ## Not sure if the part below is needed
    # try:
    #     fetch = cur.fetchone()[0]
    #     print(fetch)
    # except:
    #     print("An exception has occurred")



    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%& QUERY THE DATABASE %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&
    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%& Older code %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&

    # print("Enter first part of query below:")
    # print("Examples: 'pizza places', 'cities', or 'number of'")
    # q1 = input("First part of query: ")
    #
    # if q1.startswith("population"):
    #     value = q1.partition('population ')[2]
    #     cur.execute("SELECT population FROM cities WHERE city =?", (value,))
    #     try:
    #         fetch = cur.fetchone()[0]
    #         print(fetch)
    #     except:
    #         print("An exception has occurred")
    #
    # elif q1.startswith("number"):
    #     value = q1.partition('number ')
    #     # need the rest of query before executing

    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&&%&%&%&%&%&
    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%& OLD BELOW %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&
    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&&%&%&%&%&%&

    # query = [getSectionalQuery(), getModifierQuery()]

    # if query[1] == "with ":
    #     query.append(getRestrictiveQuery())
    # else:
    #     query.append(getSectionalQuery())
    #
    # cont = input("Add more to the query? (y/n) ")
    # if cont == 'y':
    #     continueQuery = True
    # else:
    #     continueQuery = False
    #
    # # possibly limit how many times we allow a user to extend a query?
    # while continueQuery:
    #     if query[len(query)] == "with ":
    #         query.append(getRestrictiveQuery())
    #         query.append(getModifierQuery())
    #     else:
    #         query.append(getSectionalQuery())
    #         query.append(getModifierQuery())
    #
    # # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%& BUILD QUERY %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&
    # # Need to add handling for 'number of'
    # executionString = "SELECT "
    # for i in range(len(query)):
    #     if (i % 2 == 0):
    #         if query[i - 1] == "with ":
    #             # this means we are on a restrictive query
    #             executionString += query[i][0]
    #             executionString += "< "
    #             executionString += query[i][1]
    #
    #         # this means we are on a sectional query
    #         executionString += query[i]
    #
    #     else:
    #         # this means we are on a modifier query
    #         if query[i] == "with ":
    #             executionString += "WHERE "
    #         else:
    #             executionString += "FROM "
    #
    # cur.execute(executionString)


main()
