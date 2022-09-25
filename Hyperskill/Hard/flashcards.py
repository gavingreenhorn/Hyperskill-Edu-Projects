import os.path
from dataclasses import dataclass
from collections import defaultdict
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--import_from', type=str)
parser.add_argument('--export_to', type=str)

args = parser.parse_args()


@dataclass
class Flashcard:
    term: str
    definition: str
    
    
class Game:
    SAVE_MSG = '{0} cards have been saved.\n'
    LOAD_MSG = '{0} cards have been loaded.\n'
    HARDEST_ONE = 'The hardest card is "{0}". You have {1} errors answering it.\n'
    HARDEST_MUL = 'The hardest cards are {0}\n'
    ADD_SUCCESS = 'The pair "{0}":"{1}" has been added.\n'
    NO_TERM = 'Can\'t remove "{0}": there is no such card.\n'
    ANSWER_PROMPT = 'Print the definition of "{0}":\n'
    WRONG_ANSWER = 'Wrong. The right answer is "{0}".'
    DUP_TERM = 'The term "{0}" already exists. Try again:\n'
    DUP_DEFINITION = 'The definition "{0}" already exists. Try again:\n'
    KNOWN_DEFINITION = 'Wrong. The right answer is "{0}", ' \
                       'but your definition is correct for "{1}"'

    cards = []
    log = []
    errors = defaultdict(int)
    
    @property
    def terms(self):
        return (obj.term for obj in self.cards)
        
    @property
    def definitions(self):
        return {
            obj.definition: obj.term
            for obj in self.cards}

    def print(self, string):
        self.log.append(string)
        print(string)

    def input(self, string):
        self.log.append(string)
        return input(string)

    def _add(self):
        term = self.input('The card:\n')
        while term in self.terms:
            term = self.input(self.DUP_TERM.format(term))
        definition = self.input('The definition of the card:\n')
        while definition in self.definitions:
            definition = self.input(self.DUP_DEFINITION.format(definition))
        self.cards.append(Flashcard(term, definition))
        self.print(self.ADD_SUCCESS.format(term, definition))

    def _remove(self):
        if (term := self.input('Which card?\n')) not in self.terms:
            self.print(self.NO_TERM.format(term))
            return
        self.cards.remove(
            next(filter(lambda c: c.term == term, self.cards)))
        self.print('The card has been removed.\n')

    def _export(self):
        name = self.input('File name:\n')
        self._save(name)

    def _save(self, name):
        with open(name, 'w') as file:
            file.writelines(
                (f'{card.term},{card.definition}\n' for card in self.cards))
        self.print(self.SAVE_MSG.format(len(self.cards)))

    def _import(self):
        name = self.input('File name:\n')
        self._load(name)

    def _load(self, name):
        if not os.path.exists(name):
            self.print(f'File {name} not found.\n')
            return
        with open(name, 'r') as file:
            cards = file.readlines()
            for term, definition in (
                    card.rstrip().split(',') for card in cards):
                if term not in self.terms:
                    self.cards.append(Flashcard(term, definition))
                    continue
                card = next(filter(lambda c: c.term == term, self.cards))
                card.definition = definition
            self.print(self.LOAD_MSG.format(len(cards)))

    def _ask(self):
        if len(self.cards):
            for i in range(int(self.input('How many times to ask?\n'))):
                card = self.cards[i % len(self.cards)]
                answer = self.input(self.ANSWER_PROMPT.format(card.term))
                if answer == card.definition:
                    self.print('Correct!')
                elif answer in self.definitions:
                    self.errors[card.term] += 1
                    self.print(self.KNOWN_DEFINITION.format(
                        card.definition, self.definitions[answer]))
                else:
                    self.errors[card.term] += 1
                    self.print(self.WRONG_ANSWER.format(card.definition))
        else:
            self.print('No cards in program memory, add some to continue.')

    def _log(self):
        name = self.input('File name:\n')
        with open(name, 'w') as file:
            file.writelines(self.log)
        self.print('The log has been saved.')

    def _hardest(self):
        hardest = list(filter(
            lambda x: x[1] == max(self.errors.values()), self.errors.items()))
        if not hardest:
            self.print('There are no cards with errors.')
        elif len(hardest) > 1:
            cards = ', '.join((f'"{cards[0]}"' for cards in hardest))
            self.print(self.HARDEST_MUL.format(cards))
        else:
            term, count = hardest[0]
            self.print(self.HARDEST_ONE.format(term, count))

    def _reset(self):
        self.errors.clear()
        self.print('Card statistics have been reset.')

    def get_action(self, action):
        if action not in ('add', 'remove', 'import', 'export', 'ask',
                          'exit', 'log', 'hardest card', 'reset stats'):
            self.print('No such action available.')
        if ' ' in action:
            action = action.split()[0]
        getattr(self, '_' + action)()

    def play(self, options):
        if options.import_from:
            self._load(options.import_from)
        while (inp := self.input(
            'Input the action (add, remove, import, export, ask, '
            'exit, log, hardest card, reset stats):\n'
        )) != 'exit':
            self.get_action(inp)
        else:
            if options.export_to:
                self._save(options.export_to)
            else:
                self.print('Bye bye!')


if __name__ == '__main__':
    game = Game()
    game.play(args)
