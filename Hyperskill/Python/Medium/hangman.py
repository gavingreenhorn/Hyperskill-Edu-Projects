from random import choice
from string import ascii_lowercase as LOWERCASE


def play():
    lives = 8
    guessed_set = set()
    display_word = '-' * len(secret_chosen)
    while lives > 0 and display_word != secret_chosen:
        print(f'\n{display_word}')
        letter = input('Input a letter: ')
        if len(letter) != 1:
            print('You should input a single letter')
            continue
        elif letter not in LOWERCASE:
            print('Please enter a lowercase English letter')
            continue
        elif letter in guessed_set:
            print("You've already guessed this letter")
            continue
        elif letter in secret_set:
            display_word = ''.join(x if x == letter else '-' for x in secret_chosen)
            guessed_set.add(letter)
        else:
            print("That letter doesn't appear in the word")
            guessed_set.add(letter)
            lives -= 1
    else:
        print('You guessed the word!\nYou survived!' if lives > 0 else 'You lost!')


SECRET_WORDS = 'python', 'java', 'kotlin', 'javascript'
secret_chosen = choice(SECRET_WORDS)
secret_set = set(secret_chosen)

print('H A N G M A N')
while True:
	selection = input('Type "play" to play the game, "exit" to quit: ')
	if selection == 'play':
		play()
	elif selection == 'exit':
		break
