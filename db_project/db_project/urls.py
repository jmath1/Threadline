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
from django.urls import include, path

urlpatterns = [    
    path("hood/", include("main.urls.hood")),
    path("block/", include("main.urls.block")), 
    path("user/", include("main.urls.user")),
    path("thread/", include("main.urls.thread")),
    path("notifications/", include("main.urls.notifications")),
    
    # path("admin/", admin.site.urls),
]
