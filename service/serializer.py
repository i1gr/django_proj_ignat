from rest_framework import serializers
from .models import Services


class ServicesSerializerWithoutOrders(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Services
        fields = ('name', 'slug', 'price', 'text', 'run_time', 'absolute_url')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
