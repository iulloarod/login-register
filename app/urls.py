from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('imin', views.imin),
    path('logout', views.logout),
]
