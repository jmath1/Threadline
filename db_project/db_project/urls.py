"""
URL configuration for db_project project.

The `urlpatterns` list routes URLs to api. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function api
    1. Add an import:  from my_app import api
    2. Add a URL to urlpatterns:  path('', api.home, name='home')
Class-based api
    1. Add an import:  from other_app.api import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main import api

urlpatterns = [
    path("healthcheck", api.healthcheck),
    path("user/register/", api.ProfileRegisterView.as_view()),
    path("user/me/", api.MeGET.as_view()),
    path("user/login/", api.ProfileLogin.as_view()),
    path("user/logout/", api.logout),
    path("user/edit/", api.EditProfileView.as_view()),
    path("user/<int:user_id>/threads/", api.get_user_threads),
    
    path("users/neighbors/", api.get_user_neighbors),
    path("users/followers/", api.get_followers),    
    
    path("block/<int:block_id>/threads/", api.get_block_threads),
    path("block/<int:block_id>/members/", api.list_block_members),
    path("block/follows", api.get_block_follows),
    
    path("hood/<int:hood_id>/threads/", api.get_hood_threads),
    path("hood/<int:hood_id>/members/", api.list_hood_members),
    path("hood/follows/", api.get_hood_follows),
    path("thread/<int:thread_id>/", api.get_thread),

    path("threads/user/", api.get_user_threads),
    
    path("threads/hood/new/", api.get_new_hood_threads),
    path("threads/block/new/", api.get_new_block_threads),
    path("threads/user/new/", api.get_new_user_threads),
    
    path("notifications/", api.get_notifications),    
  
    #path("admin/", admin.site.urls),
]
