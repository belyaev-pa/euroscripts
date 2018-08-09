import pymorphy2
import nltk
import string
from nltk.corpus import stopwords


def word_tokenize(sentence):
    morph = pymorphy2.MorphAnalyzer()
    tokens = nltk.word_tokenize(str(sentence))
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])
    tokens = [morph.parse(i)[0].normal_form for i in tokens if (i not in stop_words) and (i not in string.punctuation)]
    return tokens