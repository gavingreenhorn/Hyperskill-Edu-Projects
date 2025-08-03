from string import punctuation

import pandas as pd
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from lxml import etree
from sklearn.feature_extraction.text import TfidfVectorizer

xml = etree.parse('news.xml')
root = xml.getroot()
corpus = root[0]
lemmatizer = WordNetLemmatizer()
filter_tokens = list(punctuation) + stopwords.words('english')
vectorizer = TfidfVectorizer(input='content')

titles = []
texts = []

for story in corpus:
    title = story[0].text
    text = story[1].text.lower()
    tokens = word_tokenize(text)
    lemmas = list(map(lemmatizer.lemmatize, tokens))
    words = list(filter(lambda token: token not in filter_tokens, lemmas))
    titles.append(title)
    texts.append(' '.join(
        [word for word in words if pos_tag([word])[0][1] == 'NN']))

tfidf_matrix = vectorizer.fit_transform(texts)
vocabulary = vectorizer.get_feature_names_out()

for i, tfidf_vector in enumerate(tfidf_matrix.toarray()):
    scores = zip(vocabulary, tfidf_vector)
    most_freq = dict(sorted(scores, key=lambda x: (x[1], x[0]), reverse=True)[:5])
    print(f'{titles[i]}:\n', *most_freq.keys(), end='\n')
