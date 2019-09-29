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


# conn = sqlite3.connect('pizzaCities.db')
#         c = conn.cursor()

# def getSectionalQuery():
#     sectionalQuery = ""
#     inputNotApproved = True
#
#     while inputNotApproved:
#         sectionalQuery = input("Enter sectional query: ")
#
#         sectionalQuery.lower()
#
#         if "pizza places" in sectionalQuery:
#             return "pizza places "
#         elif "cities" in sectionalQuery:
#             return "cities "
#         elif "postal code" in sectionalQuery:
#             return "postal code "
#         else:
#             inputNotApproved = True
#
#
# def getRestrictiveQuery():
#     inputNotApproved = True
#     restrictiveQuery = []
#
#     while inputNotApproved:
#         restrictiveQuery[0] = input("Enter the category you want to narrow down: ")
#
#         secondInputNotApproved = True
#         restrictiveQuery[0].lower()
#
#         if "price" in restrictiveQuery[0]:
#             restrictiveQuery[0] = "price "
#             while secondInputNotApproved:
#                 restrictiveQuery[1] = input("Enter price ($,$$,$$$):  ")
#
#                 if restrictiveQuery[1].isalpha():
#                     secondInputNotApproved = True
#                 else:
#                     secondInputNotApproved = False
#             return restrictiveQuery
#
#         elif "population" in restrictiveQuery[0]:
#             while secondInputNotApproved:
#                 restrictiveQuery[1] = input("Enter max population: ")
#
#                 if restrictiveQuery[1].isalpha():
#                     secondInputNotApproved = True
#                 else:
#                     secondInputNotApproved = False
#             return restrictiveQuery
#         elif "cardinal location" in restrictiveQuery[0]:
#             while secondInputNotApproved:
#                 restrictiveQuery[1] = input("Enter cardinal direction: ")
#
#                 restrictiveQuery[1].lower()
#
#                 if restrictiveQuery[1].isdecimal() or restrictiveQuery[1].isdigit():
#                     secondInputNotApproved = True
#                 elif "north" in restrictiveQuery[1]:
#                     secondInputNotApproved = False
#                 elif "south" in restrictiveQuery[1]:
#                     secondInputNotApproved = False
#                 elif "east" in restrictiveQuery[1]:
#                     secondInputNotApproved = False
#                 elif "west" in restrictiveQuery[1]:
#                     secondInputNotApproved = False
#                 elif "northeast" in restrictiveQuery[1]:
#                     secondInputNotApproved = False
#                 elif "northwest" in restrictiveQuery[1]:
#                     secondInputNotApproved = False
#                 elif "southeast" in restrictiveQuery[1]:
#                     secondInputNotApproved = False
#                 elif "southwest" in restrictiveQuery[1]:
#                     secondInputNotApproved = False
#                 else:
#                     secondInputNotApproved = True
#
#             return restrictiveQuery
#         else:
#             inputNotApproved = True
#
#
# def getModifierQuery():
#     inputNotApproved = True
#
#     while inputNotApproved:
#         modifierQuery = input("Enter modifier to previous Query: ")
#
#         modifierQuery.lower()
#
#         if "with" in modifierQuery:
#             return "with "
#         elif "in" in modifierQuery:
#             return "in "
#         else:
#             inputNotApproved = True
        
def verifyQuery(query):
    # What we're checking against
    possibleQueryElements = ["cities", "pizza places", "postal code"]
    ignorableQueryElements = ["with", "in", "for"]
    calculationQueryElements = ["price", "population", "cardinal direction"]
    cardinalDirections = ["north", "south", "east", "west", "northwest", "southwest", "northeast", "southeast"]

    approved = False

    while not approved:
        query = input("Enter the query: ").split()
        # Where we iterate and check
        error = False
        for i in range(len(query)):
            if query[i] in possibleQueryElements or query[i] in calculationQueryElements:
                if query[i] == "cardinal direction":
                    if query[i + 1] not in cardinalDirections:
                        error = True
            elif query[i] in ignorableQueryElements:
                query.remove(query[i])
                error = False
            else:
                error = True

        if not error:
            approved = True

    # Possible idea: Iterate through each of the elements of the query and check that they are
    # as they should be. Then build the query after its been verified.

    return approved


def parseQuery(query):
    stringQuery = ""

    if query[0] == "cities":
        stringQuery = "SELECT cities "
    elif query[0] == "pizza places":
        stringQuery = "SELECT pizza places "
    elif query[0] == "postal code":
        stringQuery = "SELECT postal code "

    for i in range(len(query)):
        if i == 0:
            # get past the first element - then continue query construction
            continue
        else:
            if query[i] == "price":
                if query[i + 1].isdigit():
                    stringQuery += "WHERE price < " + str(query[i + 1])
            elif query[i] == "population":
                if query[i + 1].isdigit():
                    stringQuery += "WHERE population < " +str(query[i + 1])
            elif query[i] == "cardinal direction":
                if query[i + 1] == "north":
                    stringQuery += "WHERE latitude > ??? AND WHERE longitude > ???"
                elif query[i + 1] == "south":
                    # do something else
                elif query[i + 1] == "east":
                    # do something else
                elif query[i + 1] == "west":
                    # do something else
                elif query[i + 1] == "northeast":
                    # do something else
                elif query[i + 1] == "northwest":
                    # do something else
                elif query[i + 1] == "southeast":
                    # do something else
                elif query[i + 1] == "southwest":
                    # do something else

def search():
    # Receive search query and interact with database appropriately
    c = sqlite3.connect('pizzaCities.db')
    cur = c.cursor()

    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%& GET INPUT FROM USER %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&

    continueQuery = True
    queryApproved = False

    query = []

    verifyQuery(query)
    theActualQuery = parseQuery(query)

    # execute query



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
    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%& QUERY THE DATABASE %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&
    # %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%& Older code %&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&

    print("Enter first part of query below:")
    print("Examples: 'pizza places', 'cities', or 'number of'")
    q1 = input("First part of query: ")

    if q1.startswith("population"):
        value = q1.partition('population ')[2]
        cur.execute("SELECT population FROM cities WHERE city =?", (value,))
        try:
            fetch = cur.fetchone()[0]
            print(fetch)
        except:
            print("An exception has occurred")

    elif q1.startswith("number"):
        value = q1.partition('number ')
        # need the rest of query before executing


main()
