"""
Regex engine educational project.

Supports . | ? | * | + | ^ | $ metacharacters.

If the script is being run as __main__
regex pattern and text string are separated by "|" in user input.

Input Examples:

    > '3\+3|3+3=6'
    # True
    > '^apple$|apple pie'
    # False
"""

import sys
from argparse import ArgumentParser


parser = ArgumentParser('Supply regex pattern and text string to be matched match')
parser.add_argument('-p', '--pattern', type=str)
parser.add_argument('-t', '--text', type=str)
args, flags = parser.parse_known_args()


class NonStringInputError(ValueError):
    def __init__(self, **kwargs):
        kwargs_str = '\n'.join(f'{k}: {type(v)}' for k, v in kwargs.items())
        self.message = f'Arguments of incorrect type supplied:\n{kwargs_str}'
        super().__init__(self.message)
 

def match(regex, string):
    """match characters in input pattern and string one by one recursively"""
    if not regex:
        return True
    elif not string:
        return False
    elif regex[0] == '\\':
        return literal_match(regex, string)
    elif '?' in regex[1:] and regex[1] == '?':
        return rep_zero_to_once(regex, string)
    elif '*' in regex[1:] and regex[1] == '*':
        return rep_zero_to_many(regex, string)
    elif '+' in regex[1:] and regex[1] == '+':
        return rep_once_to_many(regex, string)
    elif regex and regex[0] in {'?', '*', '+'}:
        return match(regex[1:], string)  # slice off meaningless metacharacters
    elif regex[0] in ('.', string[0]):
        return match(regex[1:], string[1:])
    return False


def literal_match(regex, string):
    """matches literal characters when escape sequence is encountered"""
    if len(regex) == 1:
        return match(regex[1:], string)
    elif regex[:2] == '\\\\' and string[0] == '\\':
        return match(regex[2:], string[1:])
    return match(regex[1:], string[1:])


def rep_zero_to_once(regex, string):
    """regex pattern's first character may appear once or zero times"""
    if regex[0] not in (string[0]):
        return match(regex[2:], string)
    return match(regex[2:], string[1:])


def rep_zero_to_many(regex, string):
    """regex pattern's first character may appear zero or multiple times"""
    if regex[0] not in (string[0], '.'):
        return match(regex[2], string)
    elif regex[-1] == '*' and len(string) == 1:
        return True
    elif regex[:2] == '.*' and regex[-1] == string[0]:
        return True
    return match(regex, string[1:])


def rep_once_to_many(regex, string):
    """regex pattern's first character may appear once or multiple times"""
    if regex[0] not in (string[0], '.'):
        return False
    elif len(regex) - len(string) == 1:
        return match(regex[:1] + regex[2:], string)
    return match(regex, string[1:])


def bounded_match(regex, string):
    """regex pattern is only searched at the beginning or at the end of a string"""
    if regex[0] == '^' and regex[-1] == '$':
        res = match(regex[1:-1], string)
        if res and len(regex) - 2 == len(string):
            return True
        elif res and {'*', '?', '+'} & set(regex):
            return True
        return False
    elif regex[0] == '^':
        return match(regex[1:], string[:len(regex) - 1])
    elif regex[-1] == '$':
        return match(regex[:-1], string[-len(regex) + 1:])


def regex_engine(regex, string):
    """
    Engine's main recursive function

    Iterates over input string until a match is found
    Consumes first character of the string each recursive call

    @param regex: searched pattern
    @param string: string the pattern is searched in
    @return: return boolean value

    >>> regex_engine('3\+3', '3+3=6')
    True
    >>> regex_engine('^apple$', 'apple pie')
    False
    >>> regex_engine(5, 5)
    Traceback (most recent call last):
    __name__.NonStringInputError
    """
    if not isinstance(regex, str) and not isinstance(string, str):
        raise NonStringInputError(pattern=regex, text=string)
    if not regex:
        return True
    elif not string:
        return False
    elif regex[0] == '^' or regex[-1] == '$':
        return bounded_match(regex, string)
    elif match(regex, string):
        return True
    return regex_engine(regex, string[1:])
    

def main():
    if args.pattern and args.text:
        r, s = args.pattern, args.text
    else:
        r, s = input('Enter pattern|text to match: \n').split('|')
    print(regex_engine(r, s))


sys.setrecursionlimit(10000)

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL) # exhaustive tests are implemented via unittest ./test_regex.py
    main()
