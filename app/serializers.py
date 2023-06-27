from django.utils import timezone
from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Restaurant, Menu, Vote


class CreateRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'name',
            'address',

        ]
        model = Restaurant


class UploadMenuSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        menu = Menu(
            menu=validated_data['menu'],
            restaurant=validated_data['restaurant'],
            date=timezone.now().date()
        )
        menu.save()
        return menu

    class Meta:
        fields = [
            'restaurant',
            'menu',
        ]
        model = Menu


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuListSerializer(serializers.ModelSerializer):

    restaurant = serializers.CharField(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


class ResultMenuListSerializer(serializers.ModelSerializer):

    restaurant = serializers.CharField(read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id',
            'menu',
            'restaurant',
            'votes',
            'created_at'
        ]


class VoteCreateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())

    class Meta:
        model = Vote
        fields = ['employee', 'menu']
