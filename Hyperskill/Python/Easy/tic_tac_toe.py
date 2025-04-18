S = 5
BORDER = '-'*(S*2+3)


def get_winning_positions(input_matrix):
    win_combos = input_matrix.copy()                                    # create a list to store all possible winning positions 
                                                                        # (already contains all horizontal positions)
    for i in range(len(input_matrix)):
        win_combos.append([input_matrix[d][i] for d in range(S)])       # adding vertical positions
    win_combos.append([input_matrix[d][S-1-d] for d in range(0, S, 1)]) # diagonal upper-right to lower-left corner
    win_combos.append([input_matrix[d][d] for d in range(0, S, 1)])     # diagonal upper-left to lower-right corner
    return win_combos

def print_grid(matrix):
    print(BORDER)
    for x in matrix:
        formatted_row = " ".join(x)
        print(f'| {formatted_row} |')
    print(BORDER)
    
def win(win_combos, sign):
    combo = list(sign * S)
    if combo in win_combos:
        return True
    return False
           
def declare_results(win_combos, matrix):
    if win(win_combos, 'X'):
        return 'X wins'
    elif win(win_combos,'O'):
        return 'O wins'
    elif all(('X' in line and 'O' in line) for line in win_combos):
        return 'Draw'
    elif '_' not in [item for row in matrix for item in row]:
        return 'Draw'
            
def prompt_move():
    turn = 1
    while True:
        input_list = input('Enter the coordinates:').split()
        if len(input_list) > 1:
            x, y = input_list
            if not x.isdigit() or not y.isdigit():
                print('You should enter numbers!')
            elif int(x) not in range(1, S+1) or int(y) not in range(1, S+1):
                print('Coordinates should be from 1 to 3!')
            elif matrix[int(x) - 1][int(y) - 1] != "_":
                print('This cell is occupied! Choose another one!')
            else:
                matrix[int(x) - 1][int(y) - 1] = 'X' if turn % 2 != 0 else 'O'  # odd turn = 'X' and vice versa
                print_grid(matrix)                                              # reprint field after changes
                win_combos = get_winning_positions(matrix)                      # make changes to winning combinations
                if(results := declare_results(win_combos, matrix)):             # check if either win or draw conditions are met
                    print(results)
                    break
                turn = turn + 1
        else:
            print('You should enter two numbers!')

matrix = [list("_" * S) for _ in range(S)]
print_grid(matrix)                                                              # print an empty field
prompt_move()                                                                   # entry point