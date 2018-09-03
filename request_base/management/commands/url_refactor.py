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

    def handle(self, *args, **kwargs):
        t = time.time()
        i = 1
        url_list = Url.objects.all()
        # for url in url_list:
        #     value = url.name
        #     value = value.split('?')[0]
        #     if value[7] == '.':
        #         value = value[:7]+value[7+1:]
        #     url.name = value
        #
        while True:
            try:
                url = Url.objects.all()[i]
            except:
                break
            else:
                same_url_obj = Url.objects.filter(name=url.name).exclude(id=url.id)
                if same_url_obj.exists():
                    for obj in same_url_obj:
                        for obj2 in obj.searchreport_set.all():
                            obj2.url = url
                            obj2.save()
                        for obj3 in obj.yandexdirect_set.all():
                            obj3.url = url
                            obj3.save()
                    same_url_obj.delete()
                print("iter {} time - {}".format(i, str(time.time() - t)))
                i += 1
