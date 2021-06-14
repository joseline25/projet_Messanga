from django.urls import path
from ..views import users_view as views

urlpatterns = [
    path('', views.getWithdraws, name="withdraws"),
    path('create/', views.createWithdraw, name="createWithdraw"),
    path('<str:pk>/delete', views.deleteWithdraw, name="deleteWithdraw"),
    path('<str:pk>/edit', views.editWithdraw, name="editWithdraw")

]
