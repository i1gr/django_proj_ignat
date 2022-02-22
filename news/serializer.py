from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('title', 'slug', 'datetime', 'author', 'text', 'stars', 'absolute_url')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
