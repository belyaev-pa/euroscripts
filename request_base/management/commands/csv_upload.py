import csv
#import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from ...snippets import word_tokenize
from ...models import *
#logger = logging.getLogger('default')

class Command(BaseCommand):
    csv_file_path = settings.CSV_ROOT
    def handle(self, *args, **kwargs):
        bulk_list = dict(phrase=list(), word=set(), link=list())
        phr_count = Phrase.objects.count()
        for iter, row in enumerate(get_data(self.csv_file_path), 1):
            if iter < phr_count:
                continue
            phrase = row[0]
            frequency = int(str(row[1]).replace('.', '').replace(' ', '').replace(',', '') or '1')
            phrase_word_set = set(word_tokenize(phrase))
            phrase_dict = dict(
                phrase=phrase,
                frequency=frequency,
                phrase_len=len(phrase_word_set),
            )
            bulk_list['phrase'].append(phrase_dict)
            for word in phrase_word_set:
                bulk_list['word'].add(word)
                bulk_list['link'].append(dict(phrase=phrase, word=word))

            if iter % 2500 == 0:
                print('---{}'.format(iter))
#                logger.info('msg')
                check = Phrase.objects.filter(phrase__in=[i['phrase'] for i in bulk_list['phrase']]).values_list(
                    'phrase',
                    flat=True)
                if check:
                    bulk_list['phrase'] = [i for i in bulk_list['phrase'] if i['phrase'] not in check]
                created_phrase = False
                if bulk_list['phrase']:
                    created_phrase = Phrase.objects.bulk_create([Phrase(**i) for i in bulk_list['phrase']],
                                                                len(bulk_list['phrase']))
                obj_queryset = Word.objects.filter(word__in=bulk_list['word'])
                value_list = obj_queryset.values_list('word', flat=True)
                bulk_list['word'] -= set(value_list)
                if bulk_list['word']:
                    Word.objects.bulk_create([Word(word=i) for i in bulk_list['word']],
                                             len(bulk_list['word']))
                if not created_phrase:
                    bulk_list = dict(phrase=list(), word=set(), link=list())
                    continue
                bulk_list['word'] |= set(value_list)
                obj_queryset = Word.objects.filter(word__in=bulk_list['word'])
                unique = []
                for unique_obj in bulk_list['link']:
                    if unique_obj in unique:
                        continue
                    unique.append(unique_obj)
                for obj in list(unique):
                    obj['word'] = obj_queryset.get(word=obj['word'])
                    obj['phrase'] = [item for item in created_phrase if item.phrase == obj['phrase']][0]
                if bulk_list['link']:
                    Link.objects.bulk_create([Link(**i) for i in bulk_list['link']], len(bulk_list['link']))
                bulk_list = dict(phrase=list(), word=set(), link=list())
            if iter % 10000 == 0:
                print('######{}'.format(iter))

def get_data(filename1):
    with open(filename1, encoding='Windows-1251') as f_csv:
        reader = csv.reader(f_csv, delimiter=';')
        for row in reader:
            yield (row)