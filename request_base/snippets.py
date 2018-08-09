import csv
import pymorphy2
import nltk
import string
from nltk.corpus import stopwords


def word_tokenize(sentence):
    """take sentence, return list of normalized sentence words"""
    morph = pymorphy2.MorphAnalyzer()
    tokens = nltk.word_tokenize(str(sentence))
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])
    tokens = [morph.parse(i)[0].normal_form for i in tokens if (i not in stop_words) and (i not in string.punctuation)]
    return tokens


def get_data(filename1):
    """generator to yield csv row by row"""
    with open(filename1, encoding='Windows-1251') as f_csv:
        reader = csv.reader(f_csv, delimiter=';')
        for row in reader:
            yield (row)