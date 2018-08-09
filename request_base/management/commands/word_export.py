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
        with open(self.csv_output_file, 'w') as output_file:
            word_writer = csv.writer(output_file, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for word in Word.objects.all():
                if not word.frequency:
                    frequency = 0
                    for link in word.link_set.all():
                        frequency += link.phrase.frequency
                    word.frequency = frequency
                    word.save()
                word_writer.writerow([word.word, word.link_set.count(), word.frequency])
                pass
