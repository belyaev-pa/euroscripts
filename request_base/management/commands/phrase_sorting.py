import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import *
from ...snippets import timer, ns, recursion_sort
import time



class Command(BaseCommand):
    """сортировка списка фраз по хитрой Гришиной схеме (аля граф)"""
    csv_output_file = settings.PHRASE_SORT_OUTPUT_ROOT
    @timer
    def handle(self, *args, **kwargs):
        t = time.time()
        print("start - {}".format(str(time.time() - t)))
        number = 1
        while True:
            phrase = Phrase.objects.filter(phrase_len__gte=1).exclude(
                pk__in=ns.processed_id).order_by('phrase_len', '-frequency')
            if phrase.exists():
                recursion_sort(phrase.first(), number, '')
            else:
                break
            if number % 2:
                counter = Phrase.objects.filter(phrase_len__gte=1).exclude(
                    pk__in=ns.processed_id)
                print('Осталось обработать {} фраз, я работаю уже: {} с.'.format(counter.count(), str(time.time() - t)))
            number += 1
        with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for obj in ns.output_list:
                word_writer.writerow(obj)
        print('csv write completed')
        phrase_list = Phrase.objects.all()
        for obj in ns.phrase_to_update:
            phrase_list.filter(pk=obj[0]).update(sort=obj[1])
        print('phrase update completed')



