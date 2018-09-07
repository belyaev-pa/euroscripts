import time
import csv
import openpyxl
import pymorphy2
import nltk
import string
from nltk.corpus import stopwords
from functools import lru_cache, wraps
from .models import *



class Namespace: pass
ns = Namespace()
ns.processed_id = []
ns.output_list = []
ns.phrase_to_update = []


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


@lru_cache(maxsize=2)
def get_tag_list(filename):
    """get list of tags and words from xlsx file
    [['tag', list], ['tag', list],...]       """
    wb = openpyxl.load_workbook(filename)
    first_sheet = wb.sheetnames[0]
    worksheet = wb[first_sheet]
    output_list = list()
    for row in range(1, worksheet.max_row+1):
        phrase_cell = "{}{}".format('A', row)
        tag_cell = "{}{}".format('B', row)
        phrase = worksheet[phrase_cell].value
        tag = worksheet[tag_cell].value
        item = list()
        item.append(phrase)
        item.append(tag)
        item.append(word_tokenize(phrase))
        output_list.append(item)
    print('get_tag_list - ended')
    return sorted(output_list, key = lambda s: len(s[1]), reverse=True)



def timer(f):
#    @wraps()
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print("f time - {} {}".format(str(time.time()-t), f.__name__, ))
        return res
    return tmp


def recursion_sort(phrase, number, level):
    ns.output_list.append([phrase.phrase, phrase.phrase_len, level+str(number)+'.'])
    ns.processed_id.append(phrase.id)
    ns.phrase_to_update.append((phrase.id, level+str(number)))
    phrase_word_list = phrase.link_set.values_list('word_id', flat=True)
    phrase_in_phrase = Phrase.objects.filter(
        phrase_len=phrase.phrase_len+1).exclude(
        pk__in=ns.processed_id).order_by('phrase_len', '-frequency')
    for word in phrase_word_list:
        phrase_in_phrase = phrase_in_phrase.filter(link__word=word)
    for i, item in enumerate(phrase_in_phrase, 1):
        recursion_sort(item, i, level+str(number)+'.')
    return 0