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
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import UserViewSet, ProfileViewSet, ProfileDetailView
from inventory.views import BrandViewSet, StoreViewSet, ProductViewSet, index
from payments.views import CartViewSet, CartItemViewSet


router = DefaultRouter()
router.register(r'accounts', UserViewSet)
router.register(r'brands', BrandViewSet, 'brands')
router.register(r'stores', StoreViewSet, 'stores')
router.register(r'products', ProductViewSet, 'products')
router.register(r'carts', CartViewSet, 'carts')
router.register(r'cartitems', CartItemViewSet, 'cart-items')
router.register(r'profiles', ProfileViewSet, 'profiles')
router.register(r'profiles/<int:profile_id>', ProfileViewSet, 'profiles')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('home/', index),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]


# Use include() to add paths from the payments application
urlpatterns += [
    path('payments/', include('payments.urls')),
    path('profiles/<int:profile_id>',ProfileDetailView.as_view() )
]

# Use static() to add URL mapping to serve static files during development (only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
