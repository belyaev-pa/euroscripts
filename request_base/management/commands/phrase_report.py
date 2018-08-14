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
#        phrase_list = Phrase.objects.filter(phrase_le__lte=4).order_by('phrase_len')#prefetch_related('link_set__word')
        with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #for phrase in phrase_list:
                #phrase_word_list = phrase.link_set.values_list('word', flat=True)
                #phrase_with_phrase = Phrase.objects.filter(link__word__in=phrase_word_list).annotate(
                #    num_words=Count('link__words')).filter(num_words=len(phrase_word_list))
                #phrase_count = phrase_with_phrase.count()
                #print(phrase.phrase)
                #print(phrase_count)
                #phrase_frequency = phrase_with_phrase.aggregate(Sum('frequency'))
                #print(phrase_frequency)
                #word_writer.writerow([phrase.phrase, phrase_count, phrase_frequency])
            from_begin, till_end = 0, 1000
            while True:
                phrase_list_pack = Phrase.objects.filter(phrase_len__lte=4).order_by('phrase_len')[from_begin:till_end]
                print(phrase_list_pack.query)

                if phrase_list_pack.exists():
                    for phrase in phrase_list_pack:
                        phrase_word_list = phrase.link_set.values_list('word', flat=True)
                        phrase_with_phrase = Phrase.objects.filter(link__word__in=phrase_word_list).annotate(
                            num_words=Count('link__words')).filter(num_words=len(phrase_word_list))
                        phrase_count = phrase_with_phrase.count()
                        phrase_frequency = phrase_with_phrase.aggregate(Sum('frequency'))
                        word_writer.writerow([phrase.phrase, phrase_count, phrase_frequency])
                        from_begin += 1000
                        till_end += 1000
                else:
                    break
                print(from_begin)

