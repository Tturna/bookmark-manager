from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import BookmarkForm
from .models import Bookmark


def Index(request):
    bookmarks = Bookmark.objects.all()

    return render(request, "bookmarks/index.html", {"bookmarks": bookmarks})

@login_required
def AddBookmark(request):
    if (request.method == "POST"):
        form = BookmarkForm(request.POST)

        if (form.is_valid()):
            # process form.cleaned_data (dict of form data)
            bm_name = form.cleaned_data["name"]
            bm_url = form.cleaned_data["url"]
            
            bm = Bookmark(name=bm_name, url=bm_url, user=request.user)
            bm.save()

            messages.success(request, "Bookmark added successfully!")

            return HttpResponseRedirect(reverse("bookmarks:addbookmark"))

        messages.error(request, "Error! Invalid bookmark.")
        return render(request, "bookmarks/add.html", {"form": form})

    # assume GET request
    form = BookmarkForm()

    return render(request, "bookmarks/add.html", {"form": form})

@login_required
def EditBookmark(request, pk):
    bm = get_object_or_404(Bookmark, pk=pk)

    if (bm.user != request.user):
        return HttpResponseForbidden()

    if (request.method == "POST"):
        form = BookmarkForm(request.POST, instance=bm)

        if (form.is_valid()):
            form.save()
            messages.success(request, f"Bookmark '{bm.name}' updated successfully!")

            return HttpResponseRedirect(reverse("bookmarks:editbookmark", args=[bm.id]))

        messages.error(request, "Error! Invalid bookmark.")
        context = {
            "bookmark": bm,
            "form": form
        }

        return render(request, "bookmarks/edit.html", context)

    # use "instance" to prepopulate the ModelForm
    form = BookmarkForm(instance=bm)
    context = {
        "bookmark": bm,
        "form": form
    }

    return render(request, "bookmarks/edit.html", context)


def DeleteBookmark(request, pk):
    bm = get_object_or_404(Bookmark, pk=pk)

    if (request.method == "POST"):
        bm.delete()
        return HttpResponseRedirect(reverse("bookmarks:index"))

    return render(request, "bookmarks/confirm_delete.html", {"bookmark": bm})
