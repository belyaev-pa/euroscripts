import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Sum, Count
from ...models import *
from ...snippets import timer
import time



class Command(BaseCommand):
    """Получаем список фраз, проходим по нему
     на каждой итерации делаем filter() фраз по словам
     делаем count(), Sum(frequency)  и пишем результат в csv"""
    csv_output_file = settings.PHRASE_OUTPUT_ROOT
    @timer
    def handle(self, *args, **kwargs):
        phrase_list = Phrase.objects.filter(phrase_len__lte=4).order_by('phrase_len')#prefetch_related('link_set__word')
        print(phrase_list.count())
        t = time.time()
        with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            from_begin, till_end = 0, 1000
            print("start - {}".format(str(time.time() - t)))
            while True:
                phrase_list_pack = Phrase.objects.filter(phrase_len__lte=4).order_by('phrase_len')[from_begin:till_end]
                if phrase_list_pack.exists():
                    for phrase in phrase_list_pack:
                        phrase_word_list = phrase.link_set.values_list('word_id', flat=True)
                        if len(phrase_word_list) == 1:
                            phrase_with_phrase = Phrase.objects.filter(link__word_id=phrase_word_list[0])
                        elif len(phrase_word_list) == 2:
                            phrase_with_phrase = Phrase.objects.filter(link__word_id=phrase_word_list[0]
                                                             ).filter(link__word_id=phrase_word_list[1])
                        elif len(phrase_word_list) == 3:
                            phrase_with_phrase = Phrase.objects.filter(link__word_id=phrase_word_list[0]
                                                             ).filter(link__word_id=phrase_word_list[1]
                                                             ).filter(link__word_id=phrase_word_list[1])
                        elif len(phrase_word_list) == 4:
                            phrase_with_phrase = Phrase.objects.filter(link__word_id=phrase_word_list[0]
                                                             ).filter(link__word_id=phrase_word_list[1]
                                                             ).filter(link__word_id=phrase_word_list[2]
                                                             ).filter(link__word_id=phrase_word_list[3])
                        else:
                            continue
                        phrase_count = phrase_with_phrase.count()
                        phrase_frequency = phrase_with_phrase.aggregate(Sum('frequency'))
                        word_writer.writerow([phrase.phrase, phrase.phrase_len, phrase_count, phrase_frequency])
                else:
                    break
                from_begin += 1000
                till_end += 1000
                print("{} items - {}".format(from_begin, str(time.time() - t)))

