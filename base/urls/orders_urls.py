from django.urls import path
from ..views import orders_views as views

urlpatterns = [
    path('', views.getOrders, name="orders"),
    path('askedOrders/', views.getAskedOrders, name="asked-orders"),
    path('<str:pk>/asked', views.getUserOrders, name="asked-orders"),
    path("add/", views.addOrderItem, name="orders-add"),
]

"""
la différence entre askedOrders/ et <str:pk>/asked est claire dans le libellé mais 
je ne sais sur quel champ du modèle order 
me baser pour les différencier. Que est le champ dans le modèle order qui me renvoie
l'utilisateur à qui est passé la commande?
"""