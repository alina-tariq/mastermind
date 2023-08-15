from enum import Enum
import time 
import inquirer
from helper import *

class Circle(Enum):
    '''
        for each valid guess value holds the ansi escape and unicode characters
        for the corresponding coloured circle to print to the cli
    '''
    r = '\033[38;5;196m\u2B24\033[0m '
    o = '\033[38;5;202m\u2B24\033[0m '
    y = '\033[38;5;214m\u2B24\033[0m '
    g = '\033[38;5;29m\u2B24\033[0m '
    b = '\033[38;5;27m\u2B24\033[0m '
    i = '\033[38;5;63m\u2B24\033[0m '
    v = '\033[38;5;135m\u2B24\033[0m '
    u = ''

if __name__ == '__main__':

    # greeting 
    greeting = "Welcome to Mastermind! \n\nMastermind is a code-breaking game where you must use logic\nand strategy to figure out the computer\'s secret code. \n"
    
    # rules

    # prompt for selecting a level
    question = [
        inquirer.List('size',
                message="Choose a level: ",
                choices=['EASY', 'MEDIUM', 'HARD'],
                carousel=True
            ),
    ]

    valid_chars = 'roygbiv'  
    code_str = ''
    guess = ''  
    guesses = []  
    clues = []  
    prompt = "Please enter your guess: "
    tries = 0

    time.sleep(0.5)

    print(" _________________________________________________________")
    print("|  __  __           _                      _           _  |")
    print("| |  \/  | __ _ ___| |_ ___ _ __ _ __ ___ (_)_ __   __| | |")
    print("| | |\/| |/ _` / __| __/ _ \ '__| '_ ` _ \| | '_ \ / _` | |")
    print("| | |  | | (_| \__ \ ||  __/ |  | | | | | | | | | | (_| | |")
    print("| |_|  |_|\__,_|___/\__\___|_|  |_| |_| |_|_|_| |_|\__,_| |")
    print("|_________________________________________________________|\n")

    time.sleep(0.5)

    for char in greeting:
        print(char, end='', flush=True)
        time.sleep(0.025)

    time.sleep(0.75)

    print('___________________________________________________________\n')

    time.sleep(0.75)
    print('The rules of the game are simple.\n')
    time.sleep(0.75)
    print('1. The only characters the code will contain are: R, O, Y,\nG, B, I, V.\n')
    print('2. In order to win, you must determine which character(s)\nappear in the code as well as their exact position in a\nfinite number of tries.\n')
    print('3. Each character can appear in the code 0, 1, or 1+ times.\n')
    print('4. You are provided with clues for each guess. A \'\033[38;5;236m\u2B24\033[0m \' means')
    print('that one of the characters in your guess is present in the')
    print('code and is in its correct position. A \'\033[38;5;231m\u2B24\033[0m \' as a clue means')
    print('that one of the charactersin your guess is present in the\ncode but is in the incorrect position.\n')
    time.sleep(0.75)

    level = inquirer.prompt(question)["size"]

    match level:
        case 'EASY':
            size = 4
            maxTries = 10
            response = "EASY\nHmph. Why not try a real challenge for once?"
        case 'MEDIUM':
            size = 6
            maxTries = 15
            response = "MEDIUM\nFair enough. I respect that."
        case 'HARD':
            size = 8
            maxTries = 20
            response = "HARD\nPrepare to be destroyed."
        case default:
            size = 4
            maxTries = 10
            response = "EASY\nWhy not try a real challenge for once?"

    print("You have chosen level: " + response)

    print('___________________________________________________________\n')

    code = create_code(valid_chars, size)

    for item in code:
        code_str = code_str + str(item)

    print('The computer has chosen a ' + str(size) + '-letter code.')
    print('You will have ' + str(maxTries) + ' tries to guess the code.\n')

    guess = input(prompt)
    guess = guess.lower()
    print(' ')

    while guess != code_str and tries < maxTries:

        guess_str = ''  
        clue_str = ''  
        guess_list = [] 
        blacks = []  
        whites = []

        for char in guess:
            # adds each guess character to a list for comparison
            guess_list.append(char)

        # valid guesses are checked against code

        if valid(guess_list, valid_chars, size):

            for char in guess:
                guess_str += Circle[char].value

            tries += 1  # keeps track of all the tries

            blacks = (find_fully_correct(code, guess_list))

            # adds the 'b' clues to the clue string

            for item in blacks:
                clue_str += '\033[38;5;236m\u2B24\033[0m '

            whites = (find_colour_correct(code, guess_list))

            # adds the 'w' clues to the clue string

            for item in whites:
                clue_str += '\033[38;5;231m\u2B24\033[0m '

            guesses.append(guess_str)  # adds each guess to the master list
            clues.append(clue_str)  # adds the clues to the master list

            print_game(guesses, clues)  # prints the list of guesses and clues

            if tries < maxTries:
                guess = input(prompt)
                guess = guess.lower()
                print(" ")
        else: # prompts user again if guess is invalid
            guess = input(prompt)
            guess = guess.lower()
            print(" ")

    if tries >= maxTries:
        print("HAHA! You lose! The correct code was " + code_str + ".")
    elif guess == code_str:
        print("Well...congratulations I suppose. It took you " + str(tries+1), end='')
        print(" guesses to find the code.\n")