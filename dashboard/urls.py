from . import views
from django.urls import path


urlpatterns = [
    path("home", views.index, name="index"),
    path('analytics', views.analytics, name="analytics"),
    path('customers', views.customers_agents, name="customers_agents")
]