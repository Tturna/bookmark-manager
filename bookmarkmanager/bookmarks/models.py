from django.db import models
from django.contrib.auth.models import User


class Bookmark(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200) # corresponding form widget: URLInput
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=25)


class TagInstance(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    bookmark_id = models.ForeignKey(Bookmark, on_delete=models.CASCADE)
