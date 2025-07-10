from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views.CustomUserViewSet import CustomUserViewSet
from myapp.views.AppViewSet import AppViewSet




router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'apps',AppViewSet,basename='apps')

urlpatterns = [
    path('', include(router.urls)),
]