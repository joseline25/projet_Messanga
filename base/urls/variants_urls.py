from django.urls import path
from ..views import products_views as views

urlpatterns = [
    #path('', views.getVariants, name="variants"),
    path('<str:pk>/', views.getVariants, name="getVariants"),
    path('<str:pk>/delete', views.deleteVariant, name="deleteVariant"),
    path('<str:pk>/edit', views.editVariant, name="editVariant"),
    path('add/', views.addVariant, name='addVariant'),
]

