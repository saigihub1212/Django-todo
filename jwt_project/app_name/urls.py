from .views import register,login,greet,createtitle
from django.urls import path
urlpatterns=[
    path('register/',register),
    path('login/',login),
    path('greet/',greet),
    path('title/',createtitle)
]