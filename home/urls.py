from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('product', views.product, name='product'),
    path('shop', views.shop, name='shop'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('contact', views.contact, name='contact'),
    path('logout', views.logout, name='logout'),
    path('manage_products', views.manage_products, name='manage_products'),
    path('add_product', views.add_product, name='add_product'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'), 
    path('disable/<int:id>', views.disable, name='disable'),
    path('view_product/<int:id>', views.view_product, name='view_product'),
    path('manage_staff', views.manage_staff, name='manage_staff'),
    path('manage_users', views.manage_users, name='manage_users'),

    path('add_staff', views.add_staff, name='add_staff'),
    path('delete_user/<int:id>&<str:username>', views.delete_user, name='delete_user'),  
    path('try_now/<int:id>', views.try_now, name='try_now'),  
    # path('buy_now/<int:id>&<str:username>&<str:name>&<int:price>', views.buy_now, name='buy_now'),
    path('buy_now', views.buy_now, name='buy_now'),
    path('contactUS', views.contactUS, name='contactUS'),
    path('delete_mess/<int:id>', views.delete_mess, name='delete_mess'),  
    path('orders', views.orders, name='orders'),  

]
