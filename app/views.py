from rest_framework import generics, status
from rest_framework.response import Response

from .models import Restaurant, Menu, Employee, Vote
from .serializers import RestaurantSerializer, MenuSerializer, EmployeeSerializer, VoteSerializer
import datetime


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CurrentDayMenuView(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_object(self):
        today = datetime.date.today()
        return self.queryset.get(date=today)


class CurrentDayResultsView(generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_object(self):
        today = datetime.date.today()
        return self.queryset.get(date=today)


class VoteListCreateView(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
