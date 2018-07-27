# Twistedteam SoC Week 2 hackathon solution 
# Team Members: 
# import stuff. Do I put this stuff at the top? I'm used to doing that in C...
import urllib.request  #need this to read the dictionary from the web
import random  #need this to generate random numbers for the board generation
import math #need to sqrt() the dice lists to figure out the size of the board.
import time #need this to have time functions for the timers

#Dice distributions. I might have to make this all into one object somehow later. I'm not good at OOP yet...
# old4by4 = [['A','A','C','I','O','T'],
#            ['A','H','M','O','R','S'],
#            ['E','G','K','L','U','Y'],
#            ['A','B','I','L','T','Y'],
#            ['A','C','D','E','M','P'],
#            ['E','G','I','N','T','V'],
#            ['G','I','L','R','U','W'],
#            ['E','L','P','S','T','U'],
#            ['D','E','N','O','S','W'],
#            ['A','C','E','L','R','S'],
#            ['A','B','J','M','O','Qu'],
#            ['E','E','F','H','I','Y'],
#            ['E','H','I','N','P','S'],
#            ['D','K','N','O','T','U'],
#            ['A','D','E','N','V','Z'],
#            ['B','I','F','O','R','X']]
new4by4 = [['A','A','E','E','G','N'],
           ['E','L','R','T','T','Y'],
           ['A','O','O','T','T','W'],
           ['A','B','B','J','O','O'],
           ['E','H','R','T','V','W'],
           ['C','I','M','O','T','U'],
           ['D','I','S','T','T','Y'],
           ['E','I','O','S','S','T'],
           ['D','E','L','R','V','Y'],
           ['A','C','H','O','P','S'],
           ['H','I','M','N','Qu','U'],
           ['E','E','I','N','S','U'],
           ['E','E','G','H','N','W'],
           ['A','F','F','K','P','S'],
           ['H','L','N','N','R','Z'],
           ['D','E','I','L','R','X']]

#Defines what dice are next to each other
NEIGHBORS = [(-1, -1), (0, -1), (1, -1),
             (-1, 0),          (1, 0),
             (-1, 1), (0, 1),  (1, 1)]

def generate_board(dice):
    #function to generate the board
    #start with a blank board
    board = []
    #figure out what size the board is by how many dice we have
    boardsize = int(math.sqrt(len(dice)))

    #for loops for the grid of the board
    for x in range(0,boardsize):
        board.append([])
        for y in range(0,boardsize):
            #pick a random die out of the dice list
            dicepick = random.randint(0, len(dice)-1)
            #make sure we haven't used that die already, otherwise roll again
            while(dice[dicepick] == "rolled"):
                dicepick = random.randint(0, len(dice)-1)
            #roll the die & put its letter in the board
            board[x].append(dice[dicepick][random.randint(0,5)])
            #mark this die as used
            dice[dicepick] = "rolled"
                
    #returns a list of lists that is the boggle board
    return board

def print_board(board):
    #function to print the board. Just for us to see it, mostly.
    for row in board:
        for letter in row:
            print(letter, end = "\t")
        print("\n")

def setup_dictionary():
    #function to get the dictionary as a set.
    dictionary = set()
    
    #getting the text file from the website
    try: 
        website = urllib.request.urlopen('https://raw.githubusercontent.com/jonbcard/scrabble-bot/master/src/dictionary.txt')
        raw = website.read()
        dictionaryraw = raw.decode("utf8") #decoding into proper text because .read() returns a byte thingie
    except:
        print('Dictionary error.')
        
    #making the dictionary into a set because it will check faster than a string
    dictionarystring = dictionaryraw.split("\n") #splitting the raw dictionary into lines
    for word in dictionarystring:
        dictionary.add(word)
        
    #returning the dictionary as a set DON'T TRY TO PRINT IT OMG!
    return dictionary
        
#def find_words(dictionary, board): #########THIS IS WHAT NEEDS DOING########
    #function for finding words.
    #Takes a set that is the dictionary and a list of lists that is the board
#    words = []
    
    #returns a list of words that it found on that board
#    return words

def count_score(words):
    #Takes the list of found words found on the board and calculates score
    #this function is actually done, I think, because it's pretty short so I just wrote it
    score = 0
    for w in words:
        score = score + len(w) - 2
    #returns an integer for score
    return score

# Function to solve the board and find all the words

def solve(my_board):

    # competiton time initalization
    start_time = time.time()
    #list for the results
    results = []
    #time check to finish loading 
    print ("Finished loading dictionary: %f" % (time.time() - start_time))
    #find the prefix set of possible words and with a tree for letter prefixes
    prefix_set = set(word[:i] for word in my_dictionary for i in range (1, len(word) +1))
    #print ("Finished loading prefix set: %f" % (time.time() - start_time))
    #For each letter in the grid x and y
    for y in range(len(my_board)):
        for x in range(len(my_board[y])):
            #Finding the words that occur recursive function 
            results += find_words(my_board,my_dictionary,prefix_set,
                                  my_board[y][x], y, x, set([(y, x)]))                              
    print ("finished finding words: %f" % (time.time() - start_time))
    #Return set of all lwords found
    return set(results)

#Function to find if a word is in the word list
def find_words(board, dictionary, prefix_set, current, y, x, used):
    #Initalize list of found words
    found = []
    if current not in prefix_set:
        return found
    #If word found put it in the list of found words    
    if current in dictionary:
        found.append(current)
    #For every neighbor letter    
    for dy, dx in NEIGHBORS:
        ny, nx = y + dy, x +dx 
        #Find words until we have used up neighbors
        if on_board(board, ny, nx) and (ny, nx) not in used:
            used.add((ny, nx))
            #keep doing it till we find all the words
            found.extend(find_words(board, dictionary, prefix_set,
                                    current+board[ny][nx], ny, nx, used))
            #remove used letters
            used.remove((ny, nx))
    #return set of found words        
    return list(set(found))

#Returns true if letter is on the board, false if it isn't
def on_board(board, y, x):
    return y >= 0 and x >= 0 and y < len(board) and x < len(board[y])

#calling all the functions to make all the things happen
my_board = generate_board(new4by4)
print_board(my_board)
my_dictionary = setup_dictionary()
my_words = solve(my_board)
my_score = count_score(my_words)

#this is the result they asked for, but I'm not sure what to do with it?
result = { "score" : my_score,
           "words" : my_words }

# print results out so that we can see the found words and score
print ("\nWords Found: " + str(my_words))
print ("\nFinal score: "  + str(my_score))
