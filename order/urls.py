from . import views
from django.urls import path

urlpatterns = [
    path('', views.order, name='order'),
    path('checkout', views.checkout, name='checkout'),
    path('tayid', views.tayid, name='tayid')

]
