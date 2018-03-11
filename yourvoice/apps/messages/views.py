import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse

import utils
from yourvoice.apps.filterers.models import MessageTag
from yourvoice.apps.issues.models import Issue, Stance

from .models import Message

# Create your views here.

def list_public(request):
    context = utils.nav_context(request)
    context["messages"] = Message.objects.filter(is_public = True)
    return HttpResponse(render(request, "messages/public.html", context = context))
    

def new(request):
    context = utils.nav_context(request)
    
    if request.method == "POST":
        message = request.POST["message"]
        politician_id = request.POST["politician"]
        is_public = "is_public" in request.POST
        context["message"] = message.strip()
        context["politician_id"] = politician_id
        context["is_public"] = is_public
        if len(message) < 30:
            context["error_messages"] = "Your message must be at least 30 characters long."
        elif len(message) > 65535:
            context["error_messages"] = "Your message must be less than 65,535 characters long."
        else:
            message = Message(text = message, sender = request.user, recipient = get_user_model().objects.get(pk = politician_id), is_public = is_public)
            try:
                message.save()
            except ValidationError as ex:
                context["error_messages"] = str(ex.message)
            else:
                return HttpResponseRedirect("/")

    context["politicians"] = list(get_user_model().objects.filter(user_type = "politician"))
    return HttpResponse(render(request, "messages/new.html", context = context))


def sent_by_me(request):
    context = utils.nav_context(request)
    messages = Message.objects.filter(sender = request.user)
    context["messages"] = messages
    return HttpResponse(render(request, "messages/list_mine.html", context = context))


def filter(request, politician_id):
    if request.method == "POST":
        message_id = request.POST["message_id"]
        issue_id = request.POST["issue_id"]
        stance_id = request.POST["stance_id"]
        message = Message.objects.get(pk = message_id)
        issue = Issue.objects.get(pk = issue_id)
        stance = Stance.objects.get(pk = stance_id)
        tag = MessageTag(filterer = request.user, message = message, issue = issue, stance = stance)
        tag.save()
    context = utils.nav_context(request)
    politician = get_user_model().objects.get(pk = politician_id)
    messages = Message.objects.filter(recipient = politician)
    context["messages"] = [message for message in messages if message.tag is None]
    context["politician"] = politician
    issues = Issue.objects.all()
    stances = {issue.id: [[stance.id, stance.name] for stance in issue.stances] for issue in issues}
    context["issues"] = issues
    context["json_issues_stances"] = json.dumps(stances)
    return HttpResponse(render(request, "messages/list_to_filter.html", context = context))


def statistics(request):
    issues = Issue.objects.all()
    stances = []

    issue_votes = []
    stance_votes = []
    max_cols = 1
    for issue in issues:
        stances.append(issue.stances)
        issue_votes.append(len(MessageTag.objects.filter(issue = issue)))
        stance_votes.append([len(MessageTag.objects.filter(stance = stance)) for stance in issue.stances])
        max_cols = max(max_cols, len(issue.stances))
    

    stance_percents = []
    for i_vote, s_votes in zip(issue_votes, stance_votes):
        if not i_vote:
            stance_percents.append([0.0] * len(s_votes))
        else:
            stance_percents.append([s_vote * 100.0 / i_vote for s_vote in s_votes])

    context = utils.nav_context(request)
    stances_and_percents = [list(zip(stance, stance_pct)) for stance, stance_pct in zip(stances, stance_percents)]
    context["issues_and_stances"] = list(zip(issues, stances_and_percents))
    context["max_cols"] = max_cols

    return HttpResponse(render(request, "messages/statistics.html", context = context))


def set_visibility(request, message_id):
    if request.method == "POST":
        message = Message.objects.get(pk = message_id)
        message.is_public = ("is_public" in request.POST)
        message.save()
    return HttpResponseRedirect(reverse("messages:sent_by_me"))
