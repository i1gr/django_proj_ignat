from rest_framework import serializers
from .models import Services, Orders


class ServicesSerializerWithoutOrders(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Services
        fields = ('name', 'slug', 'price', 'text', 'run_time', 'absolute_url')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class OrdersSerializer(serializers.ModelSerializer):
    koban_type_str = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('name', 'service', 'customer', 'executor',
                  'koban_type_str', 'data_start', 'data_end', 'text')

    def get_koban_type_str(self, obj):
        return obj.get_koban_type_display()
