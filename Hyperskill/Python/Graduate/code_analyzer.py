import os
import re
import ast
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path


parser = ArgumentParser()
parser.add_argument('path', nargs='?')
args = parser.parse_args()


class NodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = {}

    @dataclass
    class FuncStat:
        name: str
        arguments: list
        defaults: list
        assignments: list

    def visit_FunctionDef(self, node):
        name = node.name
        arguments = [a.arg for a in node.args.args]
        defaults = [d for d in node.args.defaults]
        assignments = []
        for child in node.body:
            if isinstance(child, ast.Assign):
                for v in child.targets:
                    if hasattr(v, "id"):
                        assignments.append((v.id, v.lineno))
        self.generic_visit(node)
        self.functions[node.lineno] = self.FuncStat(
            name, arguments, defaults, assignments)


class Linter:
    ERROR_MESSAGE = '{path}: Line {line_number}: {code} {description}'
    ERRORS = {
        's001': 'Too long',
        's002': 'Indentation is not a multiple of four',
        's003': 'Unnecessary semicolon',
        's004': 'At least two spaces required before inline comments',
        's005': 'TODO found',
        's006': 'More than two blank lines used before this line',
        's007': 'Too many spaces after \'{construction}\'',
        's008': 'Class name \'{name}\' should use CamelCase',
        's009': 'Function name \'{name}\' should use snake_case',
        's010': 'Argument name \'{argument}\' should be snake_case',
        's011': 'Variable \'{variable}\' in function should be snake_case',
        's012': 'Default argument value is mutable'
    }
    CONSTRUCTION_PATTERN = re.compile(r'\s*\w+\b \S+')
    CLASS_NAME_PATTERN = re.compile(r'([A-Z]|([A-Z][a-z]+)+)$')
    FUNCTION_NAME_PATTERN = re.compile(r'[a-z_]')

    @staticmethod
    def read_file(file):
        content = file.read()
        code = dict(enumerate(content.split('\n'), start=1))
        tree = ast.parse(content)
        return tree, code

    def print_error(self, line_nb, code, description):
        print(
            self.ERROR_MESSAGE.format(
                  path=self.path,
                  line_number=line_nb,
                  code=code.capitalize(),
                  description=description
            )
        )

    def s001(self, line_nb, line, code, *arg):
        if len(line) > 79:
            self.print_error(
                line_nb, code, self.ERRORS[code])

    def s002(self, line_nb, line, code, *arg):
        if not line.startswith(' '):
            pass
        elif (len(line) - len(line.lstrip())) % 4:
            self.print_error(
                line_nb, code, self.ERRORS[code])

    def s003(self, line_nb, line, code, *arg):
        if ';' not in line:
            pass
        elif line.startswith('#'):
            pass
        elif not bool(re.match(r'.*[\"\'].*;.*[\'\"]|.*#.*;', line)):
            self.print_error(
                line_nb, code, self.ERRORS[code])

    def s004(self, line_nb, line, code, *arg):
        if '#' not in line:
            pass
        elif not re.match(r'.* {2,}#|^#', line):
            self.print_error(
                line_nb, code, self.ERRORS[code])

    def s005(self, line_nb, line, code, *arg):
        if '#' not in line:
            pass
        elif bool(re.search(r'todo', line, re.IGNORECASE)):
            self.print_error(
                line_nb, code, self.ERRORS[code])

    def s006(self, line_nb, line, code, *arg):
        if not line or line_nb < 4:
            return
        preceding = map(
            lambda x: x.strip(),
            list(self.code.values())[line_nb-4:line_nb-1])
        if not sum(map(len, preceding)):
            self.print_error(
                line_nb, code, self.ERRORS[code])

    def s007(self, line_nb, line, code, *arg):
        if match := re.match(r'\s*(?P<construction>(class|def)).*\b', line):
            construction = match.group('construction')
            if not self.CONSTRUCTION_PATTERN.match(line):
                self.print_error(
                    line_nb, code,
                    self.ERRORS[code].format(
                        construction=construction)
                )

    def s008(self, line_nb, line, code, *arg):
        if match := re.match(r'class (?P<name>\w+)', line):
            name = match.group('name')
            if not self.CLASS_NAME_PATTERN.match(name):
                self.print_error(
                    line_nb, code,
                    self.ERRORS[code].format(name=name)
                )

    def s009(self, line_nb, line, code, *arg):
        if line_nb in self.visitor.functions:
            name = self.visitor.functions[line_nb].name
            if not self.FUNCTION_NAME_PATTERN.match(name):
                self.print_error(
                    line_nb, code,
                    self.ERRORS[code].format(name=name)
                )

    def s010(self, line_nb, line, code, *arg):
        if line_nb in self.visitor.functions:
            for name in self.visitor.functions[line_nb].arguments:
                if not re.match(r'[a-z_]+', name):
                    self.print_error(
                        line_nb, code,
                        self.ERRORS[code].format(argument=name))

    def s011(self, line_nb, line, code, *arg):
        if line_nb in self.visitor.functions:
            if self.visitor.functions[line_nb].assignments:
                for name, line in self.visitor.functions[line_nb].assignments:
                    if not re.match(r'[a-z_]+', name):
                        self.print_error(
                            line, code,
                            self.ERRORS[code].format(variable=name))

    def s012(self, line_nb, line, code, *arg):
        if line_nb in self.visitor.functions:
            for default in self.visitor.functions[line_nb].defaults:
                if isinstance(default, ast.List):
                    self.print_error(
                        line_nb, code, self.ERRORS[code])

    def __init__(self, file):
        self.path = file.name
        self.visitor = NodeAnalyzer()
        self.tree, self.code = self.read_file(file)

    def run(self):
        self.visitor.visit(self.tree)
        for line_number, line in self.code.items():
            for code in self.ERRORS:
                func = getattr(self, code)
                func(line_number, line, code)


def main():
    path = Path(args.path)
    if not path.exists():
        print(f'No file or directory found at {args.path}')
        return
    if path.is_file():
        with path.open() as file:
            linter = Linter(file)
            linter.run()
            return
    for obj in Path(path).iterdir():
        if obj.is_file():
            with obj.open() as file:
                linter = Linter(file)
                linter.run()


if __name__ == '__main__':
    main()
