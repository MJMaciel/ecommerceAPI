from rest_framework import serializers

from orders.api.functions import get_dollar_price
from orders.models import Order, OrderDetail
from products.api.serializers import ProductSerializer


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = ('__all__')


class OrderDetailReadSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = OrderDetail
        fields = ('__all__')


class OrderSerializer(serializers.ModelSerializer):
    
    order_details = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    total_usd = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('__all__')

    def get_order_details(self, obj):
        queryset = OrderDetail.objects.filter(order=obj)
        serializer = OrderDetailReadSerializer(queryset, many=True)
        return serializer.data

    def get_total(self, obj):
        queryset = OrderDetail.objects.filter(order=obj)
        return sum(order_detail.product.price * order_detail.quantity for order_detail in queryset)

    def get_total_usd(self, obj):
        dollar_price = get_dollar_price()
        if dollar_price == None:
            return None    
        return self.get_total(obj) / dollar_price
        

