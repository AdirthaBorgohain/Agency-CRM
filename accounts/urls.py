from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirector, name="redirector"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name='logout')
]