from django.urls import include, path
from rest_framework import routers

from orders.api import views


router = routers.SimpleRouter()
router.register('orders', views.OrderViewSet)
router.register('order_detail', views.OrderDetailViewSet)


urlpatterns = [
    path('', include(router.urls)),
]