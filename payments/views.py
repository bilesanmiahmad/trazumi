from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import CartSerializer, CartItemSerializer, CartContainerSerializer, TransactionSerializer
import utils.bot_messaging as bot
from accounts.models import Profile
from .models import Cart, CartItem


def testbot(request):
    # runbot
    # pelumi_chat_id = 437599023
    # harold_chat_id = 743071488

    chat_id = 786206902
    message = "New message from within Trazumi Django!"
    # message = "Hi Harold! Testing sending messages from within Trazumi Django..."
    payload = bot.send_message(text=message)
    bot.update_profile()

    profile = Profile.objects.get(telegram_username='Gbolz')

    print('something something whatever ...')

    context = {
        'profile': profile
    }

    return render(request, 'testbot.html', context=context)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('date_created')
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all().order_by('cart')
    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]
