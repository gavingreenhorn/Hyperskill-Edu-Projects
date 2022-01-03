matrix = [list("_" * 3) for x in range(3)]
win_combos = list()

def get_winning_positions(input_matrix):
    win_combos = input_matrix.copy()                                    # create a list to store all possible winning positions 
                                                                        # (already contains all horizontal positions)
    for i in range(len(input_matrix)):
        win_combos.append([input_matrix[d][i] for d in range(3)])       # adding vertical positions
    win_combos.append([input_matrix[d][2-d] for d in range(0, 3, 1)])   # diagonal upper-right to lower-left corner
    win_combos.append([input_matrix[d][d] for d in range(0, 3, 1)])     # diagonal upper-left to lower-right corner
    return win_combos

def print_grid(matrix):                                                 # print the field
    print('---------')
    for x in matrix:
        formatted_row = " ".join(x)
        print(f'| {formatted_row} |')
    print('---------')
    
def win(sign):                                                          # check if there're 'XXX' or 'OOO' rows in win_combos
    combo = list(sign * 3)
    if combo in win_combos:
        return True
    else:
        return False
           
def declare_results(matrix):                                            # check conditions and return results
    if win('X'):
        print('X wins')
        return True
    elif win('O'):
        print('O wins')
        return True
    elif '_' not in [item for row in matrix for item in row]:           # flatten matrix and see if it contains an empty cell
        print('Draw')
        return True
            
def prompt_move():                                                      # iterate until declare_results returns true
    turn = 1
    while True:
        input_list = input('Enter the coordinates:').split()            # ask for coordinates
        if len(input_list) > 1:
            move_x, move_y = input_list
            if not move_x.isdigit() or not move_y.isdigit():
                print('You should enter numbers!')
            elif int(move_x) not in range(1,4) or int(move_y) not in range(1,4):
                print('Coordinates should be from 1 to 3!')
            elif matrix[int(move_x) - 1][int(move_y) - 1] != "_":
                print('This cell is occupied! Choose another one!')
            else:
                matrix[int(move_x) - 1][int(move_y) - 1] = 'X' if turn % 2 != 0 else 'O' # odd turn = 'X' and vice versa
                print_grid(matrix)                                      # reprint field after changes
                global win_combos
                win_combos = get_winning_positions(matrix)              # make changes to winning combinations
                if(declare_results(matrix)):
                    break
                turn = turn + 1
        else:
            print('You should enter two numbers!')
        
print_grid(matrix)                                                      # print an empty field
prompt_move()                                                           # entry