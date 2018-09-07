import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Sum, Count
from ...models import *
from ...snippets import timer, ns, recursion_sort
import time



class Command(BaseCommand):
    """сортировка списка фраз по хитрой Гришиной схеме (аля граф)"""
    csv_output_file = settings.PHRASE_CSV
    @timer
    def handle(self, *args, **kwargs):
        t = time.time()
        print("start - {}".format(str(time.time() - t)))
        with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            phrase_list = Phrase.objects.all()
            for phrase in phrase_list:
                word_writer.writerow([phrase.phrase])
        print("csv write completed - {}".format(str(time.time() - t)))




