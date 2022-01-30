from typing import ClassVar


class Markdown:
    markdown_cache: ClassVar[list] = []

    @classmethod
    def show_help():
        print('Available formatters: plain bold italic header link inline-code'
              'new-line ordered-list, unordered-list'
              '\nSpecial commands: !help !done')

    @classmethod
    def new_line(cls) -> None:
        cls.markdown_cache.append('\n')

    def add_line(line: str) -> None:
        __class__.markdown_cache.append(line)


class List(Markdown):

    def __init__(self, lines: str) -> None:
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

    def add_line(self, line: str) -> None:
        entry = f'{"*"}{self.line}{"*"}'
        super().add_line(entry)


class InlineCode(Markdown):

    def __init__(self, line: str) -> None:
        self.line = line

    def add_line(self) -> None:
        entry = f'`{self.line}`'
        super().add_line(entry)


COMMANDS = {
    '!help': Markdown,
    'plain': Plain,
    'new-line': Markdown,
    'ordered-list': OrderedL,
    'unordered-list': UnorderedL,
    'bold': Bold,
    'italic': Italic,
    'header': Header,
    'link': Link,
    'inline-code': InlineCode,
}

while (command := input('Choose a formatter: ')) != '!done':
    if command not in COMMANDS:
        print('Unknown formatting type or command')
        continue
    if command in ('ordered-list', 'unordered-list'):
        while (n_of_lines := int(input('Number of rows: '))) < 0:
            continue
        lines = [input(f'Row #{x+1}: ') for x in range(n_of_lines)]
        a_list = COMMANDS.get(command)(lines)
        a_list.add_lines()
    elif command == 'new-line':
        Markdown.new_line()
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
    print("".join(Markdown.markdown_cache))
