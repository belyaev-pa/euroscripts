from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import *
from ...snippets import get_tag_list


class Command(BaseCommand):
    tags_file_path = settings.TAGS_ROOT
    def handle(self, *args, **kwargs):
        tag_list = get_tag_list(self.tags_file_path)
        for tag in tag_list:
            tag_words = Word.objects.filter(word__in=tag[1])
            tag_obj, created = Tag.objects.get_or_create(
                name= tag[0],
                defaults={'word': tag_words},)
