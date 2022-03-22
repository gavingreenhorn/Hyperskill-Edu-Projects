import hashlib
import os
import sys
import re
from argparse import ArgumentParser
from collections import defaultdict


class MyArgumentParser(ArgumentParser):
    def error(self, message):
        message = 'Directory is not specified'
        print(message)
        sys.exit()


parser = MyArgumentParser()
parser.add_argument('root', type=str)
args = parser.parse_args()

start_dir = args.root

help_message = """
Size sorting options:
1. Descending
2. Ascending
"""

duplicates_list = []


def get_file_sizes(root_dir, pattern):
    by_size = defaultdict(list)
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if pattern.match(f):
                path = os.path.join(root, f)
                md = hashlib.md5()
                with open(path, mode='rb') as fh:
                    md.update(fh.read())
                size = os.path.getsize(path)
                by_size[size].append((md.hexdigest(), path))
    return by_size


def get_hash_table(size_dict):
    by_hash = {}
    for k, v in size_dict.items():
        tmp = defaultdict(list)
        for hash_code, path in v:
            tmp[hash_code].append(path)
        by_hash[k] = tmp
    return get_duplicates(by_hash)


def get_duplicates(hash_table):
    dup_table = {}
    for size, files_data in hash_table.items():
        for hash_code, paths in files_data.items():
            if len(paths) > 1:
                tmp = defaultdict(list)
                for path in paths:
                    tmp[hash_code].append(path)
                if not dup_table.get(size):
                    dup_table[size] = tmp
                else:
                    dup_table[size].update(tmp)
    return dup_table


def enumerate_duplicates(size, paths, count_from):
    enumeration = enumerate(paths, count_from)
    for file_ref in enumeration:
        duplicates_list.append((size, *file_ref))
    return [f'{count}. {path}' for count, path in enumeration]


def printer(inp_dict, sort_option, print_hash=False):
    if not print_hash:
        for size, files_data in sorted(inp_dict.items(), reverse=sort_option):
            paths = [file[1] for file in files_data]
            print(f'{size} bytes', *paths, sep='\n')
    else:
        count_from = 1
        for size, files_data in sorted(inp_dict.items(), reverse=sort_option):
            print(f'\n{size} bytes')
            for hash_code, paths in files_data.items():
                print(f'Hash: {hash_code}', *enumerate_duplicates(size, paths, count_from), sep='\n')
                count_from += len(paths)


def remove_duplicates(duplicates, inp_nums):
    freed_total = 0
    if inp_nums:
        for size, num, path in duplicates:
            if num in inp_nums:
                freed_total += size
                os.remove(path)
    return freed_total


def prompt(text, options):
    while (inp := input(f'{text}\n')) not in options:
        print('Wrong option\n')
        continue
    else:
        return inp


format_inp = input('Enter file format:\n')
regex = re.compile(f'.+\\.{format_inp}')

print(help_message)
sort_inp = prompt('Enter a sorting option:', {'1', '2'})
reverse = True if sort_inp == '1' else False
size_dict = get_file_sizes(start_dir, regex)
printer(size_dict, reverse)
check_dup = prompt('Check for duplicates?', {'yes', 'no'})
if check_dup == 'yes':
    duplicates_table = get_hash_table(size_dict)
    printer(duplicates_table, reverse, print_hash=True)
    delete = prompt('Delete files?', {'yes', 'no'})
    if delete == 'yes':
        while True:
            try:
                nums = list(map(int, input('Enter file numbers to delete:\n').split()))
            except ValueError:
                print('Wrong option\n')
            else:
                if not (space := remove_duplicates(duplicates_list, nums)):
                    print('Wrong option\n')
                else:
                    print(f'Total freed up space: {space} bytes')
            break
