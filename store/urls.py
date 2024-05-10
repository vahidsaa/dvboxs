from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('update_password/', views.update_password, name='update_password'),
    path('product/<int:pk>/', views.products_show, name='product_show'),
    path('product_amade/', views.product_amade, name='product_amade'),
    path('product_nemone/', views.product_nemone, name='product_nemone'),
    path('product-shop/<int:pk>/', views.products_shop, name='product_shop'),
    path('search/', views.search, name='search'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('bime/', views.bime, name='bime'),
    path('amozesh/', views.amozesh, name='amozesh'),
    path('amozesha/', views.amozesha, name='amozesha'),
    path('amozeshb/', views.amozeshb, name='amozeshb'),
    path('amozeshc/', views.amozeshc, name='amozeshc'),
    # path('amozeshd/', views.amozeshd, name='amozeshd'),
    path('sabt/', views.sabt, name='sabt'),


]
