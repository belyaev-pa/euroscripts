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
    input_folder_path = settings.DECODE_INPUT
    def handle(self, *args, **kwargs):
        for root, dirs, files in os.walk(self.input_folder_path):
            for file in files:
                try:
                    with open(os.path.join(root, file), 'r', encoding='Windows-1251') as f:
                        text = f.read()
                        with open(os.path.join(root, file), 'w+', encoding='utf-8') as utf_f:
                            utf_f.write(text)
                            print('file: {} - success'.format(os.path.join(root, file)))
                except:
                    print('file: {} - error'.format(os.path.join(root, file)))