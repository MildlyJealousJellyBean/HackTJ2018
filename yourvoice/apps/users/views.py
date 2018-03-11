import itertools

from django.shortcuts import render, reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect

import utils
# Create your views here.

def show(request, user_id):
    context = utils.nav_context(request)
    context["user"] = get_user_model().objects.get(pk = user_id)
    return HttpResponse(render(request, "users/show.html", context = context))

def politicians(request):
    context = utils.nav_context(request)
    context["connected_politicians"] = request.user.politicians_filtered
    context["requesting_politicians"] = request.user.politician_filter_requests
    
    return HttpResponse(render(request, "users/politicians.html", context = context))

def filterers(request):
    context = utils.nav_context(request)
    context["connected_filterers"] = request.user.connected_filterers
    context["requested_filterers"] = request.user.requested_filterers
    context["available_filterers"] = list(get_user_model().objects.filter(user_type = "filterer"))
    for filterer in itertools.chain(context["connected_filterers"], context["requested_filterers"]):
        if filterer in context["available_filterers"]:
            context["available_filterers"].remove(filterer)
    return HttpResponse(render(request, "users/filterers.html", context = context))

def connect(request, user_id):
    other = get_user_model().objects.get(pk = user_id)
    if request.user.is_politician:
        request.user.connect_to_filterer(other)
        return HttpResponseRedirect(reverse("users:filterers"))
    else:
        request.user.connect_to_politician(other)
        return HttpResponseRedirect(reverse("users:politicians"))

def disconnect(request, user_id):
    other = get_user_model().objects.get(pk = user_id)
    if request.user.is_politician:
        request.user.disconnect_from_filterer(other)
        return HttpResponseRedirect(reverse("users:filterers"))
    else:
        request.user.disconnect_from_politician(other)
        return HttpResponseRedirect(reverse("users:politicians"))