# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for letter in secret_word:
        if letter in letters_guessed:
            continue
        else:
            return False
            

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    out_word = ''
    for letter in secret_word:
        if letter in letters_guessed:
            out_word = out_word + letter
            continue
            return letter
        else:
            out_word = out_word + '_ '
            continue
            return '_ '
    return out_word

# secret_word = input("secret word: ")
# letters_guessed = input("letters guessed: ")
# print(get_guessed_word(secret_word, letters_guessed))



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    available_letters = ''
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters = available_letters + letter
            continue
            return letter
        else:
            continue
    return available_letters

# letters_guessed = input("letters guessed: ")
# print(get_available_letters(letters_guessed))
    
    
def check_guess(guess, letters_guessed, secret_word, guesses_remaining, warnings_remaining):
    """ 
    guess: char, user inputted
    letters_guessed: list (of letters), which letters have been guessed so far
    secret_word: string, the word the user is guessing
    guesses_remaining: int, amount of guesses left starting at 6
    warnings_remaining: int, amount of warnings left, starting at 3
    returns: letters_guessed, guesses_remaining, warnings_remaining so that 
    those are updated for further rounds
    
    """
    
        
    letters_guessed.append(guess)
    if guess in secret_word:
        print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
        
    else:
        print("Oops! That letter is not in my word.")
        print(get_guessed_word(secret_word, letters_guessed))
        
        if guess in ['a', 'e', 'i', 'o', 'u']:
            guesses_remaining = guesses_remaining - 2
        else:
            guesses_remaining = guesses_remaining - 1
           
            
    return letters_guessed, guesses_remaining, warnings_remaining
    
   
def check_is_valid_guess(guess, warnings_remaining, guesses_remaining,letters_guessed): 
    
    if guess not in string.ascii_lowercase:
          print("Oops! That is not a valid letter.")
          if warnings_remaining > 0:
              warnings_remaining = warnings_remaining - 1
          else:
              guesses_remaining = guesses_remaining - 1 
          print("You have", warnings_remaining, "warnings left")
          print(get_guessed_word(secret_word, letters_guessed))
          
          return False, warnings_remaining, guesses_remaining
          
    if guess in letters_guessed:
          print("Oops! You've already guessed that letter.")
          if warnings_remaining > 0:
              warnings_remaining = warnings_remaining - 1
          else:
              guesses_remaining = guesses_remaining - 1 
          print("You have", warnings_remaining, "warnings left")
          print(get_guessed_word(secret_word, letters_guessed))
          
          return False, warnings_remaining, guesses_remaining

    return True, warnings_remaining, guesses_remaining

def unique(secret_word):
    
    unique_letters = []
    for letter in secret_word:
        if letter not in unique_letters:
            unique_letters.append(letter) 
            
    return len(unique_letters)
        


def score(guesses_remaining, secret_word):
    """" 
    guesses_remaining: int, the number of guesses remaining
    secret_word: string, the word the user is guessing
    returns: user's score
    """
    score = guesses_remaining * unique(secret_word)
    return score
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    #initialize variables
    guesses_remaining = 6
    warnings_remaining = 3
    dashes = '----------'
    letters_guessed = []
    
    #welcome and let user know length of secret word
    length = len(secret_word)
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", length, "letters long.")
    print("You have", warnings_remaining, "warnings left.")
    
    # keep playing the game while the secret word isnt guessed and you have guesses remaining
    while (is_word_guessed(secret_word, letters_guessed) == False \
           and guesses_remaining != 0):
        # do this on each turn
        print(dashes)
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        guess_raw = input("Please guess a letter: ")
        guess = guess_raw.lower()
        
        is_valid_guess, warnings_remaining, guesses_remaining = check_is_valid_guess(
            guess, warnings_remaining, guesses_remaining,letters_guessed
            )
        
        if is_valid_guess:
            letters_guessed, guesses_remaining, warnings_remaining = check_guess(
                guess, letters_guessed, secret_word, guesses_remaining, warnings_remaining
                )
    
    if is_word_guessed(secret_word, letters_guessed) != False:
         print(dashes)
         print("Congratulations you won!")
         print("Your total score for this game is", score(guesses_remaining, secret_word))
   
    if guesses_remaining == 0:
        print(dashes)
        print("Sorry, you ran out of guesses. The word was", secret_word, ".")
       
    



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
        
    my_word_no_spaces = my_word.replace(' ', '')
    
    if len(my_word_no_spaces) != len(other_word):
        return False
        
    for i in range(len(my_word_no_spaces)):
        
        if my_word_no_spaces[i] == '_':
            continue
        elif my_word_no_spaces[i] == other_word[i]:
            continue
        else:
            return False

    return True
    
    
    




def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    matching_words= []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            print(word)
            matching_words.append(word)
    
    if len(matching_words) == 0:
        print('No Matches Found')
        
        
    


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    #initialize variables
    guesses_remaining = 6
    warnings_remaining = 3
    dashes = '----------'
    letters_guessed = []
    
    #welcome and let user know length of secret word
    length = len(secret_word)
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", length, "letters long.")
    print("You have", warnings_remaining, "warnings left.")
    
    # keep playing the game while the secret word isnt guessed and you have guesses remaining
    while (is_word_guessed(secret_word, letters_guessed) == False \
           and guesses_remaining > 0):
        # do this on each turn
        print(dashes)
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        guess_raw = input("Please guess a letter: ")
        guess = guess_raw.lower()
        
        if guess == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))    
            continue
        
        is_valid_guess, warnings_remaining, guesses_remaining = check_is_valid_guess(
            guess, warnings_remaining, guesses_remaining,letters_guessed
            )
        
        if is_valid_guess:
            letters_guessed, guesses_remaining, warnings_remaining = check_guess(
                guess, letters_guessed, secret_word, guesses_remaining, warnings_remaining
                )
    
    if is_word_guessed(secret_word, letters_guessed) != False:
         print(dashes)
         print("Congratulations you won!")
         print("Your total score for this game is", score(guesses_remaining, secret_word))
   
    if guesses_remaining <= 0:
        print(dashes)
        print("Sorry, you ran out of guesses. The word was", secret_word + ".")
       
    



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # # secret_word = 'apple'
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
