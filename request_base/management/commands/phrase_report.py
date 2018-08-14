import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Sum
from ...models import *
from ...snippets import timer, get_tag_list, word_tokenize
import time
from collections import defaultdict


class Command(BaseCommand):
    csv_output_file = settings.PHRASE_OUTPUT_ROOT
    @timer
    def handle(self, *args, **kwargs):
        phrase_list = Phrase.objects.all().order_by('')
        t = time.time()
        with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            print("start - {}".format(str(time.time() - t)))
            for i, phrase in enumerate(phrase_list):
                print("{} iteration - {}".format(i, str(time.time() - t)))
                phrase_word_list = phrase.link_set.value_list('word__word')
                phrase_with_phrase = Phrase.objects.filter(link__word__in=phrase_word_list)
                phrase_count = phrase_with_phrase.count()
                phrase_frequency = phrase_with_phrase.aggregate(Sum('frequency'))
                word_writer.writerow([phrase.phrase, phrase_count, phrase_frequency])

