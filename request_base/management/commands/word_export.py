import csv
import os
from time import gmtime, strftime
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import *


class Command(BaseCommand):
    csv_output_path = settings.OUPPUT_ROOT
    time_now = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    name = 'words_'+time_now+'.csv'
    csv_output_file = os.path.join(csv_output_path, name)

    def handle(self, *args, **kwargs):
        with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for word in Word.objects.all().order_by('-count'):
                if kwargs['reset']:
                    word.frequency = sum(word.link_set.all().values_list('phrase__frequency', flat=True))
                    word.count = word.link_set.count()
                    word.save()
                word_writer.writerow([word.word, word.count or word.link_set.count(), word.frequency or 0])
                pass

    def add_arguments(self, parser):
        parser.add_argument(
            '-r',
            '--reset',
            action='store_true',
            default=False,
            help='Перерасчет значений в БД (затратна по времени)'
        )
