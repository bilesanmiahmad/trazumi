"""marketpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import UserViewSet
from inventory.views import BrandViewSet, StoreViewSet, ProductViewSet, index


router = DefaultRouter()
router.register(r'accounts', UserViewSet)
router.register(r'brands', BrandViewSet, 'brands')
router.register(r'stores', StoreViewSet, 'stores')
router.register(r'products', ProductViewSet, 'products')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('home/', index),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
