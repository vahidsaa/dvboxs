from django.contrib import admin
from store.models import Category, Product, ProductChoose, Profile
from django.contrib.auth.models import User



admin.site.register(Category)

admin.site.register(ProductChoose)


class ProfileInLine(admin.StackedInline):
    model = Profile



class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInLine]
    list_display = ('id', 'username', 'first_name', 'last_name')

admin.site.unregister(User)


admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'old_cart', 'date_modified')
    ordering = ['-date_modified']



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'sale_price')

