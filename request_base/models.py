from django.db import models

# Create your models here.
class Phrase(models.Model):
    phrase = models.TextField(db_index=True, unique=True)
    frequency = models.BigIntegerField()
    phrase_len = models.IntegerField()
    tag = models.ManyToManyField('request_base.TagPhrase', blank=True, null=True)
    untaged_words = models.ManyToManyField('request_base.Word', blank=True, null=True)

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
