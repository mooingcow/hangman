#==LIBRARIES==
import random
import os
import sys

#==HANGMAN IMAGES==
HANGMANPICS = ['''

 +---+
 |   |
     |
     |
     |
     |
=========

''', '''

 +---+
 |   |
 O   |
     |
     |
     |
=========

''', '''

 +---+
 |   |
 O   |
 |   |
     |
     |
=========

''', '''

 +---+
 |   |
 O   |
/|   |
     |
     |
=========

''', '''

 +---+
 |   |
 O   |
/|\  |
     |
     |
=========

''', '''

 +---+
 |   |
 O   |
/|\  |
/    |
     |
=========

''', '''

 +---+
 |   |
 O   |
/|\  |
/ \  |
     |
=========

''']

#==FUNCTIONS==
#clear command line
def clearconsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

#'Press ENTER to continue' prompt
def cont():
    cont = False
    while(not(cont)):
        conttext = input("\nPress ENTER to continue")
        if(conttext == ""):
            cont = True
    clearconsole()

#shows current hangman picture, number of incorrect guesses, and current blanks
def displayBoard(HANGMANPICS, missedLetters, correctLetters, myWord):
    print(HANGMANPICS[len(missedLetters)])
    print("You've taken", len(missedLetters), "incorrect guesses.")   
    for letter in missedLetters:
        print(letter)
    blanks = '_' * len(myWord)
    for i in range(len(myWord)):
        if(myWord[i] in correctLetters):
            blanks = blanks[:i] + myWord[i] + blanks[i+1:]
    print()
    print(blanks)

#gets user's guess
def getGuess(alreadyGuessedLetters):
    while True:
        guess = input("\nGuess a letter\n>>> ")
        guess = guess.lower()
        if(len(guess) != 1):
            print("<Please enter a single letter>")
        elif(guess not in "abcdefghijklmnopqrstuvwxyz"):
            print("<Please enter a letter in the alphabet>")
        elif(guess in alreadyGuessedLetters):
            print("<You already guessed this letter>")
        else:
            return guess

#gets random word from selected word list
def getRandomWord(words):
    myWord = words[random.randint(0, len(words))]
    return(myWord)

#==LISTS OF WORDS==
words = []
easywords = ["dog", "clam", "tree", "peak", "mochi", "forest"]
mediumwords = ["ravioli", "concert", "theatre", "dinosaur", "backpack", "baseball"]
hardwords = ["buildings", "signature", "projector", "lightning", "spaghetti", "washington"]

#==MAIN PROGRAM LOGIC==
while(True):
    #PLAYERID
    clearconsole()
    print("\n---------------------------------------")
    print("----------------HANGMAN----------------")
    print("---------------------------------------")
    print("\nWelcome to Hangman\n\nPlease select your preferred option:\n1. Create PlayerID\n2. Scoreboard\n0. Exit")
    playerchoice = input(">>> ")
    while(not(str(playerchoice).isnumeric()) or int(playerchoice) < 0 or int(playerchoice) > 2):
        print("\nInvalid!")
        playerchoice = input(">>> ")
    playerchoice = int(playerchoice)

    #1. Create PlayerID
    if(playerchoice == 1):
        clearconsole()
        playerid = input("Enter your PlayerID\n>>> ")

        sessionpoints = 0
        while(True):
            #MAIN MENU
            clearconsole()
            print("\n---------------------------------------")
            print("----------------HANGMAN----------------")
            print("---------------------------------------")
            print("\nWelcome to Hangman\n\nPlease select your preferred option:\n1. Play\n0. Exit")
            hangmanchoice = input(">>> ")
            while(not(str(hangmanchoice).isnumeric()) or int(hangmanchoice) < 0 or int(hangmanchoice) > 1):
                print("\nInvalid!")
                hangmanchoice = input(">>> ")
            hangmanchoice = int(hangmanchoice)

            #1. PLAY
            if(hangmanchoice == 1):
                #DIFFICULTY MENU
                clearconsole()
                print("\n------------------------------------------")
                print("----------------DIFFICULTY----------------")
                print("------------------------------------------")
                print("\nChoose your difficulty\n\nPlease select your preferred option:\n1. Easy (6 or less letters)\n2. Medium (7-8 letters)\n3. Hard (9-10 letters)")
                difficultychoice = input(">>> ")
                while(not(str(difficultychoice).isnumeric()) or int(difficultychoice) < 1 or int(difficultychoice) > 3):
                    print("\nInvalid!")
                    difficultychoice = input(">>> ")
                difficultychoice = int(difficultychoice)
                
                #select word list based on difficulty
                if(difficultychoice == 1):
                    words = easywords
                elif(difficultychoice == 2):
                    words = mediumwords
                elif(difficultychoice == 3):
                    words = hardwords
                clearconsole()
                #variables
                correctLetters = []
                missedLetters = []

                #intro message
                print("Hello, let's play Hangman!!")
                cont()
                #get random word from selected word list
                myWord = getRandomWord(words)
                #guessing loop
                while(True):
                    clearconsole()
                    displayBoard(HANGMANPICS, missedLetters, correctLetters, myWord)
                    guess = getGuess(correctLetters+missedLetters)
                    #user guesses correct letter
                    if(guess in myWord):
                        correctLetters.append(guess)
                        #check whether user has guessed all the letters
                        win = True
                        for i in range(len(myWord)):
                            if(myWord[i] not in correctLetters):
                                win = False
                                break
                        #if user guesses the whole word
                        if(win):
                            print("\nYayyyyy you've guessed the word " + myWord)
                            sessionpoints += len(myWord)
                            print("----------------")
                            print("Total Points:", sessionpoints)
                            cont()
                            break
                    #user guesses incorrect letter
                    else:
                        missedLetters.append(guess)
                        #user runs out of guesses
                        if (len(HANGMANPICS) - 1) == len(missedLetters):
                            clearconsole()
                            displayBoard(HANGMANPICS, missedLetters, correctLetters, myWord)
                            print("\nYou've lost!!")
                            print("The word is", myWord)
                            cont()
                            break

            #0. EXIT
            else:
                print("\nThank You!\n")
                #read txt file
                fn = open('./scoreboard.txt','r')
                scoreboard = fn.read()
                scoreboard = scoreboard.split('\n') #[playerid|score, playerid|score]
                fn.close()
                #split by '|' - [[playerid, score], [playerid, score]]
                scoreboardlist = []
                for i in scoreboard:
                    if(i != ""):
                        i = i.split('|')
                        i[1] = int(i[1])
                        scoreboardlist.append(i)
                #get index current user's score
                for j in range(len(scoreboardlist)):
                    if(scoreboardlist[j][1] <= sessionpoints):
                        pointindex = j
                        break
                #to be written into scoreboard.txt
                newscoreboardlist = []
                for k in range(len(scoreboardlist)):
                    if(k == pointindex):
                        newscoreboardlist.append([playerid, sessionpoints])
                        newscoreboardlist.append([scoreboardlist[k][0], scoreboardlist[k][1]])
                    else:
                        newscoreboardlist.append([scoreboardlist[k][0], scoreboardlist[k][1]])
                scoreboardwrite = ""
                for m in newscoreboardlist:
                    scoreboardwrite += m[0] + "|" + str(m[1]) + "\n"
                #write into scoreboard.txt
                fn = open("./scoreboard.txt", "w")
                fn.write(scoreboardwrite)
                fn.close()
                cont()
                break
    
    #2. Scoreboard
    elif(playerchoice == 2):
        #read txt file
        fn = open('./scoreboard.txt','r')
        scoreboard = fn.read()
        scoreboard = scoreboard.split('\n')
        fn.close()
        #print scoreboard
        scoreboardlist = []
        for i in scoreboard:
            if(not(i == '')):
                i = i.split('|')
                i[1] = int(i[1])
                scoreboardlist.append(i)
        clearconsole()
        print("\n---------------------------------------")
        print("----------------RESULTS----------------")
        print("---------------------------------------")
        print("\nPlayerID : Points\n-----------------")
        counter = 0
        while(counter < 5 and counter < len(scoreboardlist)):
            print(str(counter + 1) + '. ' + scoreboardlist[counter][0] + " : " + str(scoreboardlist[counter][1]))
            counter += 1
        cont()
    
    #0. Exit
    else:
        print("\nThank You!\n")
        sys.exit(0)