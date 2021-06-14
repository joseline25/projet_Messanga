from django.urls import path
from ..views import users_view as views

urlpatterns = [
    path('', views.getThemes, name="themes"),
    path('add/', views.addTheme, name="addTheme"),
    path('<str:pk>/delete', views.deleteTheme, name="deleteTheme"),
    path('<str:pk>/edit', views.editTheme, name="editTheme")

]
