from django.conf import settings
from django.core.management.base import BaseCommand
from request_base.models import Url
from django.db.models import Sum
import csv
import time
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.INFO)


class Command(BaseCommand):
    url_output_path = settings.URL_OUTPUT

    def handle(self, *args, **kwargs):
        with open(self.url_output_path, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file,
                                     delimiter=';',
                                     quotechar='|',
                                     quoting=csv.QUOTE_MINIMAL)
            url_list = Url.objects.all()
            word_writer.writerow(['url',
                                  'яндекст директ кол-во',
                                  'агрегация суммы показов директа',
                                  'поисковая выдача кол-во',
                                  'агрегация суммы поисковой выдачи'])
            t = time.time()
            for obj in url_list:
                obj_count_sr = obj.searchreport_set.count()
                obj_month_show_sr = obj.searchreport_set.aggregate(Sum('month_show'))
                obj_count_ya = obj.yandexdirect_set.count()
                obj_month_show_ya = obj.yandexdirect_set.aggregate(Sum('month_show'))
                word_writer.writerow([obj.name,
                                      obj_count_ya,
                                      obj_month_show_ya['month_show__sum'],
                                      obj_count_sr,
                                      obj_month_show_sr['month_show__sum']])
                print("next iter: {}".format(str(time.time() - t)))
