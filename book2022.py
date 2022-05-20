'''
This program shows implementation of a book class.
Passing filepath as command line argument in sys.argv[1]:
python3 book.py /users/abrick/resources/urantia.txt
python3 book.py https://hills.ccsf.edu/~abrick/urantia.txt
Else first paragraph of urantia will be taken as book content.
'''
import re, sys

class Book():
  def __init__(self, *args): # path to local file or url to a web text
    self.name = args[0].split('/')[-1] if 'http' in args[0] else args[0]
    self.file = args[0]

    try:
      self.text = open(self.file, 'r').read()

    except FileNotFoundError:
      try:
        from urllib.request import urlopen
        self.text = urlopen(self.file).read().decode()

      except ValueError:

        print("No valid file path was passed, setting to default: first paragraph of urantia book.\n")
    
        self.name = "Urantia: First Paragraph"
      
        self.text = "\t\t0:0.1 IN THE MINDS of the mortals of Urantia -- that being the name of\n\
                   your world -- there exists great confusion respecting the meaning of such\n\
                   terms as God, divinity, and deity. Human beings are still more confused and\n\
                   uncertain about the relationships of the divine personalities designated by\n\
                   these numerous appellations. Because of this conceptual poverty associated\n\
                   with so much ideational confusion, I have been directed to formulate this\n\
                   introductory statement in explanation of the meanings which should be\n\
                   attached to certain word symbols as they may be hereinafter used in those\n\
                   papers which the Orvonton corps of truth revealers have been authorized to\n\
                   translate into the English language of Urantia.\n"


    self.author	= args[1] if args[1:] else "Unknown"
    self.language = args[2] if args[2:] else self.lang()
    self.genre = args[3] if args[3:] else "Unknown"
    self.type = "Digital"
    self.length = len(self.text.splitlines())

  def __repr__(self):
    return "\n ***This is a book class that instantiates with a text file found in local\n" + \
         " directory or on web. In absence of any valid filepath or url it sets the class\n" + \
         " with first paragraph of urantia book. Optional class properties can be set as\n" + \
         " arguments in this order: author, language, genre.The class provides methods\n" + \
         " like UniqueWords, UniqueNum, longestWord, largestNumber, randWord.***\n" + \
         "\nThis book is " + self.name + "\n"


  # A method to read book. Utilizes generator comprehension and facilitates bookmarking
  def displayBook(self, bookmark = 1): # bookmark a page
    print("\nPrinting the book here:\n")
    print("This is {}, written by {} in {} language. \nIt's of {} genre and is available as a {} book.\
    \n..Start of Content:\n".format(self.name, self.author, self.language, self.genre, self.type))
    assert (bookmark-1)*30 < self.length
    
    page = 30 # number of lines in one page
    count = 0 # Start at 1st line of 1st page
    inp = ''
    
    lines = (line for line in self.text.splitlines())
    # skip lines if bookmark provided
    while count < (bookmark-1)*30:
      next(lines)
      count += 1

    # Print pages
    while lines and not inp: 
      try:
        print(next(lines))
        count += 1 
        if not (count % page): # multiple of 30, end of page
          print("\n::End of page#", count//30) 
          inp = input("\nEnter to continue, 'q' to quit reading:")
      except StopIteration:
        print("End of Book.")
        break
       

  # Read book page by page
  def display(self, bookmark=1):
    lines = self.text.splitlines()

    while True:
      print(*lines[(bookmark-1)*30:bookmark*30], sep = '\n')
      print("\n::End of page#", bookmark)
      if bookmark*30 >= len(lines):
        print("End of Book.")
        break

      inp = input("\nEnter to continue, 'q' to quit reading:")
      if inp: 
        break
      else: 
        bookmark += 1


  # This function helps us determine if the text is written in english or not.
  def lang(self):
    eng_stop_words = ['is', 'am', 'are', 'was', 'were', 'will', 'shall', \
       'the', 'have', 'has', 'had', 'for', 'at', 'from', 'to', 'on', 'of']
    textlist = re.split(r'[\W\d]+', self.text.lower() if len(self.text) < 1000 else self.text[:1000].lower())
    lookup = {key: textlist.count(key) for key in eng_stop_words}
    return "English" if sum(lookup.values()) else "Non-English" 


  # This function extracts all words as a list and returns count of uniques.
  def UniqueWords(self): 
    self.wordlist = re.split("[\W\d]", self.text.lower())
    return len(set(self.wordlist))


  # This function extracts all numbers as a list and returns count of uniques.           
  def UniqueNum(self):
    # Floating point numbers and integers are extracted
    # Pick all numbers including punctuation in the end
    # Check https://en.wikipedia.org/wiki/Decimal_separator
    # Numbers can be 1.300.000,00, 1.842842682846783, 50,000,000, 2 393 Or 842 842 682 846 781st

    # First pick all numbers with findall and then split at punctuation + space
      # Gives '3.9 300,000,000,000', '50,000,000 842 842 682 846 781.21', '23 3.89'
        # Split at space that did not belong to a numeric string
        # Extract numbers as int or float 
    self.numlist = list()
    punc = ', ._'
    numbers = re.split('[,._][ ]+', ', '.join(re.findall(r'[, ._\d]+', self.text)))
    for num in numbers:
      num = num.strip(punc).replace('_', '')
      
      if num:
        idx = num.find(' ')
        temp1, temp2 = '', '' 
        if idx >= 0 and (not num[:idx].isnumeric()) or (not re.search('\d{3}[ .,]*', num[idx+1:])):
          temp1, temp2 = num[:idx].replace(' ', '').strip(punc), num[idx+1:].replace(' ', '').strip(punc)
        else:
          temp1 = num.replace(' ', '')

        try:
          if self.language == "English":
            temp1 = temp1.replace(',', '') 
            temp2 = temp2.replace(',', '') 
          else:
            temp1 = temp1.replace('.', '').replace(',', '.')
            temp2 = temp2.replace('.', '').replace(',', '.')

          self.numlist.append(float(temp1) if float(temp1) % 1 else int(temp1)) if temp1 else None
          self.numlist.append(float(temp2) if float(temp2) % 1 else int(temp2)) if temp2 else None
        except ValueError:
          continue
    return len(set(self.numlist))


  # This function returns longest word found in text
  def longestWord(self):
    return max(self.wordlist, key=len) if self.wordlist else None


  # This function returns largest number found in text
  def largestNum(self):
    return "{:,.2f}".format( round(max(self.numlist), 2) ) if self.numlist else None

  # This function returns a random number from text
  def randWord(self):
    from random import choice
    return choice(list(set(self.wordlist))) if self.wordlist else None


### Running the program with the class initialized. 
## Give url or filepath of a text file as command line argument, to be considered as a book.

if __name__ == '__main__':
  
  aBook = Book(*sys.argv[1:]) if sys.argv[1:] else Book(" ")
  print(aBook)
  aBook.displayBook(4401) if aBook.length > 4400 * 30 else aBook.displayBook() 
  
  #print last page
  aBook.display(aBook.length//30 + 1)

  print("Here are some statistics:")
  print("\nThis book contains", aBook.UniqueWords(), "unique words and", aBook.UniqueNum(), "unique numerics")
  print("out of", len(aBook.wordlist), "total words and", len(aBook.numlist), "total numerics.")
  print("Longest Word:", aBook.longestWord())
  print("Largest Number:", aBook.largestNum())
  print("A random word:", aBook.randWord())

