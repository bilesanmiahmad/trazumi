from rest_framework import serializers
from .models import Brand, Store, Product
from accounts.models import User, Address
from accounts.serializers import UserSerializer

class BrandSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        model = Brand
        fields = ['id', 'name', 'created_by', 'created', 'updated']



class StoreSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    address = Address()
    created_by = UserSerializer()
    class Meta:
        model = Store
        fields = ['id', 'brand', 'address', 'created_by', 'created', 'updated']


class ProductSerializer(serializers.ModelSerializer):
    owner = StoreSerializer()
    created_by = UserSerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'owner', 'selling_price', 'created_by', 'created', 'updated']
