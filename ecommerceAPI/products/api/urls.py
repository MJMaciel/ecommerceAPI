from django.urls import include, path
from rest_framework import routers

from products.api import views


router = routers.SimpleRouter()
router.register('products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]