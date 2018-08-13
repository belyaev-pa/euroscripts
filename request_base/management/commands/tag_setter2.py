from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import *


class Command(BaseCommand):
#    tags_file_path = settings.TAGS_ROOT
    def handle(self, *args, **kwargs):
        phrase_list = Phrase.objects.all()
        tag_list = TagPhrase.objects.all()
        for i, phrase in enumerate(phrase_list):
            print(i)
            for link in phrase.link_set.all():
                phrase.untaged_words.add(link.word)
            for tag in tag_list:
                try:
                    if all((tag_word in phrase.untaged_words.all()) for tag_word in tag.word.all()):
                        phrase.tag.add(tag)
                except:
                    pass
                else:
                    for tag_word in tag.word.all():
                        phrase.untaged_words.remove(tag_word)