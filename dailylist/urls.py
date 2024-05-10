from . import views
from django.urls import path




urlpatterns = [

    path('today_list/', views.today_list, name='today_list'),

]
