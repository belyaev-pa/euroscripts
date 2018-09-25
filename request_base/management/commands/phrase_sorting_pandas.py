import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import *
from ...snippets import timer, ns, recursion_sort, get_phrase_list, get_phrase_list2, recursion_sort2, get_phrase_with_words
import time
import pandas as pd
from memory_profiler import profile



class Command(BaseCommand):
    """сортировка списка фраз по хитрой Гришиной схеме (аля граф)"""
    csv_output_file = settings.PHRASE_SORT_OUTPUT_ROOT
    memory_profiler_log = settings.MEMORY_PROFILE_LOG
    fp = open(memory_profiler_log, 'w+')
    @profile(stream=fp)
    def handle(self, *args, **kwargs):
        t = time.time()
        print("start - {}".format(str(time.time() - t)))
        number = 1
        ns.df = pd.DataFrame(get_phrase_list2(), columns=settings.PANDAS_COLUMNS)
        ns.df = ns.df.sort_values(by=['phrase_len', 'frequency'], ascending=[True, False],)
        # while not ns.df.empty:
        #     first = ns.df.head(1)
        #     recursion_sort2(first, 1, number, '')
        #     print('Итерация № {} , я работаю уже: {} с.'.format(number, str(time.time() - t)))
        #     number += 1
        # with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
        #     word_writer = csv.writer(output_file, delimiter=';',
        #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     for obj in ns.output_list:
        #         word_writer.writerow([obj[0], obj[1], obj[2]])
        # print('csv write completed')
        # phrase_list = Phrase.objects.all()
        # for obj in ns.phrase_to_update:
        #     phrase_list.filter(pk=obj[0]).update(sort=obj[1])
        print('phrase update completed')

