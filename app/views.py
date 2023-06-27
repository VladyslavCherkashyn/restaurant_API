from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Restaurant, Menu, Vote
from .serializers import (
    CreateRestaurantSerializer,
    UploadMenuSerializer,
    RestaurantListSerializer,
    MenuListSerializer,
    ResultMenuListSerializer, VoteCreateSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RestaurantListSerializer
        return CreateRestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = UploadMenuSerializer


class CurrentDayMenuView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuListSerializer

    def get_object(self):
        today = timezone.now().date()
        return get_object_or_404(self.queryset, date=today)


class CurrentDayResultsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Menu.objects.all()
    serializer_class = ResultMenuListSerializer

    def list(self, request, *args, **kwargs):
        today = timezone.now().date()
        queryset = self.get_queryset().filter(date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VoteCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteCreateSerializer

    def create(self, request, *args, **kwargs):
        menu_id = request.data.get('menu_id')

        try:
            menu = Menu.objects.get(id=menu_id)
        except ObjectDoesNotExist:
            return Response({'detail': 'Menu does not exist'}, status=status.HTTP_404_NOT_FOUND)

        employee = request.user
        Vote.objects.create(employee=employee, menu=menu)

        # Increment the vote count for the menu
        menu.votes = F('votes') + 1
        menu.save()

        todays_date = menu.created_at.date()
        qs = Menu.objects.filter(created_at__date=todays_date)
        serializer = MenuListSerializer(qs, many=True)
        res = {
            "msg": 'You voted successfully!',
            "data": serializer.data,
            "success": True
        }
        return Response(data=res, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        print('Creating Vote:', serializer.validated_data)

        super().perform_create(serializer)

        print('Created Vote:', serializer.data)
