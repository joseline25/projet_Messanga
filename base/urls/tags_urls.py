from django.urls import path
from ..views import products_views as views

urlpatterns = [
    path('', views.getTags, name="tags"),
    path('<str:pk>/', views.getProductTags, name="getProductTags"),
    path('addTag/', views.addTag, name="addTag"),
    path('<str:pk>/editTag/', views.editTag, name='editTag'),
    path('<str:pk>/deleteTag/', views.deleteTag, name='editTag'),
]
