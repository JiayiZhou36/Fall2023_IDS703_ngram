"""
Markov Text Generator.

Jiayi Zhou, 2023
"""
import random


def unigram(corpus):
    """Unigram--list frequency of full corpus"""
    dict_words = {}
    for i in corpus:
        if i in dict_words:
            # if corpus words alread in dictionary, increase count
            dict_words[i] += 1
        else:
            # not in dictionary, creat key and value
            dict_words[i] = 1
    return dict_words


def multigram(sentence, n, corpus):
    """More than unigram---match sentence with corpus"""
    dict_words = {}
    for i in range(len(corpus) + n - 1):
        # compare sentence and corpus
        if sentence[-n + 1 :] == corpus[i : i + n - 1]:
            # if corpus words alread in dictionary, increase count
            if corpus[i + n - 1] in dict_words:
                dict_words[corpus[i + n - 1]] += 1
            else:
                # not in dictionary, creat key and value
                dict_words[corpus[i + n - 1]] = 1
    return dict_words


def backoff(sentence, n, corpus):
    """studpid backoff"""
    dict_words = {}
    # when sentence is empty
    if len(sentence) == 0:
        dict_words = unigram(corpus)
    else:
        # when sentence is not empty
        if n > 1:
            # when n is larger than 1
            dict_words = multigram(sentence, n, corpus)
            while len(dict_words) == 0:
                if n == 2:
                    # stupid backoff go to unigram
                    dict_words = unigram(corpus)
                else:
                    # stupid backoff go to multigram
                    n = n - 1
                    dict_words = multigram(sentence, n, corpus)
        else:
            # when n is equal to 1
            dict_words = unigram(corpus)
    return dict_words


def select_next(sentence, n, corpus, randomize):
    """Add one word for sentence"""
    dict_words = backoff(sentence, n, corpus)
    if not randomize:
        # deterministic
        sentence.append(max(dict_words, key=dict_words.get))
        return sentence
    else:
        # stochastic
        keys = list(dict_words.keys())
        values = list(dict_words.values())
        sentence.append(random.choices(keys, weights=values)[0])
        return sentence


def finish_sentence(sentence, n, corpus, randomize=False):
    """Generate in a sentense"""
    punc_list = [".", "?", "!"]
    # when sentence is empty
    if len(sentence) == 0:
        select_next(sentence, n, corpus, randomize)
    # when sentence is no empty
    while (sentence[-1] not in punc_list) and len(sentence) < 10:
        select_next(sentence, n, corpus, randomize)
    return sentence
