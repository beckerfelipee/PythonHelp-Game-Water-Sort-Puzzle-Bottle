import time
from random import randint, shuffle
from time import sleep
from os import path, listdir

# *****************************************************
def topSymbolAndPosition(contents):
    """
    The symbol and position of the top of the bottle, that is,
    of the last position of the list contents

    Parameters
    ----------
    contents : a sequence of characters
        The contents of a bottle.

    Returns
    -------
    symbol : string
        The symbol at the last position. "_" if contents is empty.
    position : int
        The index of the last position. -1 if contents is empty.

    """
    position = len(contents) - 1
    symbol = "_" if contents == [] else contents[position]
    return symbol, position

# *****************************************************
def showBottles(bottles,botSize,nrErrors):
    """
    Prints in the standard output a representation of the
    game bottles.

    Parameters
    ----------
    bottles : dictionary
        Keys are strings and values are lists.
    botSize : int
        The capacity of bottles.
    nrErrors : int
        The number of errors the user already made.

    Returns
    -------
    None.

    """
    print(" " * 3, end = "")
    for letter in bottles.keys():
        print(letter, end = " " * 6) 
    print()
    
    line = botSize - 1
    while line >= 0:
       for content in bottles.values():
           print(" " * 2, end = "")
           if line < len(content):
               print("|" + content[line] + "|", end = "")
           else:
               print("| |", end = "")               
           print(" " * 2, end = "")
       line -= 1
       print()
    print("NUMBER OF ERRORS:", nrErrors)
# *****************************************************
def allBottlesFull(nrBotts, nrBottFull, expert):
    """
    Are all the bottles that are supposed to be full at the end  
    of the game already full?

    Parameters
    ----------
    nrBotts : int
        The number of bottles in the game.
    nrBottFull : int
        The number of bottles already full (with equal symbol).
    expert : int
        The user's expert level.

    Returns
    -------
    True if the number of bottles that are supposed to be full at
    the end of the game is already achieved.

    """
    expectFull = nrBotts - expert
    return nrBottFull == expectFull
# *****************************************************
def full(bottle, botSize):
    """
    Is a given bottle all full with a same symbol?

    Parameters
    ----------
    bottle : list of characters
        The contents of a bottle.
    botSize : int
        The capacity of the bottle.

    Returns
    -------
    bool
        True if the list bottle has botSize elements, all equal.

    """
    if len(bottle) < botSize:
        return False
    top = bottle[0]
    for char in bottle:
        if not char == top:
            return False
    return True

# *****************************************************
def doMove(botSize, source, destin, bottles):
    """
    Transfers as much "liquid" as possible from source to destin

    Parameters
    ----------
    botSize : int
        The capacity of bottles.
    source : string
        The letter that identifies the source bottle in the dict bottles.
    destin : string
        The letter that identifies the destination bottle in the dict bottles.
    bottles : dictionary
        Keys are strings and values are lists.

    Returns
    -------
    int
        The quantity of "liquid" that was transferred from source to destin.

    Requires: 
    --------
        moveIsPossible(botSize, source, destin, bottles)
    """
    sourceSymb, sourceTop = topSymbolAndPosition(bottles[source])
    destSymb, destTop = topSymbolAndPosition(bottles[destin])    
    # How many there are in source to transfer?
    howManyEqual = 0
    i = sourceTop
    sourceContent = bottles[source]
    while i >= 0 and sourceContent[i] == sourceSymb:
       i -= 1
       howManyEqual += 1
    # Transfer as many as possible
    transfer = min(howManyEqual, botSize - destTop - 1)
    for i in range(transfer):
        sourceContent.pop()
        bottles[destin].append(sourceSymb)
    
    return transfer
# *****************************************************
def moveIsPossible(botSize, source, destin, bottles):
    """
    Is it possible to transfer any "liquid" from source to destin?

    Parameters
    ----------
    botSize : int
        The capacity of bottles.
    source : string
        The letter that identifies the source bottle in the dict bottles.
    destin : string
        The letter that identifies the destination bottle in the dict bottles.
    bottles : dictionary
        Keys are strings and values are lists.

    Returns
    -------
    bool
        True if the source is not empty, and, either the destination is empty
        or it has some empty position(s) and the top symbols of both bottles
        are the same.

    Requires: 
    --------
        bottles contain keys source and destin

    """
    sourceSymb, sourceTop = topSymbolAndPosition(bottles[source])
    destSymb, destTop = topSymbolAndPosition(bottles[destin])    
 
    return sourceTop != -1 and \
           (destTop == -1 or
           (destTop < botSize - 1 and sourceSymb == destSymb)) 
# ***************************************************************
def buildGameBottles(nrBotts, botSize, expert, letters, symbols):
    """
    Builds a dictionary of bottles, filled in a random way.

    Parameters
    ----------
    nrBotts : int
        The number of bottles in the game.
    botSize : int
        The capacity of bottles.
    expert : int
        The level of the user's expertise.
    letters : string
        The letters that identify bottles.
    symbols : string
        The symbols that compose the liquid in bottles.

    Returns
    -------
    result : dictionary where keys are strings and values are lists. 
        The dictionary contains nrBotts items, whose keys are the first nrBotts
        characters of letters. The different symbols used to populate the lists
        corresponding to keys are the first (nrBotts - expert) characters of
        symbols. In total, ((nrBotts - expert) * botSize) symbols will be
        randomly distributed by the nrBotts bottles.

    Requires: 
    --------
        letters length is >= nrBotts; symbols length is >= (nrBotts - expert);
        expert < nrBotts

    """   
    result = {}
    howManyFullBott = nrBotts - expert
    allSymbols = randomSymbols(botSize,howManyFullBott,symbols)
    letter = 0
    indexFrom = 0
    # In this way we obtain a more balanced symbol distribution
    indexTo = randint(botSize - expert,botSize)
    for nr in range(nrBotts - 1):
        symbolsToPut = allSymbols[indexFrom : indexTo]
        result[letters[letter]] = symbolsToPut
        letter += 1
        indexFrom = indexTo
        newValueTo = indexTo + randint(botSize - expert,botSize)
        indexTo = min(len(allSymbols), newValueTo)
    symbolsToPut = allSymbols[indexFrom : indexTo]
    result[letters[letter]] = symbolsToPut
        
    return result
# *****************************************************
def randomSymbols(botSize, howMany, symbols):
    """
    Builds and returns a list with (botSize * howMany) characters of symbols

    Parameters
    ----------
    botSize : int
        Capacity of bottles.
    howMany : int
        The number of different symbols to be used.
    symbols : string
        The symbols that can be used.

    Returns
    -------
    list of characters

    Requires: 
    --------
        symbols length is >= howMany;

    """
    # botSize chars of each of the first howMany symbols
    symbolsToUse = symbols[0:howMany]
    result = [s for s in symbolsToUse for _ in range(botSize)]
    shuffle(result)
    return result

# *****************************************************
def askUserFor(ask, options, end = ""):
    """
    Asks the user for some information

    Parameters
    ----------
    ask : string
        The text to be shown the user.
    options : sequence
        The options the user has.
    end : string, optional
        Additional messages to add to the above options. 
        The default is "".

    Returns
    -------
    string
        The user's choice (that belongs to the available options),
        in uppercase.

    """
    listOptions = list(options) + [end]
    answer = input(ask).upper()
    while answer not in listOptions:
       answer = input("Wrong choice! Repeat input: ").upper()
     
    return answer

# *****************************************************
# ***************** NEW FUNCTIONS HERE ****************
# *****************************************************

def newGameInfo(fileName):

    print("Creating a new game...")
    sleep(1)

    try:
        # Abrir o arquivo e ler as informações
        # 'utf-8' para lidar com caracteres especiais e evitar caracteres não esperados. (Â)
        with open(fileName, 'r', encoding='utf-8') as file:
            file_contents = file.readlines()
        # The file is automatically closed here; there's no need to call file.close().

        # Extração das informações do arquivo
        botSize = int(file_contents[1].strip())
        nrBotts = int(file_contents[4].strip())
        symbols = file_contents[7].strip()
        letters = file_contents[10].strip()


        # Opção expertise no arquivo
        expertise_option = file_contents[13].strip()

        # Verificar se expertise_option é "random" ou um número
        if expertise_option.lower() == "random":
            # Geração aleatória do nível de expertise
            expertise = randint(1, 5)
        else:
            expertise = int(expertise_option)

        print("Expertise Level: " + str(expertise))

        # Criação do dicionário representando as garrafas
        bottles = buildGameBottles(nrBotts, botSize, expertise, letters, symbols)

        # Inicialização de outros valores
        nrErrors = 0
        fullBottles = 0

        # Retorno dos valores necessários para o jogo
        return botSize, nrBotts, expertise, nrErrors, fullBottles, bottles

    except Exception as e:
        # Tratamento de exceção em caso de problemas com o arquivo
        raise Exception(f"Erro ao ler o arquivo: {e}")

# Test the Function
# fileName = 'cfg.newGame.txt'
# testInfo = newGameInfo(fileName)
# print(testInfo)

def writeGameInfo(botSize, nrBotts, expertise, nrErrors, fullBottles, bottles):
    try:
        while True:
            user = input("Enter your name to store your game information: ")
            fileName = user + ".txt"

            # Check if the file already exists with the chosen name
            if path.exists(fileName):
                choice = input(f"A file with the name '{fileName}' already exists. "
                               f"Do you want to overwrite it? (YES/NO): ").upper()
                if choice == "YES":
                    break
                else:
                    print("Please choose a different name for your game information.")
            else:
                break

        # Open the file for writing
        with open(fileName, 'w', encoding='utf-8') as file:
            # Write the necessary values to the file
            file.write(f"# Attention - Changing any value in this database may break your save forever.\n\n")
            file.write(f"# Bottle capacity\n{botSize}\n\n")
            file.write(f"# Total number of bottles in the game\n{nrBotts}\n\n")
            file.write(f"# Expertise level\n{expertise}\n\n")
            file.write(f"# Number of Errors\n{nrErrors}\n\n")
            file.write(f"# Number of Full Bottles\n{fullBottles}\n\n")

            # Write the current state of the bottles
            file.write(f"Bottles: \n")
            for letter, content in bottles.items():
                file.write(f"{letter}:{','.join(content)}\n")

        # The file is automatically closed here; there's no need to call file.close().

        print("Game information has been successfully saved in: " + fileName)

    except Exception as e:
        # Exception handling in case of problems with the file
        print(f"Error writing information to the file: {e}")

# Test the Function
# testBottles = {'A': ['%', '+', '!', '%', '$', 'o'],
#               'B': ['#', '$', '!', '+', '+', '!', '$', '!'],
#               'C': ['@', 'o', '#', '%', '+', '$', '@'],
#               'D': ['!', '$', '!', '@', '$'],
#               'E': ['@', '!', '%', '#', '%', '+'],
#               'F': ['!', 'o', '#', '@', '%', '+'],
#               'G': ['$', '$', 'o', '@', '+', '#', '%'],
#               'H': ['o', '#', 'o', '#', '@', '@'],
#               'I': ['#', '+', 'o', 'o', '%'],
#               'J': []}
# writeGameInfo(8, 10, 3, 0, 0, testBottles)

def oldGameInfo():
    try:
        # Obter a lista de arquivos .txt na pasta
        file_list = [f for f in listdir() if f.endswith(".txt") and f != "cfg.newGame.txt"]

        if not file_list:
            print("No game files found.")
            return newGameInfo('cfg.newGame.txt')

        # Mostrar a lista de arquivos para o usuário escolher
        print("Choose a saved game file:")
        for i, filename in enumerate(file_list, start=1):
            print(f"{i}. {filename}")

        # Solicitar ao usuário a escolha do arquivo
        choice = int(input("Enter the number of the file you want to load: "))
        sleep(1)
        selected_file = file_list[choice - 1]

        # Abrir o arquivo selecionado e extrair as informações
        with open(selected_file, 'r', encoding='utf-8') as file:
            file_contents = file.readlines()

        # The file is automatically closed here; there's no need to call file.close().

        # Processar as informações do arquivo
        botSize = int(file_contents[3].strip())
        nrBotts = int(file_contents[6].strip())
        expertise = int(file_contents[9].strip())
        nrErrors = int(file_contents[12].strip())
        fullBottles = int(file_contents[15].strip())

        # Extrair o estado atual das garrafas
        bottles = {}
        for line in file_contents[18:]:
            letter, content = line.strip().split(":")
            bottles[letter] = content.split(',')

        # print(botSize, nrBotts)
        # print(expertise)
        # print(nrErrors, fullBottles)
        # print(bottles)

        print("Game information loaded successfully from " + selected_file)
        sleep(0.5)
        print("Iniciating the game..")
        sleep(1)

        return botSize, nrBotts, expertise, nrErrors, fullBottles, bottles

    except Exception as e:
        # Tratamento de exceção em caso de problemas com o arquivo
        print(f"Error loading information from the file: {e}")
        return None

# test the function
# testInfo: oldGameInfo()
# print(testInfo)


def default_cfg():
    try:
        # Abrir o arquivo de configuração
        with open('cfg.newGame.txt', 'w', encoding='utf-8') as cfg_file:
            # Escrever as opções padrão no arquivo
            cfg_file.write("# Bottle capacity (Min 8)\n")
            cfg_file.write("8")
            cfg_file.write("\n\n# Total number of bottles in the game (Max 10)\n")
            cfg_file.write("10")
            cfg_file.write("\n\n# Available symbols (Must contain 9 different symbols)\n")
            cfg_file.write("@#%$!+o?§")
            cfg_file.write("\n\n# Identifying letters for the bottles (Must contain 10 different letters)\n")
            cfg_file.write("ABCDEFGHIJ")
            cfg_file.write("\n\n# Expertise (options: random; 1; 2; 3; 4; 5)\n")
            cfg_file.write("random")

        print("Default configuration has been set successfully.")

    except Exception as e:
        print(f"Error writing default configuration to the file: {e}")


# Test the function
# default_cfg()

def config():
    while True:
        try:
            # Abrir o arquivo de configuração
            with open('cfg.newGame.txt', 'r', encoding='utf-8') as cfg_file:
                cfg_contents = cfg_file.readlines()

            # Extrair informações do arquivo de configuração
            botSize = int(cfg_contents[1].strip())
            nrBotts = int(cfg_contents[4].strip())
            expertise_option = cfg_contents[13].strip()

            print("|---------------|")
            print("|  Game Config  | ")
            print("|---------------|\n")

            # Exibir valores atuais
            print("- New Game Values")
            print(f"| Bottle capacity: {botSize}")
            print(f"| Total number of bottles: {nrBotts}")
            print(f"| Expertise: {expertise_option}")

            # Oferecer opções para alteração
            print("\n- New Game Options")
            print("a. Change bottle capacity")
            print("b. Change total number of bottles")
            print("c. Change expertise")
            print("d. Reset all New Game Values to default")
            print("\n- Other Options")
            print("z. Go Back\n")

            rewrite = True

            # Solicitar escolha do usuário
            choice = input("Enter your choice: ").lower()

            if choice == 'a':
                new_botSize = int(input("Enter new bottle capacity (between 8 and 20): "))
                if 8 <= new_botSize <= 20:
                    cfg_contents[1] = str(new_botSize) + "\n"
                    print("Bottle capacity updated successfully.")
                else:
                    print("Invalid input. Please check the specified range.")

            elif choice == 'b':
                new_nrBotts = int(input("Enter new total number of bottles (between 7 and 10): "))
                if 7 <= new_nrBotts <= 10:
                    cfg_contents[4] = str(new_nrBotts) + "\n"
                    print("Total number of bottles updated successfully.")
                else:
                    print("Invalid input. Please check the specified range.")

            elif choice == 'c':
                new_expertise = input("Enter new expertise (options: random; 1; 2; 3; 4; 5): ").lower()
                if new_expertise in ['random', '1', '2', '3', '4', '5']:
                    cfg_contents[13] = str(new_expertise) + "\n"
                    print("Expertise updated successfully.")
                else:
                    print("Invalid input. Please check the specified options.")

            elif choice == 'd':
                rewrite = False
                default_cfg()

            elif choice == 'z':
                break

            else:
                print("Invalid choice. Please enter a valid option.")

            # Gravar as alterações no arquivo
            if rewrite:
                with open('cfg.newGame.txt', 'w', encoding='utf-8') as cfg_file:
                    cfg_file.writelines(cfg_contents)

        except Exception as e:
            print(f"Error accessing or modifying the configuration file: {e}")

        time.sleep(0.8)


# Test the function
# config()


    
    
    
    
    
    
