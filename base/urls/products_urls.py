from django.urls import path
from ..views import products_views as views

urlpatterns = [
    path('', views.getProducts, name="products"),
    path('categories/', views.getCategories, name="categories"),
    path('<str:pk>/', views.getProduct, name="product"),
    path('<str:pk>/delete', views.editProduct, name="product"),
    path('<str:pk>/edit', views.editProduct, name="product"),
    #path('addProduct/', views.addProduct, name='addproduct'),
]

