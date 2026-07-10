from django.contrib import admin
from .models import User, Media, Episode, Sentence, WordCard, WordBook, WordBookEpisodeRel

admin.site.register(Media)
admin.site.register(User)
admin.site.register(Episode)
admin.site.register(Sentence)
admin.site.register(WordCard)
admin.site.register(WordBook)
admin.site.register(WordBookEpisodeRel)