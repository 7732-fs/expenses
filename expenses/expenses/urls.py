
from django.contrib import admin
from django.urls import include, path
from expenses_api import views


urlpatterns = [
    path('', views.display),
    path('admin/', admin.site.urls),
    path('expenses/', include('expenses_api.urls')),
]
