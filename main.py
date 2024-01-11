import functions as funcs

while True:
    option = input("1 - New game \n2 - Load Game\n3 - Options\n\n")
    print()  # Just to skip one line

    if option == "1":
        """ Read some of the information about a new game from a config file, and
            build the missing information accordingly"""
        infoGame = funcs.newGameInfo('cfg.newGame.txt')
        break
    elif option == "2":
        """ Read all the information about an old game from a file"""
        # Our program will locate all saved files and allow the player to choose
        # among them without needing to type the desired file name.
        infoGame = funcs.oldGameInfo()
        break
    elif option == "3":
        funcs.config()
    else:
        print("You didn't type it correctly.")

# infoGame is a tuple with several different values??    
botSize, nrBotts, expertise, nrErrors, fullBottles, bottles = infoGame

endGame = False
funcs.showBottles(bottles, botSize, nrErrors)
source = funcs.askUserFor("Source bottle? ", bottles.keys())
# Let's play the game
while not endGame and not source == 'Z':
    destin = funcs.askUserFor("Destination bottle? ", bottles.keys())
    if funcs.moveIsPossible(botSize, source, destin, bottles):
        funcs.doMove(botSize, source, destin,bottles)
        funcs.showBottles(bottles, botSize, nrErrors)
        if funcs.full(bottles[destin], botSize):
            fullBottles += 1
    else:
        print("Error!")
        nrErrors += 1
    endGame = funcs.allBottlesFull(nrBotts, fullBottles, expertise) or \
              nrErrors == 3
              
    if not endGame:
        source = funcs.askUserFor("Source bottle? (Z to leave game) ",
                                  bottles.keys(), 'Z')
"""
End of game may have happened either because the user filled all the bottles he
was supposed to, or he made 3 errors, or he gave up playing (by inputing 
the letter 'Z'' for the source) 
"""        
if source == 'Z':
    store = funcs.askUserFor("\nWant to store the game for future playing? (YES,NO) ",
                             ['YES', 'NO'], '')
    if store == "YES":
        # FileName will be defined in writeGameInfo() to simplify user experience
        funcs.writeGameInfo(botSize, nrBotts, expertise, nrErrors, fullBottles, bottles)
        print("Hope to see you again soon!")
    else:
        print("Better luck next time!")
else:
    print("Full bottles =", fullBottles, "  Errors =", nrErrors)
    if nrErrors >= 3:
        print("Better luck next time!")
    else:
        print("CONGRATULATIONS!!")

print()
