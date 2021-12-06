from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Profile


# Create your models here.
class Services(models.Model):
    name = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    price = models.FloatField()
    run_time = models.DateTimeField()
    orders = models.ForeignKey('Orders', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return str(self.name) + '\n\t' + str(self.text)


class Orders(models.Model):
    class KobunType(models.TextChoices):
        DO = 'DO', _('Do')
        INPROCESS = 'IN', _('In process')
        DONE = 'DN', _('Done')

    name = models.CharField(max_length=255)
    service = models.OneToOneField(Services, on_delete=models.SET_NULL, null=True, related_name='+')
    customer = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True, related_name='+')
    executor = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True, related_name='+')
    koban_type = models.CharField(max_length=2, choices=KobunType.choices, default=KobunType.DO)
    data_start = models.DateTimeField(auto_now_add=True)
    data_end = models.DateTimeField()
    text = models.TextField()
    comments = models.ForeignKey('OrderComments', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return f'Order {self.name}' \
               f'\n\tCustomer: {self.customer}' \
               f'\n\tExecutor: {self.executor}'


class OrderComments(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    order = models.OneToOneField(Orders, on_delete=models.SET_NULL, null=True)


    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return str(self.title) + '\n\t' + str(self.text)
