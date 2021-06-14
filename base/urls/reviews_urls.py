from django.urls import path
from ..views import products_views as views

urlpatterns = [
    path('<str:pk>/', views.getReviews, name="reviews"),
    path('add/', views.addReview, name="addReview"),
    path('<str:pk>/delete', views.deleteReview, name="product"),
    path('<str:pk>/edit', views.editReview, name="product"),

]
