from django.utils import timezone
from rest_framework import serializers

from .models import Menu, Restaurant


class CreateRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = [
            'name',
            'address',
        ]


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
        model = Menu
        fields = [
            'restaurant',
            'menu',
        ]


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'address'
        ]


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
            'menu',
            'restaurant',
            'votes',
            'created_at'
        ]


class VoteCreateSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    employee = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
