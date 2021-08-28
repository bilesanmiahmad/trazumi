from rest_framework import serializers
from .models import Brand, Store, Product
from accounts.models import User, Address
from accounts.serializers import UserSerializer, AddressSerializer

class BrandSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo', 'created_by', 'created', 'updated']
    
    # def create(self, validated_data):
    #     name = validated_data.get('name', None)
    #     brand = Brand(name=name)
    #     return brand



class StoreSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    name = serializers.CharField(write_only=True)
    line_1 = serializers.CharField(write_only=True)
    line_2 = serializers.CharField(write_only=True, allow_blank=True)
    lga = serializers.CharField(write_only=True)
    town = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)

    class Meta:
        model = Store
        fields = ['id', 'brand', 'address', 'created_by', 'created', 'updated', 'name', 'line_1', 'line_2', 'lga', 'town', 'city', 'state']
        read_only_fields = ['address', 'created_by', 'brand']
    
    def create(self, validated_data):
        name = validated_data.get('name', None)
        line1 = validated_data['line_1']
        line2 = validated_data.get('line_2', None)
        lga = validated_data.get('lga', None)
        town = validated_data.get('town', None)
        city = validated_data.get('city', None)
        state = validated_data.get('state', None)
        
        address = Address.objects.create(line_1=line1, line_2=line2, town=town, state=state, lga=lga)
        brand = Brand.objects.get(name=name)
        if not brand:
            raise serializers.ValidationError("This brand name does not exist")
        store = Store(brand=brand, address=address)
    
        return store


class ProductSerializer(serializers.ModelSerializer):
    owner = StoreSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    store_id  = serializers.CharField(write_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'owner', 'image', 'cost_price', 'selling_price', 'created_by', 'created', 'updated', 'store_id']
    
    def create(self, validated_data):
        name = validated_data.get('name', None)
        cost_price = validated_data.get('cost_price', None)
        selling_price = validated_data.get('selling_price', None)
        store_id = validated_data.get('store_id', None)
        image = validated_data.get('image', None)
        store = Store.objects.get(id=int(store_id))
        if not store:
            raise serializers.ValidationError('The store provided does not exist')
        product = Product(name=name, owner=store, selling_price=selling_price, cost_price=cost_price, image=image)
        return product

class ProductOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'cost_price', 'selling_price')