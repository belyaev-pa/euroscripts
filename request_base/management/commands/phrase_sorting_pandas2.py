import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import *
from ...snippets import timer
import time
import pandas as pd
from memory_profiler import profile



class Command(BaseCommand):
    """сортировка списка фраз по хитрой Гришиной схеме (аля граф)"""
    #global variables
    df = pd.DataFrame(columns=settings.PANDAS_COLUMNS)
    output_list = []
    phrase_to_update = []
    #settings
    csv_output_file = settings.PHRASE_SORT_OUTPUT_ROOT
    memory_profiler_log = settings.MEMORY_PROFILE_LOG
    fp = open(memory_profiler_log, 'w+')
    @profile(stream=fp)
    @timer
    def handle(self, *args, **kwargs):
        t = time.time()
        print("start - {}".format(str(time.time() - t)))
        number = 1
        one_word_phrase_list = self.get_phrase_list()
        for phrase, word in one_word_phrase_list:
            print(phrase)
            self.get_phrase_with_phrase(word)
            first = self.df.head(1)
            self.recursion_sort(first, 1, number, '')
            number += 1

        # while not ns.df.empty:
        #     first = ns.df.head(1)
        #     recursion_sort2(first, 1, number, '')
        #     print('Итерация № {} , я работаю уже: {} с.'.format(number, str(time.time() - t)))
        #     number += 1
        with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for obj in self.output_list:
                word_writer.writerow([obj[0], obj[1], obj[2], obj[3]])
        print('csv write completed')
        # phrase_list = Phrase.objects.all()
        # for obj in ns.phrase_to_update:
        #     phrase_list.filter(pk=obj[0]).update(sort=obj[1])
        print('phrase update completed')

    @timer
    @profile(stream=fp)
    def get_phrase_list(self):
        result = list(Link.objects.filter(phrase__phrase_len=1
                                 ).order_by('-phrase__frequency'
                                 )[:3].values_list('phrase__phrase', 'word__word'))
        return result

    @timer
    @profile(stream=fp)
    def get_phrase_with_phrase(self, word):
        l = list(Link.objects.filter(phrase__phrase_len__gte=1
                            ).filter(word__word=word
                            ).values_list('phrase__phrase', 'word__word', 'phrase__phrase_len',
                                          'phrase__frequency', 'phrase__id'))
        self.df = pd.DataFrame(l, columns=settings.PANDAS_COLUMNS)
        self.df = self.df.sort_values(by=['phrase_len', 'frequency'], ascending=[True, False],)
        del l

    @profile(stream=fp)
    def recursion_sort(self, row, level, number, sort_str):
        s = sort_str + str(number) + '.'
        print(s)
        self.output_list.append((row['phrase'].tolist()[0],
                                 row['phrase_len'].tolist()[0],
                                 row['frequency'].tolist()[0],
                                 s))
        self.phrase_to_update.append((row['id'].tolist()[0], s))
        counter = 1
        first_df = self.df.loc[self.df['phrase'] == row['phrase'].tolist()[0]]
        word_list = first_df['words'].tolist()
        index_list = first_df.index.tolist()
        self.df = self.df.drop(index_list)
        del index_list
        word_df = self.get_phrase_with_words(word_list, level)
        if word_df.empty:
            word_df = self.get_phrase_with_words(word_list, level + 1)
        del word_list
        phrase_list = word_df.phrase.tolist()
        for phrase in set(phrase_list):
            first = word_df.loc[word_df['phrase'] == phrase].head(1)
            self.recursion_sort(first, level + 1, counter, s)
            counter += 1
        del phrase_list
        del first_df
        del word_df
        del counter
        return 0

    @timer
    @profile()
    def get_phrase_with_words(self, word_list, level):
        word_df = pd.DataFrame(columns=settings.PANDAS_COLUMNS)
        append_df = pd.DataFrame(columns=settings.PANDAS_COLUMNS)
        flag = True
        for word in word_list:
            if flag:
                append_df = self.df.loc[self.df['words'] == word]
                if not append_df.empty:
                    word_df = self.df.loc[self.df['phrase'].isin(append_df['phrase'].tolist())]
                flag = False
            else:
                if not word_df.empty:
                    append_df = word_df.loc[word_df['words'] == word]
                    if not append_df.empty:
                        word_df = self.df.loc[self.df['phrase'].isin(append_df['phrase'].tolist())]
        del append_df
        del flag
        return word_df.loc[word_df['phrase_len'] == level + 1]