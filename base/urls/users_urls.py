from django.urls import path
from ..views import users_view as views

urlpatterns = [
    path('', views.getUsers, name="users"),
    path('login/', views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('register/', views.registerUser, name="register"),
    path('profile/', views.getUserProfile, name="user-profile"),
    path('profile/update/', views.updateUserProfile, name="user-profile-update"),
    path('withdraws/', views.getUserWithdraws, name="user-withdraws"),
    path('withdraws/create', views.createWithdraw, name="user-withdraws-create"),
    path('products/', views.getUserProducts, name="user-products"),
    path('shop/', views.getShopInfos, name="shop"),

]
