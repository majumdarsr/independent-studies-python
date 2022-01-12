'''
Passing filepath as command line argument in sys.argv[1]:
python3 book.py /users/abrick/resources/urantia.txt
python3 book.py https://hills.ccsf.edu/~abrick/urantia.txt
Else first paragraph of urantia will be taken as book content.
'''
import re, sys

class Book():
  def __init__(self, txtfile): # txtfile is path to local file or url to a web text
    self.name = txtfile.split('/')[-1] if 'http' in txtfile else txtfile
    self.file = txtfile

    try:
      self.text = open(self.file, 'r').read()

    except FileNotFoundError:
      try:
        from urllib.request import urlopen
        self.text = urlopen(self.file).read().decode()

      except ValueError:
        print("No valid file path was passed, setting to default: first paragraph of urantia book.\n")
    
        self.name = "Urantia: First Paragraph"
      
        self.text = "0:0.1 IN THE MINDS of the mortals of Urantia -- that being the name of\
                   your world -- there exists great confusion respecting the meaning of such\
                   terms as God, divinity, and deity. Human beings are still more confused and\
                   uncertain about the relationships of the divine personalities designated by\
                   these numerous appellations. Because of this conceptual poverty associated\
                   with so much ideational confusion, I have been directed to formulate this\
                   introductory statement in explanation of the meanings which should be\
                   attached to certain word symbols as they may be hereinafter used in those\
                   papers which the Orvonton corps of truth revealers have been authorized to\
                   translate into the English language of Urantia."



  def __repr__(self):
    return "\n ***This is a book class that instantiates with a text file found in local\n" + \
         " directory or on web. In absence of any valid filepath or url it takes\n" + \
         " the first paragraph of urantia book. The class provides methods like\n" + \
         " UniqueWords, UniqueNum, longestWord, largestNumber, randWord.***\n" + \
         "\nThis is " + self.name + "\n"

  def UniqueWords(self): 
    words = re.split("[\W]", self.text.lower())
    self.wordlist = [word for word in words if (word and word.isalpha())]
    return len(set(self.wordlist))

           
  def UniqueNum(self): # Floating point numbers and integers are extracted
    numbers = re.split("[^\d.]", self.text.replace(',', ''))
    self.numlist = []
   
    for num in numbers:
      try:
        self.numlist.append(float(num))
      except ValueError:
        continue
    
    return len(set(self.numlist))


  def longestWord(self):
    return max(self.wordlist, key=len) if self.wordlist else None


  def largestNum(self):
    return "{:,.2f}".format( round(max(self.numlist), 2) ) if self.numlist else None


  def randWord(self):
    from random import choice
    return choice(self.wordlist) if self.wordlist else None


### Running the program with the class initiated. 
## Give url or filepath of a text file as command line argument, to be considered as a book.

aBook = Book(sys.argv[1]) if sys.argv[1:] else Book(" ")

print(aBook, "\nThis book contains", aBook.UniqueWords(), "unique words and", aBook.UniqueNum(), "unique numerics")
print("out of", len(aBook.wordlist), "total words and", len(aBook.numlist), "total numerics.")
print("Longest Word:", aBook.longestWord())
print("Largest Number:", aBook.largestNum())
print("A random word:", aBook.randWord())


