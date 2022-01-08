memory = 0

def minus():
    return n1 - n2
def plus():
    return n1 + n2
def multi():
    return n1 * n2
def div():
    return n1 / n2

MESSAGES = {
    0: 'Enter an equation\n',
    1: "Yes ... an interesting math operation. You've slept through all classes, haven't you?",
    2: 'Do you even know what numbers are? Stay focused!',
    3: 'Yeah... division by zero. Smart move...',
    4: 'Do you want to store the result? (y / n):\n',
    5: 'Do you want to continue calculations? (y / n):\n',
    6: " ... lazy",
    7: " ... very lazy",
    8: " ... very, very lazy",
    9: "You are",
    10: "Are you sure? It is only one digit! (y / n)",
    11: "Don't be silly! It's just one number! Add to the memory? (y / n)",
    12: "Last chance! Do you really want to embarrass yourself? (y / n)"
}

OPERATIONS = {
    '+': plus,
    '-': minus,
    '*': multi,
    '/': div
}

def is_one_digit(v):
    return v in range(-9, 10) and str(v).split('.')[1] == '0'

def is_lazy(_n1, _n2, _oper):
    accusation = ''
    if is_one_digit(_n1) and is_one_digit(_n2):
        accusation += MESSAGES[6]
    if (_n1 == 1 or _n2 == 1) and _oper == '*':
        accusation += MESSAGES[7]
    if (_n1 == 0 or _n2 == 0) and _oper in '-+*':
        accusation += MESSAGES[8]
    if accusation != '':
        print(MESSAGES[9] + accusation)

def evaluate(_string):
    if _string != 'M':
        try:
            num = float(_string)
        except ValueError:
            return None
        else:
            return num
    else:
        return memory
    
while True:
    n1, oper, n2 = input(MESSAGES[0]).split()
    n1 = evaluate(n1)
    n2 = evaluate(n2)
    is_lazy(n1, n2, oper)
    if (n1 and n2) or (n1 and n2 == 0) or (n2 and n1 == 0):
        if oper in OPERATIONS.keys():
            operation = OPERATIONS.get(oper)
            try:
                result = operation()
            except ZeroDivisionError:
                print(MESSAGES[3])
            else:
                print(result)
                memory_prompt = ' '
                while memory_prompt not in 'yn':
                    memory_prompt = input(MESSAGES[4])
                if memory_prompt == 'y':                   
                    if is_one_digit(result):
                        msg_index = 10
                        stupid_prompt = ''
                        while msg_index < 13 and stupid_prompt != 'n':
                            stupid_prompt = input(MESSAGES[msg_index])
                            msg_index += 1
                        if stupid_prompt == 'y':
                            memory = result
                    else:
                        memory = result
                continue_prompt = ' '
                while continue_prompt not in 'yn':
                    continue_prompt = input(MESSAGES[5])
                if continue_prompt == 'n':
                    break                
        else:
            print(MESSAGES[1])
    else:
        print(MESSAGES[2])
