#!/usr/local/bin/python3

'''
This program picks a word which would be appropriate to use in the game of Hangman. 
At present 10 or less letter long words are chosen in case of dictionary words. 
In case of a text file, any one word is randomly chosen. The users can choose 
between playing themselves or watch computer play. 
Computer picks letters randomly from list of alphabets, with the preset probablility 
of finding vowels and consonants 2:1. 
-Sriparna Majumdar
TA
(CS131A online class : Prof. Aaron Brick, Fall 2018)
'''
import re
import random
import sys
import time
from urllib.request import urlopen

# This function returns a word list from a text file or dictionary
def wordLetter(file):
    if not file.startswith("http"):
        with open(file, 'rt') as datafile:
            words = set([word.rstrip().lstrip() for word in datafile.split() if (len(word.rstrip().lstrip()) <= 10 
                                                                                 and len(word.rstrip().lstrip()) >= 2)])
            words_few = [word for word in words if re.search(r'[aeiou]+', word)]
    else:
        datafile = urlopen("http://hills.ccsf.edu/~abrick/urantia").read().decode()
        words_few = [word for word in set(datafile.split()) if (word.isalpha() and len(word) >= 2 and len(word) <= 10)]

    return (words_few)

# trying various sources of files for lookup here.
try:
    wordSet = wordLetter(sys.argv[1])

except FileNotFoundError:
    wordSet = wordLetter('/users/abrick/resources/english')

except:
    wordSet = wordLetter("http://hills.ccsf.edu/~abrick/urantia")

#############################################################################
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
VOWEL = 'aeiouy'

# this function finds the indices of a chosen letter in a random word
def findLettIndex(word, player, round):
    if player == 'Comp' and round == 1:
        letter = random.choice(list(VOWEL))
        time.sleep(0.5)
    elif player == 'Comp' and round > 1:
        letter = random.choice(list(ALPHABET + VOWEL))
        time.sleep(0.5)

    else: # user is playing
        letter = input('Guess a letter : ')
    getIndex = []
    word = word.lower()
    if letter in word:
        count1 = word.count(letter)
        word1 = word[:]
        for i in range(count1):
            getIndex.append(word1.find(letter) + i) # the word gets shortened by 1 in each loop (see next line).
            word1 = word1.replace(letter, "", 1)
    return (letter, getIndex)

###
### play the hangman game here:	
###

def printString(player):
    randWord = random.choice(wordSet) # pick the random word here.
    testword = "-" * len(randWord)
    lettList = []
    print("The hangman word is", len(randWord), "letters long.\n")
    for i in range(1, 9):
        print("Round #", i)
        temp, index1 = findLettIndex(randWord, player, i) # Try to guess a letter. 8 tries maximum
	
        while temp in lettList:
            print("  Randomly chosen letter: ", temp)
            print("  You repeated a letter. Try an unused letter.") # Always provide new letter
            temp, index1 = findLettIndex(randWord, player, i)
        letter, index = temp, index1
        lettList.append(letter)
	
        print("  Randomly chosen letter: ", letter)
        if index:
            word = list(testword)  
            for j in range(len(index)):
                word[index[j]] = letter
            testword = "".join(word)
            print('	Word is:', testword) # Newly constructed word with guessed letters is output here.
        else:
            print("	Wrong guess! Word is:", testword)

        if testword == randWord.lower():
            print("Wow! You guessed it in", i, "rounds!")
            break
    print('\nThe randomly chosen word was :', randWord, '\n')
		
# This is the start of the output
print("\nThis is the hangman game. Guess a word computer chose for you. \nYou guess one letter in each round; 8 rounds maximum.\n")
print("The computer can play hangman game. Enter \"yes\" for computer, \"I\" for you, \"no\" when exit.")

inp = input("Start? ")

while inp != "no":
    if inp == "yes" or inp == 'y':
        player = "Comp"
        
    else:
        player = "I"
    printString(player)
    inp = input('Play? (yes/I/no): ' )		




