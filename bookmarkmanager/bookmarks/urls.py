from django.urls import path
from . import views

app_name = "bookmarks"

urlpatterns = [
    path("", views.Index, name="index"),
    path("add/", views.AddBookmark, name="addbookmark"),
    path("<int:pk>/edit/", views.EditBookmark, name="editbookmark"),
    path("<int:pk>/delete/", views.DeleteBookmark, name="deletebookmark")
]
