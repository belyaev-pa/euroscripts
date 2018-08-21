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
        bulk_list = dict(yandex=list(), url=set(), phrase=set())
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
            bulk_list['phrase'].add(row[0])
            bulk_list['url'].add(row[7])
            bulk_list['yandex'].append(yandex_dict)
            if iter % 5000 == 0:
#                logger.info('msg')
                phrase_obj = Phrase.objects.filter(
                    phrase__in=[i for i in bulk_list['phrase']])
                url_obj = Url.objects.filter(url__in=[i for i in bulk_list['url']])
                url_value_list = url_obj.values_list('name', flat=True)
                phrase_value_list = phrase_obj.values_list('phrase', flat=True)
                bulk_list['url'] -= set(url_value_list)
                bulk_list['phrase'] -= set(phrase_value_list)
                if bulk_list['url']:
                    Url.objects.bulk_create([Url(name=i) for i in bulk_list['url']],
                                             len(bulk_list['url']))
                if bulk_list['phrase']:
                    Phrase.objects.bulk_create(
                        [Phrase(phrase=i, frequency=0, phrase_len=0, uncreated=True) for i in bulk_list['phrase']],
                    len(bulk_list['phrase']))
                bulk_list['url'] |= set(url_value_list)
                bulk_list['phrase'] |= set(phrase_value_list)
                url_queryset = Url.objects.filter(name__in=bulk_list['url'])
                phrase_queryset = Phrase.objects.filter(phrase__in=bulk_list['phrase'])
                for obj in bulk_list['yandex']:
                    obj['url'] = url_queryset.get(name=obj['url'])
                    obj['phrase'] = phrase_queryset.get(phrase=obj['phrase'])
                if bulk_list['yandex']:
                    YandexDirect.objects.bulk_create(
                        [YandexDirect(**i) for i in bulk_list['yandex']], len(bulk_list['yandex']))
                bulk_list = dict(yandex=list(), url=set(), phrase=set())
                print('######{}'.format(iter))

