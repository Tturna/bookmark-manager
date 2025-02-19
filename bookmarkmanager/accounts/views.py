from django.shortcuts import render, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages


def RegisterView(request):
    if (request.method == "POST"):
        form = UserCreationForm(request.POST)

        if (form.is_valid()):
            form.save()
            messages.success(request, "Registration successful! You can now log in.")

            return HttpResponseRedirect(reverse("accounts:login"))

        messages.error(request, "Error! Invalid user details.")

        return render(request, "registration/register.html", {"form": form})

    form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def LogoutConfirmView(request):
    return render(request, "registration/logout_confirm.html")


@login_required
def ProfileView(request):
    return render(request, "registration/profile.html")
