import os
import requests
from argparse import ArgumentParser
from collections import deque

from bs4 import BeautifulSoup, SoupStrainer


parser = ArgumentParser()
parser.add_argument('dir', type=str, help='Enter path to the saves folder', default=os.getcwd())

args = parser.parse_args()

path = args.dir
os.makedirs(path, os.F_OK, exist_ok=True)


TAGS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
STRAINER = SoupStrainer(TAGS)


def get_html(u):
    r = requests.get(u)
    if not r:
        raise Exception(f'Http {r.status_code}')
    return r.text


def write_cached_page(fp, h):
    with open(fp, 'w', encoding='utf-8') as file:
        bs = BeautifulSoup(h, features='html.parser', parse_only=STRAINER)
        print(bs.get_text(), file=file)


def read_cached_page(fp):
    with open(fp, 'r', encoding='utf-8') as file:
        print(*file.readlines())


def cache_lookup(p, f, dn):
    fullpath = os.path.join(p, f)
    if os.access(fullpath, os.R_OK):
        read_cached_page(fullpath)
    else:
        uri = 'http://' + dn
        html = get_html(uri)
        write_cached_page(fullpath, html)
        read_cached_page(fullpath)


stack = deque()
last_page = None

while (inp := input()) != 'exit':
    if inp == 'back':
        if not stack:
            print('No cached pages')
            continue
        filename, dn = stack.pop()
        cache_lookup(path, filename, dn)
    elif '.' in inp:
        filename = inp.rsplit('.', 1)[0]
        if last_page:
            stack.append(last_page)
        last_page = filename, inp
        cache_lookup(path, filename, inp)
    else:
        print('Error: Incorrect URL')
