from django.urls import path
from . import views

urlpatterns = [
    path('', views.learnmate_view, name='learnmate'),
]
