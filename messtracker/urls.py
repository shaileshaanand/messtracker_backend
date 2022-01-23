"""messtracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import include
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import os

import mess.urls

schema_view = get_schema_view(
    openapi.Info(
        title="Messtracker API",
        default_version="v1",
        description="",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=os.environ.get("BASE_URL"),
)

urlpatterns = [
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls")),
    path("api/mess/", include("mess.urls")),
]
# urlpatterns += mess.urls.router.urls
