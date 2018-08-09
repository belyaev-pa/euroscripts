import csv
import openpyxl
import pymorphy2
import nltk
import string
from nltk.corpus import stopwords
from functools import lru_cache


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


@lru_cache(maxsize=4)
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
        item.append(tag)
        item.append(word_tokenize(phrase))
        output_list.append(item)
    return sorted(output_list, key = lambda s: len(s[1]), reverse=True)

