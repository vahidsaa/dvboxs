from django.db import models
from django.core.validators import RegexValidator
from store.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=11)
    addrees = models.TextField(max_length=15000)
    amount_paid = models.BigIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    tayid = models.BooleanField(default=False, verbose_name='تایید شده')
    bayane = models.BooleanField(default=False, verbose_name='پرداخت بیانه')
    ersal = models.BooleanField(default=False, verbose_name='ارسال شده')
    date_ersal = models.DateTimeField(blank=True, null=True)
    class Meta:
        verbose_name_plural = 'سفارش'

    def __str__(self):
        return f'سفارش, {str(self.id)}'
    
@receiver(pre_save, sender=Order)
def set_date_ersale(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.ersal and not obj.ersal:
            instance.date_ersal = now



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.BigIntegerField()

    class Meta:
        verbose_name_plural = 'جزيات سفارشات'

    def __str__(self):
        return f'جزیات سفارش - {str(self.id)}'
    


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex='^(\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')])
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = 'آدرس و تلفن'

    def __str__(self):
        return f'{self.full_name} - {str(self.id)}'
    
# def create_shipping(sender, instance, created, **kwargs):
#     if created:
#         user_shipping = ShippingAddress(user=instance)
#         user_shipping.save()

# post_save.connect(create_shipping, sender=User)