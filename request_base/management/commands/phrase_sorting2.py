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
    # global variables
    input_list = list()
    output_list = list()
    phrase_to_update = list()
    t = time.time()
    number = 1
    global_counter = 1
    # settings
    csv_output_file = settings.PHRASE_SORT_OUTPUT_ROOT
    memory_profiler_log = settings.MEMORY_PROFILE_LOG
    fp = open(memory_profiler_log, 'w+')

    @profile(stream=fp)
    @timer
    def handle(self, *args, **kwargs):
        print("start - {}".format(str(time.time() - self.t)))
        one_word_phrase_list = self.get_phrase_list()
        for phrase, word in one_word_phrase_list:
            print(phrase)
            self.get_phrase_with_word_list(word)
            self.process()
            self.csv_append()
            # self.db_update()
            self.obj_reset()
        self.process_remainder()

    @timer
    @profile(stream=fp)
    def get_phrase_list(self):
        result = list(Link.objects.filter(phrase__phrase_len=1
                                 ).order_by('-phrase__frequency'
                                 )[:3].values_list('phrase__phrase', 'word__word'))
        return result

    @timer
    @profile(stream=fp)
    def get_phrase_with_word_list(self, word):
        """
        tuples = [
            (request, set, len, frequency, id),
            (request, set, len, frequency, id),
            (request, set, len, frequency, id),
        ]                                """
        print("start - {}".format(str(time.time() - self.t)))
        tuples_list = list()
        i = 1
        for obj in Phrase.objects.filter(phrase_len__gte=1).filter(link__word__word__icontains=word):
            phrase_word_list = obj.link_set.values_list('word__word', flat=True)
            tuple_element = (obj.phrase, set(phrase_word_list), obj.phrase_len, obj.frequency, obj.id)
            tuples_list.append(tuple_element)
            print('Итерация № {} , я работаю уже: {} с.'.format(i, str(time.time() - self.t)))
            i += 1
        self.input_list = sorted(tuples_list, key=lambda x: (x[2], -x[3]))

    @profile(stream=fp)
    def recursion_sort(self, obj, number, level):
        s = level + str(number)
        self.output_list.append((*obj, s))
        self.input_list.remove(obj)
        self.phrase_to_update.append((obj[4], s))
        counter = 1
        for item in self.input_list:
            if obj[1].issubset(item[1]):
                self.recursion_sort(item, counter, s + '.')
                counter += 1
        return 0

    @timer
    @profile(stream=fp)
    def process(self):
        while self.input_list:
            self.recursion_sort(self.input_list[False], self.number, str(self.global_counter)+'.')
            print('Итерация № {} , я работаю уже: {} с.'.format(self.number, str(time.time() - self.t)))
            self.number += 1

    @timer
    @profile(stream=fp)
    def csv_append(self):
        with open(self.csv_output_file, 'a+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                     quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for obj in self.output_list:
                word_writer.writerow([obj[0], obj[2], obj[3], obj[5]])
        print('csv write completed')

    @timer
    @profile(stream=fp)
    def db_update(self):
        phrase_list = Phrase.objects.all()
        for obj in self.phrase_to_update:
            p = phrase_list.filter(pk=obj[0])
            p.update(sort=obj[1])
            p.update(processed=True)
        print('phrase update completed {}'.format(self.number))

    @timer
    @profile(stream=fp)
    def obj_reset(self):
        self.output_list = list()
        self.phrase_to_update = list()
        self.number = 1
        self.global_counter += 1

    @timer
    @profile(stream=fp)
    def process_remainder(self):
        pass
