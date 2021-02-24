from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Brand, Store, Product
from .serializers import BrandSerializer, StoreSerializer, ProductSerializer
from accounts.permissions import IsAdminUser

# Create your views here.
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]

    @action(methods=['post'], detail=False, url_path='create-brand', permission_classes=[IsAdminUser])
    def create_brand(self, request):
        name = request.data.get('name', None)
        logo = request.data.get('logo', None)
        user = request.user
        brand = Brand.objects.create(name=name, logo=logo, created_by=user)
        if brand:
            serializer = BrandSerializer(brand)
            return Response(
                {
                    'results': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'errors': 'Something went wrong'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAdminUser]

    @action(methods=['post'], detail=False, url_path='create-store', permission_classes=[IsAdminUser])
    def create_store(self, request):
        pass