from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import Bookmark
from .forms import BookmarkForm


class IndexViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="Guy", password="qwerty")

    def test_valid_empty_bookmarklist(self):
        client = self.client
        response = client.get(reverse("bookmarks:index"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["bookmarks"], [])

    def test_valid_populated_bookmarklist(self):
        Bookmark.objects.create(name="Example", url="https://example.com/", user_id=User.objects.first())
        client = self.client
        response = client.get(reverse("bookmarks:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["bookmarks"]), 1)
        self.assertContains(response, "Example")


class AddBookmarkViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Guy", password="qwerty")

    def test_get_form(self):
        client = self.client
        response = client.get(reverse("bookmarks:addbookmark"))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BookmarkForm)
        self.assertContains(response, "<form")

    def test_post_valid_bookmark(self):
        client = self.client
        data = {
            "name": "Example",
            "url": "https://www.example.com"
        }
        response = client.post(reverse("bookmarks:addbookmark"), data)

        self.assertRedirects(response, reverse("bookmarks:addbookmark"))
        self.assertEqual(Bookmark.objects.count(), 1)
        bm = Bookmark.objects.first()
        self.assertEqual(bm.url, "https://www.example.com")
        # This will need a redo once auth is implemented and bookmarks reference the right users
        self.assertEqual(bm.user_id, self.user)

    def test_post_invalid_url_bookmark(self):
        client = self.client
        data = {
            "name": "Example",
            "url": "invaliad urle"
        }

        response = client.post(reverse("bookmarks:addbookmark"), data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BookmarkForm)
        # Could use assertContains with 'response' directly but this
        # method is case-insensitive
        self.assertIn("error", response.content.decode().lower())
        self.assertEqual(Bookmark.objects.count(), 0)


class EditBookmarkViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Guy", password="qwerty")
        Bookmark.objects.create(name="Example", url="https://www.example.com", user_id=self.user)

    def test_get_valid_edit_form(self):
        client = self.client
        response = client.get(reverse("bookmarks:editbookmark", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BookmarkForm)
        self.assertContains(response, "Example")
        self.assertContains(response, "https://www.example.com")

    def test_update_valid_bookmark(self):
        client = self.client
        newdata = {
            "name": "Github",
            "url": "https://www.github.com"
        }

        response = client.post(reverse("bookmarks:editbookmark", args=[1]), newdata)

        self.assertRedirects(response, reverse("bookmarks:editbookmark", args=[1]))
        self.assertEqual(Bookmark.objects.count(), 1)
        bm = Bookmark.objects.first()
        self.assertEqual(bm.name, "Github")
        self.assertEqual(bm.url, "https://www.github.com")
        self.assertEqual(bm.user_id, self.user)

    def test_update_invalid_bookmark(self):
        client = self.client
        newdata = {
            "name": "",
            "url": "invaldfpwer url asd"
        }

        response = client.post(reverse("bookmarks:editbookmark", args=[1]), newdata)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BookmarkForm)
        self.assertIn("error", response.content.decode().lower())

    def test_get_invalid_pk(self):
        client = self.client
        response = client.get(reverse("bookmarks:editbookmark", args=[5]))

        self.assertEqual(response.status_code, 404)

    def test_post_invalid_pk(self):
        client = self.client
        data = {
            "name": "Github",
            "url": "https://www.github.com"
        }

        response = client.post(reverse("bookmarks:editbookmark", args=[5]), data)

        self.assertEqual(response.status_code, 404)


class DeleteBookmarkViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Guy", password="qwerty")
        Bookmark.objects.create(name="Example", url="https://www.example.com", user_id=self.user)

    def test_delete_valid_pk(self):
        client = self.client
        response = client.post(reverse("bookmarks:deletebookmark", args=[1]))

        self.assertRedirects(response, reverse("bookmarks:index"))
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_delete_invalid_pk(self):
        response = self.client.post(reverse("bookmarks:deletebookmark", args=[5]))

        self.assertEqual(response.status_code, 404)
