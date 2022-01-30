from typing import ClassVar


class Markdown:
    cache: ClassVar[list] = []

    @classmethod
    def show_help(cls):
        return ('Available formatters: plain bold italic header link inline-code'
                'new-line ordered-list, unordered-list'
                '\nSpecial commands: !help !done')

    @classmethod
    def new_line(cls) -> None:
        cls.cache.append('\n')

    @classmethod
    def add_line(cls, line: str) -> None:
        cls.cache.append(line)

    @classmethod
    def save(cls) -> None:
        file = open('output.md', 'w', encoding='utf-8')
        file.writelines(cls.cache)
        file.close


class List(Markdown):

    def __init__(self, lines: list) -> None:
        self.lines = lines

    def add_lines(self) -> None:
        pass


class UnorderedL(List):

    def add_lines(self) -> None:
        for line in self.lines:
            entry = f'* {line}\n'
            super().add_line(entry)


class OrderedL(List):

    def add_lines(self) -> None:
        for i in range(len(self.lines)):
            entry = f'{i+1}. {self.lines[i]}\n'
            super().add_line(entry)


class Header(Markdown):

    def __init__(self, level: int, text: str) -> None:
        self.level = level
        self.text = text

    def add_line(self) -> None:
        entry = f'{"#" * self.level} {self.text}\n'
        super().add_line(entry)


class Link(Markdown):

    def __init__(self, label: str, url: str) -> None:
        self.label = label
        self.url = url

    def add_line(self) -> None:
        entry = f'[{self.label}]({self.url})'
        super().add_line(entry)


class Plain(Markdown):

    def __init__(self, line: str) -> None:
        self.line = line

    def add_line(self) -> None:
        super().add_line(self.line)


class Bold(Markdown):

    def __init__(self, line: str) -> None:
        self.line = line

    def add_line(self) -> None:
        entry = f'{"**"}{self.line}{"**"}'
        super().add_line(entry)


class Italic(Markdown):

    def __init__(self, line: str) -> None:
        self.line = line

    def add_line(self) -> None:
        entry = f'{"*"}{self.line}{"*"}'
        super().add_line(entry)


class InlineCode(Markdown):

    def __init__(self, line: str) -> None:
        self.line = line

    def add_line(self) -> None:
        entry = f'`{self.line}`'
        super().add_line(entry)


COMMANDS = {
    'plain': Plain,
    'ordered-list': OrderedL,
    'unordered-list': UnorderedL,
    'bold': Bold,
    'italic': Italic,
    'header': Header,
    'link': Link,
    'inline-code': InlineCode,
}

while (command := input('Choose a formatter: ')) != '!done':
    if command == '!help':
        print(Markdown.show_help())
        continue
    elif command == 'new-line':
        Markdown.new_line()
    elif command not in COMMANDS:
        print('Unknown formatting type or command')
        continue
    elif command in ('ordered-list', 'unordered-list'):
        while (n_of_lines := int(input('Number of rows: '))) <= 0:
            print('The number of rows should be greater than zero')
            continue
        lines = [input(f'Row #{x+1}: ') for x in range(n_of_lines)]
        a_list = COMMANDS.get(command)(lines)
        a_list.add_lines()
    elif command == 'header':
        while (level := int(input('Level: '))) not in range(1, 7):
            print('The level should be within the range of 1 to 6')
        text = input('Text: ')
        header = COMMANDS.get(command)(level, text)
        header.add_line()
    elif command == 'link':
        label = input('label: ')
        url = input('URL: ')
        link = COMMANDS.get(command)(label, url)
        link.add_line()
    else:
        text = input('Text: ')
        formatter = COMMANDS.get(command)(text)
        formatter.add_line()
    print("".join(Markdown.cache))
else:
    Markdown.save()
