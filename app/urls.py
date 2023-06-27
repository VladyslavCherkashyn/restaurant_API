from django.urls import path, include
from rest_framework import routers
from .views import (
    RestaurantViewSet,
    MenuViewSet,
    CurrentDayMenuView,
    CurrentDayResultsView,
    VoteCreateView
)

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'current-day-menu', CurrentDayMenuView, basename='current-day-menu')
router.register(r'current-day-results', CurrentDayResultsView, basename='current-day-results')
router.register(r'vote', VoteCreateView, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "app"
