import sys
from requests import ConnectionError, HTTPError, Session
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
from argparse import ArgumentParser


LANGUAGES = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese",
             "dutch", "polish", "portuguese", "romanian", "russian", "turkish"]

parser = ArgumentParser(description="Prints translations and examples of a given word",
                        usage="Enter all necessary arguments in the following order: [lang_from] [lang_to] [word]")

parser.add_argument('lang_from', type=str, help='Enter the language you want to translate from',
                    choices=LANGUAGES)
parser.add_argument('lang_to', type=str, help='Enter the language you want to translate to',
                    choices=[*LANGUAGES, 'all'])
parser.add_argument('word', type=str, help='Enter the word you want translated')

args = parser.parse_args()
lang_from = args.lang_from.lower()
lang_to = args.lang_to.lower()
word = args.word.lower()

if lang_from == lang_to:
    parser.error("Source and target language are the same.")

BASE_URL = 'https://context.reverso.net/translation/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
TRANSLATION_STRAINER = SoupStrainer('div', id="translations-content")
EXAMPLE_STRAINER = SoupStrainer('section', id='examples-content')

def get_soup(s: Session, l_from: str, l_to: str, w: str, ss: SoupStrainer):
    direction = l_from + '-' + l_to
    url = BASE_URL + direction + '/' + w
    return cook_a_soup(s, url, ss)


def cook_a_soup(s: Session, u: str, ss: SoupStrainer):
    try:
        with s.get(url=u, headers=HEADERS) as response:
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(
                markup=html,
                features='html.parser',
                parse_only=ss
            )
            return soup
    except ConnectionError:
        print(f'Something wrong with your internet connection')
        sys.exit()
    except HTTPError:
        print(f'Sorry, unable to find {u.rsplit("/", 1)[-1]}')
        sys.exit()       


def get_text_data(soup: BeautifulSoup, limit: int, tag: str, attr: dict = None):
    if attr:
        return [ch.text.strip() for ch in soup.find_all(tag, attr, limit=limit)]
    return [ch.text.strip() for ch in soup.find_all(tag, limit=limit)]


def log_output(log, lang, translations, examples):
    print(f'\n{lang.capitalize()} Translations:', *translations, sep="\n", file=log)
    print(f'\n{lang.capitalize()} Examples:', file=log)
    for x in range(0, len(examples), 2):
        print(examples[x], examples[x+1], sep='\n', end='\n\n', file=log)


def read_log(log):
    log.seek(0)
    for line in log:
        print(line, end='')


with Session() as session:
    with open(f'{word}.txt', 'w+', encoding='utf-8') as file:
        if lang_to == 'all':
            for lang_to in (lang for lang in LANGUAGES if lang != lang_from):
                trans_soup = get_soup(session, lang_from, lang_to, word, TRANSLATION_STRAINER)
                ex_soup = get_soup(session, lang_from, lang_to, word, EXAMPLE_STRAINER)
                trans_data = get_text_data(trans_soup, 1, 'a')
                ex_data = get_text_data(ex_soup, 2, 'span', {'class': 'text'})
                log_output(file, lang_to, trans_data, ex_data)
        else:
            trans_soup = get_soup(session, lang_from, lang_to, word, TRANSLATION_STRAINER)
            ex_soup = get_soup(session, lang_from, lang_to, word, EXAMPLE_STRAINER)
            trans_data = get_text_data(trans_soup, 5, 'a')
            ex_data = get_text_data(ex_soup, 10, 'span', {'class': 'text'})
            log_output(file, lang_to, trans_data, ex_data)
        read_log(file)