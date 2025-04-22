from django.contrib import admin
from django.urls import path
from store import views
from .views import signup,login, productdetail,add_to_cart# Ensure signup view is imported


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('product-detail/<int:pk>', views.productdetail, name='product-detail'),
    path('logout/', views.logout, name='logout'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('show_cart', views.show_cart, name='show_cart'),
    path('plus_cart', views.plus_cart, name='plus_cart'),
    path('minus_cart', views.minus_cart, name='minus_cart'),
    path('remove_cart', views.remove_cart, name='remove_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('order/', views.order, name='order'),
    path('search/', views.search, name='search'),

 



    # path('category/<slug:slug>/', category_view, name='category_detail'),

]
