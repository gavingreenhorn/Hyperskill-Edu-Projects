from random import choice
import os.path


OPTIONS = ['rock', 'gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'paper',
           'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors', 'fire']
           
ordered_options = {OPTIONS[x]: OPTIONS[x+1:] + OPTIONS[:x] for x in range(len(OPTIONS)) }
beats = {x: ordered_options[x][:len(ordered_options[x]) // 2] for x in ordered_options }
           
           
def set_input_valid(set_input):
    default_set = {'rock', 'paper', 'scissors'}
    if not set_input:
        return default_set
    elif len(set_input.split(',')) < 3:
        return default_set
    return set(set_input.split(','))


def declare(p_move, c_move):
    global user_rating
    if p_move == c_move:
        user_rating += 50
        print(f'There is a draw ({p_move})')
    elif c_move in beats[p_move]:
        print(f'Sorry, but the computer chose {c_move}')
    else:
        user_rating += 100
        print(f'Well done. The computer chose {c_move} and failed')

      
def get_rating(username):
    rating = 0
    if os.path.exists('rating.txt'):
        with open('rating.txt', 'r') as rat_file:
            ratings = rat_file.readlines()
            for line in ratings:
                if username in line:
                    rating = int(line.split()[1])
    return rating


user_name = input('Enter your name: ')
user_rating = get_rating(user_name)

print(f'Hello, {user_name}')

play_set = set_input_valid(input('Enter the playable set: '))
   
print("Okay, let's start")

while (p := input('Your move: ')) != '!exit':
    if p == '!rating':
        print(user_rating)
        continue
    elif p not in play_set:
        print('Invalid input')
        continue
    c = choice(list(play_set))
    declare(p, c)
else:
    with open('rating.txt', 'a+') as rat_file:
        print(user_name, user_rating, file=rat_file)
    print('Bye!')
