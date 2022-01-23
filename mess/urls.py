from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.MessViewSet)


app_name = "mess"


urlpatterns = [path("", include(router.urls))]
