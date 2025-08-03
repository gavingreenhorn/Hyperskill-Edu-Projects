import string
import os

import requests
from dataclasses import dataclass, field
from typing import ClassVar

from bs4 import BeautifulSoup as beauty


@dataclass
class WebScraper:
    CACHE: ClassVar[dict] = dict()
    BASE_URL: ClassVar[str] = 'https://www.nature.com'
    PAGE_URL: ClassVar[str] = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
    page_number: int
    art_type: str
    raw_text: str = field(init=False)
    art_urls: dict = field(init=False)
    page_content: dict = field(init=False)

    @classmethod
    def save_content(cls):
        for page, articles in cls.CACHE.items():
            os.mkdir(page)
            for name, text in articles.items():
                path = os.path.join(page, f'{name}.txt')
                with open(path, 'wt', encoding='utf-8') as file:
                    file.write(text)

    def __post_init__(self):
        self.page_content = dict()
        url = self.PAGE_URL + f"&page{self.page_number}"
        self.raw_text = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'}).text
        self.art_urls = dict()
        self.parse_page()

    def parse_page(self):
        soup = beauty(self.raw_text, 'html.parser')
        articles = soup.find_all('article')
        for art in articles:
            span = art.find('span', {'class': 'c-meta__type'})
            if span.text == self.art_type:
                link = art.find('a')
                url = self.BASE_URL + link['href']
                self.art_urls[link.text] = url

    def parse_articles(self):
        for name, url in self.art_urls.items():
            r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup = beauty(r.text, 'html.parser')
            article = soup.find('div', {'class': 'c-article-body'})
            file_name = ''.join(ch if ch not in string.punctuation else '' for ch in name)
            file_name = file_name.replace(' ', '_')
            self.page_content[file_name] = article.get_text()

    def cache_content(self):
        self.CACHE[f'Page_{self.page_number}'] = self.page_content


n_of_pages = int(input())
art_type = input()

for page_num in range(1, n_of_pages + 1):
    scraper = WebScraper(page_num, art_type)
    scraper.parse_articles()
    scraper.cache_content()

WebScraper.save_content()
