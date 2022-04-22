from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('', include("issues_manager.urls")),

    path('', include('users.urls')) # à quoi servirai namespace = 'users' ?
    
   
] 