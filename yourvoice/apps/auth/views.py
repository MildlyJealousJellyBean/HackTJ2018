import re

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


import utils


app_name = "auth"
# Create your views here.

@login_required
def index(request):
    return HttpResponse(render(request, "index.html", context = utils.nav_context(request)))

def login(request):
    return auth_views.login(request, "registration/login.html", extra_context = utils.nav_context(request))


def logout(request):
    return auth_views.logout(request)

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("auth:index"))
    context = utils.nav_context(request)
    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        filterer = "filterer" in request.POST
        context["username"] = username
        context["firstname"] = firstname
        context["lastname"] = lastname
        context["email"] = email
        context["filterer"] = filterer
        if not username.strip():
            context["error_messages"] = "You have to type a username."
        elif len(username) > 30:
            context["error_messages"] = "Sorry, but your username can't be more than 30 characters."
        else:
            same_username = get_user_model().objects.filter(username = username)
            if len(list(same_username)):
                context["error_messages"] = "Sorry, somebody else has the same username."
            else:
                if not firstname.strip():
                    context["error_messages"] = "You have to type a first name."
                elif not lastname.strip():
                    context["error_messages"] = "You have to type a last name."
                else:
                    if not email.strip():
                        context["error_messages"] = "You have to type an email address."
                    else:
                        if request.POST["password"] != request.POST["password2"]:
                            context["error_messages"] = "Sorry, those passwords don't match."
                        elif not request.POST["password"].strip():
                            context["error_messages"] = "You need to enter a password"
                        else:
                            user = get_user_model().objects.create_user(first_name = firstname, last_name = lastname, username = username, email = email, password = request.POST["password"], user_type = "filterer" if filterer else "person")
                            user.save()
                            return HttpResponseRedirect(reverse("auth:index"))
    return HttpResponse(render(request, "registration/signup.html", context = context))
