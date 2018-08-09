from django.db import models

# Create your models here.
class Phrase(models.Model):
    phrase = models.TextField(db_index=True, unique=True)
    frequency = models.BigIntegerField()
    phrase_len = models.IntegerField()


class Word(models.Model):
    word = models.CharField(max_length=250, unique=True)
    #phrase = models.ManyToManyField(Phrase, blank=True, null=True)
    frequency = models.BigIntegerField(blank=True, null=True)


class Link(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('word', 'phrase')


class Tag(models.Model):
    name = models.CharField(max_length=250, unique=True)
    word = models.ManyToManyField()
