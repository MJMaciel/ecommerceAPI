from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.api.serializers import OrderSerializer, OrderDetailSerializer, OrderDetailReadSerializer
from orders.models import Order, OrderDetail
from products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'delete']

    def destroy(self, request, pk=None):
        order = get_object_or_404(self.queryset, pk=pk)
        order_details = OrderDetail.objects.filter(order=order)
        for od in order_details:
            product = od.product
            product.stock += od.quantity
            product.save()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    # def list(self, request):
    #     serializer = OrderDetailReadSerializer(self.queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        product_queryset = Product.objects.all()
        product = get_object_or_404(product_queryset, pk=request.data['product'])
        if product.stock < request.data['quantity']:
            raise ValidationError('There is not enough stock of the product.')
        product.stock -= request.data['quantity']
        product.save()
        serializer = OrderDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        order_detail = get_object_or_404(self.queryset, pk=pk)
        product = order_detail.product
        new_product = Product.objects.get(id=request.data['product'])
        if new_product.stock < request.data.get('quantity'):
            raise ValidationError('There is not enough stock of the new product.')
        product.stock += order_detail.quantity
        product.save()
        new_product.stock -= request.data['quantity']
        new_product.save()
        serializer = OrderDetailSerializer(instance=order_detail, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, pk=None):
        order_detail = get_object_or_404(self.queryset, pk=pk)
        product = order_detail.product
        if request.data.get('quantity') != None and request.data.get('product') != None:
            new_product = Product.objects.get(id=request.data['product'])
            if new_product.stock < request.data.get('quantity'):
                raise ValidationError('There is not enough stock of the new product.')
            product.stock += order_detail.quantity
            product.save()
            new_product.stock -= request.data['quantity']
            new_product.save()
        elif request.data.get('quantity') != None:
            quantity_diff = order_detail.quantity - request.data['quantity']
            if quantity_diff < 0 and product.stock < abs(quantity_diff):
                raise ValidationError('There is not enough stock of the product.')
            product.stock += quantity_diff
            product.save()
        elif request.data.get('product') != None:
            new_product = Product.objects.get(id=request.data['product'])
            if new_product.stock < order_detail['quantity']:
                raise ValidationError('There is not enough stock of the new product.')
            product.stock += order_detail.quantity
            product.save()
            new_product.stock -= order_detail.quantity
            new_product.save()
        serializer = OrderDetailSerializer(instance=order_detail, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        order_detail = get_object_or_404(self.queryset, pk=pk)
        product = order_detail.product
        product.stock += order_detail.quantity
        product.save()
        order_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)