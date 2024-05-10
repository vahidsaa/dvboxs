from django.contrib import admin
from django.contrib.auth.models import User
from .models import Order, OrderItem

admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'id')

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]
    list_display = ['full_name', 'id','phone', 'amount_paid', 'tayid', 'bayane', 'ersal']


admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
