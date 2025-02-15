from django.urls import path
from . import views

app_name = "bookmarks"

urlpatterns = [
    path("", views.Index, name="index"),
    path("add/", views.AddBookmark, name="addbookmark")
]
