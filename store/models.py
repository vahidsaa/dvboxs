from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save 


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(user, auto_now=True)
    phone = models.CharField(max_length=11, blank=True, verbose_name='تلفن')
    city =  models.CharField(max_length=50, blank=True, verbose_name='شهر')
    address1 = models.TextField(max_length=1300, blank=True, verbose_name='ادرس')
    old_cart = models.CharField(max_length=300, blank=True, null=True, verbose_name='سبد خرید')

    def __str__(self):
        return self.user.username


#create profile when user sign up 
def create_profile(sender, instance, created, **kwargs):

    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)




class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/category/')
    alt = models.CharField(max_length=60, null=True, blank=True)
    description_up =  models.CharField(max_length=250, default='', blank=True, null=True)
    description = models.CharField(max_length=550, default='', blank=True, null=True)
    description_sub =  models.CharField(max_length=250, default='', blank=True, null=True)
    shop_page = models.BooleanField(default=False)
    show_page = models.BooleanField(default=False)
    amade_page = models.BooleanField(default=False)
    nemone_page = models.BooleanField(default=False)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'دسته بندی'



# must add discrption for product
class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    discrption = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    alt = models.CharField(max_length=60, null=True, blank=True)
    status= models.BooleanField(default=True)
    off = models.BooleanField(default=False, verbose_name='تخفیفی')
    is_posti = models.BooleanField(default=False, verbose_name='پستی')
    is_tape = models.BooleanField(default=False, verbose_name='چسب')
    is_ready = models.BooleanField(default=False, verbose_name='جعبه اماده')




    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'محصولات فروشی'





class ProductChoose(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='uploads/product_di/')
    alt = models.CharField(max_length=60, null=True, blank=True)
    daroyi = models.BooleanField(default=False, verbose_name='دارویی')
    mamoli = models.BooleanField(default=False, verbose_name='معمولی')
    pitzayi = models.BooleanField(default=False, verbose_name='پیتزایی')
    sini = models.BooleanField(default=False, verbose_name='سینی')
    snack = models.BooleanField(default=False, verbose_name='اسنک')
    tahghofli = models.BooleanField(default=False, verbose_name='ته قفلی')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'نمونه دایکاتی ها'


