from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Restaurant, Menu, Vote
from .serializers import (
    CreateRestaurantSerializer,
    UploadMenuSerializer,
    RestaurantListSerializer,
    MenuListSerializer,
    ResultMenuListSerializer,
    VoteCreateSerializer,
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
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to vote.")

        menu_id = int(request.data.get('menu_id'))

        try:
            menu = Menu.objects.get(id=menu_id)
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'Menu does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        employee = request.user

        # Check if the user has already voted today for the same menu
        todays_date = timezone.now().date()
        has_voted = Vote.objects.filter(
            employee=employee,
            menu=menu,
            voted_at__date=todays_date
        ).exists()

        if has_voted:
            res = {
                "msg": 'You already voted today!',
                "data": None,
                "success": False
            }
            return Response(data=res, status=status.HTTP_200_OK)

        # Create a new vote
        Vote.objects.create(employee=employee, menu=menu)

        # Increment the vote count for the menu
        menu.votes = F('votes') + 1
        menu.save()

        qs = Menu.objects.filter(created_at__date=todays_date)
        serializer = MenuListSerializer(qs, many=True)
        res = {
            "msg": 'You voted successfully!',
            "data": serializer.data,
            "success": True
        }
        return Response(data=res, status=status.HTTP_200_OK)
