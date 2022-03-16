from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from products.api.serializers import ProductSerializer
from products.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]