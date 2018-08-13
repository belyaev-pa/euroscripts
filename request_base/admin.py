from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Phrase)
admin.site.register(Word)
admin.site.register(Tag)
admin.site.register(TagPhrase)

