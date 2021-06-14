from django.urls import path
from ..views import products_views as views

urlpatterns = [
    path('', views.getCategories, name="categories"),
    path('add/', views.addCategory, name="addCategory"),
    path('<str:pk>/', views.getCategory, name="getCategory"),
    path('<str:pk>/delete', views.deleteCategory, name="deleteCategory"),
    path('<str:pk>/edit', views.editCategory, name="editCategory"),
    #path('addProduct/', views.addProduct, name='addproduct'),
]

