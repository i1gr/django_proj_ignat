from rest_framework import serializers
from .models import Services, Orders
from .services import is_user_read


class ServicesSerializerWithoutOrders(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Services
        fields = ('name', 'slug', 'price', 'text', 'run_time', 'absolute_url')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class OrdersSerializer(serializers.ModelSerializer):
    kanban_type_str = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    kanban_type = serializers.StringRelatedField()
    executor = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        allow_null=True,
     )
    customer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
     )
    is_user_read = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('name', 'service', 'customer', 'executor', 'kanban_type',
                  'kanban_type_str', 'data_start', 'data_end', 'text', 'url', "is_user_read")

    def get_kanban_type_str(self, obj):
        return obj.get_kanban_type_display()

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_is_user_read(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        return is_user_read(user, obj)
