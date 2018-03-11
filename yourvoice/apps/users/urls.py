from django.urls import path

from . import views

app_name = 'urls'

urlpatterns = [
    path('<int:user_id>', views.show, name='show'),
    path('politicians/', views.politicians, name='politicians'),
    path('filterers/', views.filterers, name='filterers'),
    path('connect/<int:user_id>', views.connect, name='connect'),
    path('disconnect/<int:user_id>', views.disconnect, name='disconnect'),
]