from django.urls import path

from . import views

app_name = 'messages'

urlpatterns = [
    path('new', views.new, name='new'),
    path("sent_by_me", views.sent_by_me, name="sent_by_me"),
    path("filter/<int:politician_id>", views.filter, name="filter"),
    path("statistics", views.statistics, name = "statistics"),
    path("public", views.list_public, name = "list_public"),
    path("<int:message_id>/set_visibility", views.set_visibility, name = "set_visibility"),
]