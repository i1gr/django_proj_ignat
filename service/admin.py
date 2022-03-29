from django.contrib import admin
from service.models import Services, Orders, OrderComments


class ServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.
admin.site.register(Services, ServicesAdmin)
admin.site.register(Orders)
admin.site.register(OrderComments)
