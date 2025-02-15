from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import BookmarkForm
from .models import Bookmark


def Index(request):
    bookmarks = Bookmark.objects.all()

    return render(request, "bookmarks/index.html", {"bookmarks": bookmarks})


def AddBookmark(request):
    if (request.method == "POST"):
        form = BookmarkForm(request.POST)

        if (form.is_valid()):
            # process form.cleaned_data (dict of form data)
            bm_name = form.cleaned_data["name"]
            bm_url = form.cleaned_data["url"]

            # hard code user since we don't have auth yet
            bm = Bookmark(name=bm_name, url=bm_url, user_id=User.objects.first())
            bm.save()

            messages.success(request, "Bookmark added successfully!")

            return HttpResponseRedirect(reverse("bookmarks:addbookmark"))

        messages.error(request, "Error! Invalid bookmark.")

    # assume GET request
    form = BookmarkForm()

    return render(request, "bookmarks/add.html", {"form": form})
