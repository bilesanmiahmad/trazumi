from rest_framework import serializers
from .models import Brand, Store, Product
from accounts.models import User, Address
from accounts.serializers import UserSerializer

class BrandSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'created_by', 'created', 'updated']
    
    def create(self, validated_data):
        name = validated_data.get('name', None)
        brand = Brand(name=name)
        return brand



class StoreSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    address = Address()
    created_by = UserSerializer()
    class Meta:
        model = Store
        fields = ['id', 'brand', 'address', 'created_by', 'created', 'updated']
    
    def create(self, validated_data):
        name = validated_data.get('name', None)
        line1 = validated_data.get('line1', None)
        line2 = validated_data.get('line2', None)
        lga = validated_data.get('lga', None)
        town = validated_data.get('town', None)
        city = validated_data.get('city', None)
        state = validated_data.get('state', None)


class ProductSerializer(serializers.ModelSerializer):
    owner = StoreSerializer()
    created_by = UserSerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'owner', 'selling_price', 'created_by', 'created', 'updated']
