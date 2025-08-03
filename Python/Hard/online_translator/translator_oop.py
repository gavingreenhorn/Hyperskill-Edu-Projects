import sys
from dataclasses import dataclass, field
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


@dataclass
class Translation:
    word: str
    examples: list
    translations: list

    def __post_init__(self):
        print(self.examples)
        print(self.translations)

    def log_output(self, log):
        print(f'\n{word} Translations:', *self.translations, sep="\n", file=log)
        print(f'\n{word} Examples:', file=log)
        for x in range(0, len(self.examples), 2):
            print(self.examples[x], self.examples[x+1], sep='\n', end='\n\n', file=log)

    def read_log(self, log):
        log.seek(0)
        for line in log:
            print(line, end='')


@dataclass
class Translator:
    lang_from: str
    lang_to: str
    word: str
    url_list: list = field(init=False)
    limit: int = field(init=False)
    translation: Translation = field(init=False)

    def __post_init__(self):
        if lang_to == 'all':
            self.url_list = [BASE_URL + self.lang_from + '-' + lang + '/' + self.word for lang in LANGUAGES if lang != self.lang_from]
            self.limit = 1
        else:
            self.url_list = [BASE_URL + self.lang_from + '-' + self.lang_to + '/' + self.word]
            self.limit = 5
        self.translation = self.web_query()

    def get_translation(self):
        self.translation = Translation(
            examples='',
            translation=''
        )

    def from_tag(self, soup: BeautifulSoup, tag: str, attr: dict = None):
        if attr:
            yield [ch.text.strip() for ch in soup.find_all(tag, attr, limit=self.limit * 2)]
        yield [ch.text.strip() for ch in soup.find_all(tag, limit=self.limit)]

    def cook_a_soup(self, html: str, ss: SoupStrainer, tag: str, attr: dict = None):
        soup = BeautifulSoup(
                    markup=html,
                    features='html.parser',
                    parse_only=ss
                )
        yield from self.from_tag(soup, tag, attr)

    def get_text_data(self, s: Session, u: str, ss: SoupStrainer, tag: str, attr: dict = None):
        try:
            with s.get(url=u, headers=HEADERS) as response:
                response.raise_for_status()
        except ConnectionError:
            print(f'Something wrong with your internet connection')
            sys.exit()
        except HTTPError:
            print(f'Sorry, unable to find {u.rsplit("/", 1)[-1]}')
            sys.exit()
        else:
            html = response.text
            yield from self.cook_a_soup(html, ss, tag, attr)

    def web_query(self):
        with Session() as session:
            translations: list = []
            examples: list = []
            for url in self.url_list:
                translations += self.get_text_data(session, url, TRANSLATION_STRAINER, 'a')
                examples += self.get_text_data(session, url, EXAMPLE_STRAINER, 'span', {'class': 'text'})         
            return Translation(self.word, translations, examples)

    def print_translation(self):
        with open(f'{self.word}.txt', 'w+', encoding='utf-8') as file:
            self.translation.log_output(file)
            self.translation.read_log(file)

translator = Translator(lang_from, lang_to, word)
translator.print_translation()