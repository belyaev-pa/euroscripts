from django.db import models

# Create your models here.
class Phrase(models.Model):
    phrase = models.TextField(db_index=True, unique=True)
    frequency = models.BigIntegerField()
    phrase_len = models.IntegerField()
    tag = models.ManyToManyField('request_base.TagPhrase', blank=True, null=True)
    untaged_words = models.ManyToManyField('request_base.Word', blank=True, null=True)
    uncreated = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.phrase)


class Word(models.Model):
    word = models.CharField(max_length=250, unique=True)
    #phrase = models.ManyToManyField(Phrase, blank=True, null=True)
    frequency = models.BigIntegerField(blank=True, null=True)
    count = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.word)


class Link(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('word', 'phrase')


class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.name)


class TagPhrase(models.Model):
    tag_phrase = models.CharField(max_length=250, unique=True)
    word = models.ManyToManyField(Word)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.tag_phrase)


class Url(models.Model):
    name = models.CharField(max_length=500)


class SearchReport(models.Model):
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE, help_text='запрос')
    traffic = models.FloatField(help_text='доля трафика', null=True, blank=True)
    month_show = models.IntegerField(help_text='показов в месяц', null=True, blank=True)
    position = models.CharField(max_length=100, help_text='позиция', null=True, blank=True)
    position_change = models.CharField(max_length=100, help_text='изменение позиции', null=True, blank=True)
    snippet = models.TextField(help_text='сниппет', null=True, blank=True)
    url = models.ForeignKey(Url, on_delete=models.CASCADE, help_text='url', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.phrase.phrase)


class YandexDirect(models.Model):
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE, help_text='запрос')
    advert = models.TextField(help_text='текст объявления')
    position = models.CharField(max_length=50, help_text='позиция', null=True, blank=True)
    month_show = models.IntegerField(help_text='показов в месяц', null=True, blank=True)
    average_cpc = models.FloatField(help_text='cредний СРС', null=True, blank=True)
    traffic = models.FloatField(help_text='доля трафика', blank=True, null=True)
    rival = models.IntegerField(help_text='конкурентов по запросу', blank=True, null=True)
    url = models.ForeignKey(Url, on_delete=models.CASCADE, help_text='url', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.advert)