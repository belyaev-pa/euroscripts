import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import *
from ...snippets import timer, get_tag_list, word_tokenize
import time
from collections import defaultdict


class Command(BaseCommand):
    csv_output_file = settings.TAGS_OUTPUT_ROOT
    tags_file_path = settings.TAGS_ROOT
    word_dict_csv_out = settings.WORD_DICT_OUT
    @timer
    def handle(self, *args, **kwargs):
        phrase_list = Phrase.objects.all()
#        tag_list = TagPhrase.objects.all()#.values_list('tag_phrase', 'tag__name', 'word__count')
        tag_list = get_tag_list(self.tags_file_path)
        #print(tag_list)
        t = time.time()
        words_dict = defaultdict(int)
#        for i, phrase in enumerate(phrase_list):
#            if i < 200000:
#                continue
#            print("{} start - {}".format(i, str(time.time() - t)))
#            if phrase.untaged_words:
#                for link in phrase.link_set.all():
#                    phrase.untaged_words.add(link.word)
#            print("{} add untagged- {}".format(i, str(time.time() - t)))
#            for tag in tag_list:
#                phrase_taged = phrase.untaged_words.filter(id__in=tag.word.all())
#                phrase.tag.add(tag)
#                phrase.untaged_words.remove(*phrase_taged)
#            print(phrase.tag)
#            print("{} tag_analyse - {}".format(i, str(time.time() - t)))
        with open(self.csv_output_file, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            print("start - {}".format(str(time.time() - t)))
            for i, phrase in enumerate(phrase_list):
                print("{} iteration - {}".format(i, str(time.time() - t)))
                phrase_set = set(word_tokenize(phrase.phrase))
                res_list = list()
                res_tag_prase_list = list()
                for tag in tag_list:
                    if set(tag[2]).issubset(phrase_set):
                        phrase_set.difference_update(set(tag[2]))
                        res_list.append(tag[1])
                        res_tag_prase_list.append(tag[0])
                for word in phrase_set:
                    words_dict[word] += 1
                word_writer.writerow([phrase.phrase, res_list, phrase_set, res_tag_prase_list])
        with open(self.word_dict_csv_out, 'w+', newline='', encoding='Windows-1251') as output_file:
            word_writer = csv.writer(output_file, delimiter=';',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for key, value in words_dict.items():
                word_writer.writerow([key, value])
