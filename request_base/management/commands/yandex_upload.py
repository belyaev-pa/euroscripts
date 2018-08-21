#import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from ...snippets import word_tokenize, get_data
from ...models import *
#logger = logging.getLogger('default')
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.INFO)

class Command(BaseCommand):
    csv_file_path = settings.YANDEX_ROOT
    def handle(self, *args, **kwargs):
        bulk_list = dict(yandex=list(), url=set(), phrase=list())
        for iter, row in enumerate(get_data(self.csv_file_path), 1):
            yandex_dict = dict(
                phrase = row[0],
                advert = row[1],
                position = row[2],
                month_show = row[3],
                average_cpc = row[4],
                traffic = row[5],
                rival = row[6],
                url = row[7],
            )
            bulk_list['phrase'].append(row[0])
            bulk_list['url'].add(row[7])
            bulk_list['yandex'].append(yandex_dict)
            if iter % 5000 == 0:
                print('---{}'.format(iter))
#                logger.info('msg')
                phrase_obj = Phrase.objects.filter(phrase__in=[i['phrase'] for i in bulk_list['yandex']]).values_list(
                    'phrase',
                    flat=True)
                url_obj = Url.objects.filter(url__in=[i['url'] for i in bulk_list['yandex']]).values_list('url', fltt=True)
                if phrase_obj:
                    bulk_list['yandex'] = [i for i in bulk_list['phrase'] if i['phrase'] not in check]
                created_phrase = False
                if bulk_list['phrase']:
                    created_phrase = Phrase.objects.bulk_create([Phrase(**i) for i in bulk_list['phrase']],
                                                                len(bulk_list['phrase']))
                url_obj = Url.objects.filter(name__in=bulk_list['url'])
                value_list = url_obj.values_list('url', flat=True)
                bulk_list['url'] -= set(value_list)
                if bulk_list['url']:
                    Url.objects.bulk_create([Url(name=i) for i in bulk_list['url']],
                                             len(bulk_list['url']))
                if not created_phrase:
                    bulk_list = dict(phrase=list(), word=set(), link=list())
                    continue
                bulk_list['url'] |= set(value_list)
                obj_queryset = Url.objects.filter(name__in=bulk_list['url'])
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

