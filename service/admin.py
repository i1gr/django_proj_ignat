from django.contrib import admin
from service.models import Services, Orders, OrderComments

# Register your models here.
admin.site.register(Services)
admin.site.register(Orders)
admin.site.register(OrderComments)