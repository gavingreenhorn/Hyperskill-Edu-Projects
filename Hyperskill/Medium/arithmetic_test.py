from dataclasses import dataclass, field
from random import randint, choice
from typing import Union
import string
import operator


OPERATIONS = {
    '//':   operator.floordiv,
    '%':    operator.mod,
    '**':   operator.pow,
    '+':    operator.add,
    '-':    operator.sub,
    '*':    operator.mul,
    '/':    operator.truediv
}


@dataclass
class Calculator:
    operand_1: Union[int, float]
    operator: str
    operand_2: Union[int, float]
    
    def __post_init__(self):
        self.validator()
    
    def validator(self):
        try:
            self.operand_1 = float(self.operand_1) if '.' in self.operand_1 else int(self.operand_1)
            self.operand_2 = float(self.operand_2) if '.' in self.operand_2 else int(self.operand_2)
        except ValueError:
            return 'Please enter operands in numerical format'
        
    def run_operation(self):
        operation = OPERATIONS.get(self.operator)
        return operation(self.operand_1, self.operand_2)


@dataclass
class MathQuiz:
    
    @staticmethod
    def valid_input(inp):
        try:
            int(inp)
        except ValueError:
            return False
        else:
            return inp
            
    def run_calc(self):
        values = (str(randint(2, 9)), choice(list(OPERATIONS.keys())), str(randint(2, 9)))
        print(' '.join(values)) 
        calc = Calculator(*values)
        return calc.run_operation()
    
    def run_quiz(self):
        expect = self.run_calc()
        while not (answer := self.valid_input(input())):
            print('Incorrect format.')
        else:
            return expect == int(answer)

    
def main():
    entry_temp = string.Template('$name: $right/5}')
    right = 0
    quiz = MathQuiz()
    for i in range(5):
        if quiz.run_quiz():
            print('Right!')
            right += 1
        else:
            print('Wrong!')
    save = input(f'Your mark is {right}/5.'
                  'Would you like to save your result to the file? Enter yes or no.\n').lower()

    if save in {'yes', 'y'}:
        name = input('What is your name?\n')
        entry = entry_temp.substitute(name=name, right=right)
        with open('results.txt', 'a+', encoding='utf-8') as res:
            res.write(entry)
        print('The results are saved in "results.txt"')
            
if __name__ == '__main__':
    main()
