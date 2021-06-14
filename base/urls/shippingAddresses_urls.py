from django.urls import path
from ..views import users_view as views

urlpatterns = [
    path('', views.getShippingAddresses, name="shippingAddresses"),
    path('add/', views.addShippingAddress, name="addShippingAddress"),
    path('<str:pk>/delete', views.deleteShippingAddress, name="deleteShippingAddress"),
    path('<str:pk>/edit', views.editShippingAddress, name="editShippingAddress")

]
