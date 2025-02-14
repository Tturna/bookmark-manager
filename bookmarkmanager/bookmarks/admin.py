from django.contrib import admin
from .models import Bookmark, Tag, TagInstance

admin.site.register(Bookmark)
admin.site.register(Tag)
admin.site.register(TagInstance)
