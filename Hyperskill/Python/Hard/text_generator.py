import os
import re
from random import choice, choices
from collections import Counter, defaultdict

import nltk


STOP_WORD_REGEX = re.compile(r".+[!?.]")
CAP_WORD_REGEX = re.compile(r"[A-Z]\S*")


def get_markov_chain(counter):
    markov = defaultdict(dict)
    for trigram, count in counter.items():
        *head, tail = trigram
        markov[tuple(head)][tail] = count
    return markov


def get_lead_head(chain):
    while True:
        head = choice(list(chain.keys()))
        if CAP_WORD_REGEX.match(head[0]) and not STOP_WORD_REGEX.match(head[0])\
        and not STOP_WORD_REGEX.match(head[1]):
            return head


def get_heaviest_tail(chain, head):
    tails = chain[head]
    return choices(
        list(tails.keys()),
        list(tails.values())
    )[0]


def get_random_sentence(chain, lead_head):
    word_list = [lead_head[0], lead_head[1]]
    head = lead_head
    count = 2
    while not STOP_WORD_REGEX.match(head[1]):
        head = (head[1], get_heaviest_tail(chain, head))
        word_list.append(head[1])
        count += 1
    return word_list


def get_random_text(chain, n_of_sentences, min_words):
    text_list = []
    for _ in range(n_of_sentences):
        while True:
            head = get_lead_head(chain)
            word_list = get_random_sentence(chain, head)
            if len(word_list) >= min_words:
                text_list.append(" ".join(word_list))
                break
    return text_list


def main():
    filename = input()
    path = os.path.join(os.getcwd(), filename)
    with open(path, "r", encoding="utf-8") as f:
        corpus = f.read()
    tokens = nltk.tokenize.regexp_tokenize(corpus, r"\S+")
    trigrams = nltk.trigrams(tokens)
    tri_counter = Counter(trigrams)
    markov_chain = get_markov_chain(tri_counter)
    sentences = get_random_text(markov_chain, 10, 5)

    print(*sentences, sep="\n")


if __name__ == '__main__':
    main()