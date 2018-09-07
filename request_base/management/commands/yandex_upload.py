import os
from django.conf import settings
from django.core.management.base import BaseCommand
from ...snippets import word_tokenize, get_data
from ...models import *
#logger = logging.getLogger('default')
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.INFO)

class Command(BaseCommand):
    yandex_file_path = settings.YANDEX_ROOT
    def handle(self, *args, **kwargs):
        for root, dirs, files in os.walk(self.yandex_file_path):
            for file in files:
                print('file: {}'.format(file))
                bulk_list = dict(yandex=list(), url=set(), phrase=set())
                for iter, row in enumerate(get_data(os.path.join(root, file)), 1):
                    if iter == 1:
                        continue
                    url_ref = row[7]
                    url_ref = url_ref.split('?')[0]
                    url_ref = url_ref.replace('www.', '').replace('https', 'http').lower()
                    if url_ref[-1] == '/':
                        url_ref = url_ref[0:-1]
                    yandex_dict = dict(
                        phrase = row[0],
                        advert = row[1],
                        position = row[2],
                        month_show = int(str(row[3]).replace('.', '').replace(' ', '').replace(',', '') or '0'),
                        average_cpc = float(str(row[4]).replace(',', '.').replace(' ', '') or '0'),
                        traffic = float(str(row[5]).replace(',', '.').replace(' ', '') or '0'),
                        rival = int(str(row[6]).replace('.', '').replace(' ', '').replace(',', '') or '0'),
                        url = url_ref,
                    )
                    bulk_list['phrase'].add(row[0])
                    bulk_list['url'].add(url_ref)
                    bulk_list['yandex'].append(yandex_dict)
                    if iter % 5000 == 0:
                        phrase_obj = Phrase.objects.filter(
                            phrase__in=[i for i in bulk_list['phrase']])
                        url_obj = Url.objects.filter(name__in=[i for i in bulk_list['url']])
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
                else:
                    phrase_obj = Phrase.objects.filter(
                        phrase__in=[i for i in bulk_list['phrase']])
                    url_obj = Url.objects.filter(name__in=[i for i in bulk_list['url']])
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
                    print('ended{}'.format(file))

