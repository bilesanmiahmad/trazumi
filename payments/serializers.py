from rest_framework import serializers
from .models import Cart, CartItem, Transaction
from inventory.models import Product
from accounts.models import User
from accounts.serializers import UserSerializer
from inventory.serializers import ProductSerializer, ProductOutputSerializer


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('__all__')

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    product = ProductOutputSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity', 'date_created', 'date_updated')

class CartContainerSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = CartSerializer

class TransactionSerializer(serializers.ModelSerializer):
    pass
