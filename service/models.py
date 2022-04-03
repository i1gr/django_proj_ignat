from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from users.models import Profile


# Create your models here.
class Services(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    price = models.FloatField()
    run_time = models.DurationField(null=True)

    class Meta:
        ordering = ["-price"]

    def __str__(self):
        return str(self.name) + '\n\t' + str(self.text)

    def get_absolute_url(self):
        return reverse(viewname='make_order', kwargs={'service_slug': self.slug})


class Orders(models.Model):
    class KanbanType(models.TextChoices):
        DO = 'DO', _('Do')
        INPROCESS = 'IN', _('In process')
        DONE = 'DN', _('Done')
        ARCHIVE = 'AR', _('Archive')

    name = models.CharField(max_length=255)
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Profile, related_name='customer', on_delete=models.SET_NULL, null=True)
    executor = models.ForeignKey(Profile, related_name='executor', on_delete=models.SET_NULL, null=True)
    kanban_type = models.CharField(max_length=2, choices=KanbanType.choices, default=KanbanType.DO)
    data_start = models.DateTimeField(auto_now_add=True)
    data_end = models.DateTimeField(null=True)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    is_question = models.BooleanField(default=False)

    class Meta:
        ordering = ["-data_start"]

    def __str__(self):
        return f'Order {self.name}' \
               f'\n\tCustomer: {self.customer}' \
               f'\n\tExecutor: {self.executor}'

    def get_absolute_url(self):
        return reverse(viewname='order', kwargs={'order_id': self.pk})


class OrderComments(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    order = models.ForeignKey(to='Orders', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return str(self.text)
