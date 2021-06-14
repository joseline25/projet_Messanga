from django.urls import path
from ..views import users_view as views

urlpatterns = [
    path('', views.getShops, name="shops"),
    path('add/', views.addShop, name="addShop"),

]
