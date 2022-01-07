import random
from collections import Counter

numbers = list(range(7))
all_pieces = [[x, y] for y in range(7) for x in range(7) if x <= y ]    # generate all available domino pieces
head = []

while not head:                                                         # split pieces between stock, player and computer
        
    random.shuffle(all_pieces)
    stock_pieces = all_pieces[:14]
    player_pieces = all_pieces[14:21]
    computer_pieces = all_pieces[21:]
    
    for x in reversed(range(7)):                                        # select the highest piece and who goes first
        if 14 <= all_pieces.index([x, x]) < 21:
            head = [x, x]
            status = 'computer'
            player_pieces.remove([x, x])
            break
        elif 21 <= all_pieces.index([x, x]) < 28:
            head = [x, x]
            status = 'player'
            computer_pieces.remove([x, x])
            break

snake = [head]                                                          # set initial snake value to the heaviest piece

def print_current_state(_status_message):                               # print info about current state of the game
    snake_print = snake                                                 # and its result if draw/win conditions are reached
    if len(snake) > 6:
        snake_print = snake[:3] + snake[-3:]
    print(f"""
{'=' * 70}
Stock Size: {len(stock_pieces)}
Computer pieces: {len(computer_pieces)}

{format_snake(snake)}

Your pieces:
""")
    for x in range(len(player_pieces)):
        print(f'{x+1}:{player_pieces[x]}')    
    print_status(_status_message)

def print_status(_status_message):
    print ("\nStatus:", _status_message)

def format_snake(listlist):                                             # list representing snake is converted to string
    if len(listlist) > 6:                                               # displaying only 3 first and 3 last pieces
        snake_head = "".join([str(nest_list) for nest_list in listlist[:3]])
        snake_tail = "".join([str(nest_list) for nest_list in listlist[-3:]])
        return f'{snake_head}...{snake_tail}'
    return "".join([str(nest_list) for nest_list in listlist])
    
def is_valid(current_move, current_piece):          # check if a piece can be used as a head or tail of domino snake
    if current_move < 0:                            # and lay as such depending on the move sign
        if current_piece[1] == snake[0][0]:
            snake.insert(0, current_piece)
            return True
        elif current_piece[0] == snake[0][0]:
           current_piece.reverse()
           snake.insert(0, current_piece)
           return True
        else:
            return False
    else:
        if current_piece[0] == snake[-1][1]:
            snake.append(current_piece)
            return True
        elif current_piece[1] == snake[-1][1]:
           current_piece.reverse()
           snake.append(current_piece)
           return True
        else:
            return False

def has_options(side_list):                         # function used to determine if any side can proceed with current hand
    return any(is_valid(1, piece) or is_valid(-1, piece)  for piece in side_list)

def get_scores(nest_list):                          # creates a dict representing relative weight of each piece for "AI"
    full_list = snake + nest_list
    flat = [item for a_list in full_list for item in a_list]
    scored_items = {(flat.count(a_list[0]) + flat.count(a_list[1])): a_list  for a_list in nest_list}
    return scored_items

while len(computer_pieces) + len(player_pieces) >= 1:                   # conditions are checked here
    status_message = ("It's your turn to make a move. Enter your command." if status == 'player' else
        "Computer is about to make a move. Press Enter to continue...")
    if len(computer_pieces) == 0:
        status_message = "The game is over. The computer won!"
        print_current_state(status_message)
        break
    elif len(player_pieces) == 0:
        status_message = "The game is over. You won!"
        print_current_state(status_message)
        break
    elif len(stock_pieces) == 0 and not has_options(computer_pieces) and not has_options(player_pieces):        
        status_message = "The game is over. It's a draw!"
        print_current_state(status_message)
        break
    else:                                                               # all conditions checked, players' moves below
        print_current_state(status_message)
        if status == 'player':
            try:
                move = int(input())
            except ValueError:
                print('Invalid input. Please try again.')
            else:
                if move == 0:
                    if len(stock_pieces) > 0:
                        new_piece = stock_pieces.pop(random.randrange(len(stock_pieces)))
                        player_pieces.append(new_piece)
                        status = 'computer'
                    else:
                        status = 'computer'
                elif abs(move) <= len(player_pieces):
                    current_piece = player_pieces[abs(move) -1]
                    if is_valid(move, current_piece):
                        player_pieces.remove(current_piece)
                        status = 'computer'
                    else:
                        print('Illegal move. Please try again.')
                else:
                    print('Invalid input. Please try again.')
        else:
            input()
            scored_items = get_scores(computer_pieces)
            scored_sorted = {key: scored_items[key] for key in reversed(sorted(scored_items.keys())) }
            for current_piece in scored_sorted.values():
                if is_valid(1, current_piece) or is_valid(-1, current_piece):
                    computer_pieces.remove(current_piece)
                    status = 'player'
                    break             
            else:
                if len(stock_pieces) > 0:
                    new_piece = stock_pieces.pop(random.randrange(len(stock_pieces)))
                    computer_pieces.append(new_piece)
                    status = 'player'
                elif len(stock_pieces) == 0:
                    status = 'player'