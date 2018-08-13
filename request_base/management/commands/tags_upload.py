from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import *
from ...snippets import get_tag_list


class Command(BaseCommand):
    tags_file_path = settings.TAGS_ROOT
    def handle(self, *args, **kwargs):
        tag_list = get_tag_list(self.tags_file_path)
        for tag in tag_list:
            tag_words = Word.objects.filter(word__in=tag[2])
            if len(tag[2]) != len(tag_words):
                for word in tag[2]:
                    Word.objects.get_or_create(word=word, defaults={'frequency': 0, 'count': 0},)
                tag_words = Word.objects.filter(word__in=tag[1])
            tag_obj, created = Tag.objects.get_or_create(name=tag[1], defaults={})
            tag_phrase_obj, created = TagPhrase.objects.get_or_create(tag_phrase=tag[0],
                                                                      defaults={'tag': tag_obj})
            tag_phrase_obj.word.set(tag_words)
