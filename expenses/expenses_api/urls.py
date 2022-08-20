
from django.urls import path
from expenses_api import views

urlpatterns = [
    path('', views.login),
    path('add/', views.add),
    path('display/', views.display,name='display'),
    path('analysis/', views.analysis),
    path('remove/', views.remove),
    path('sort/', views.sort),
    path('search/', views.search),
    path('view_item/', views.view_item),
    path('login/', views.login),
    
]
