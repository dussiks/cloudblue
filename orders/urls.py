from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet


v1_router = DefaultRouter()
v1_router.register('orders', OrderViewSet, basename='orders')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
