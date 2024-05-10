from django.shortcuts import render, redirect
from cart.cart import Cart
from store.forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from .forms import ShippingForms
from .models import Order , OrderItem
from django.contrib.auth.models import User
from store.models import Category, Product, ProductChoose, Profile
from django.contrib import messages


# Create your views here.
def order(request):
    
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        user_form = ShippingForms(request.POST or None)

        # form = UserInfoForm(request.POST or None, instance=current_userr)
        return render(request, 'order/order.html', {'cart_products' : cart_products, 'quantities': quantities, 'totals': totals, 'user_form':user_form})
    else:
        user_form = ShippingForms(request.POST or None)
        return render(request, 'order/order.html', {'cart_products' : cart_products, 'quantities': quantities, 'totals': totals, 'user_form':user_form})



def checkout(request):
    if request.POST:

        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        my_shiipping = request.POST
        request.session['my_shipping'] = my_shiipping

        
        if request.user.is_authenticated:
            return render(request, 'order/checkout.html', {'user_form_info':request.POST, 'cart_products':cart_products, 'quantities':quantities, 'totals':totals})

        else:
            return render(request, 'order/checkout.html', {'user_form_info':request.POST, 'cart_products':cart_products, 'quantities':quantities, 'totals':totals})



    else:
        messages.success(request, 'ابتدا محصول را در سبد اضافه کنید')
        return redirect('home')
    


def tayid(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    my_shipping = request.session.get('my_shipping')

    full_name =my_shipping['full_name']
    phone = my_shipping['phone']
    addrees = f"{my_shipping['city']}\n{my_shipping['address']}"
    amount_paid = totals

    if request.user.is_authenticated:
        user = request.user
        create_order = Order(user=user, full_name=full_name, phone=phone, addrees=addrees, amount_paid=amount_paid)
        create_order.save()

        order_id = create_order.pk
        for product in cart_products():
            product_id = product.id
            price = product.sale_price
            for key,value in quantities().items():
                if int(key) == product.id:
                    create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price,)
                    create_order_item.save()

        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]

        messages.success(request, 'سفارش تایید و ارسال شد')
        return redirect('sabt')
    else:
        create_order = Order(full_name=full_name, phone=phone, addrees=addrees, amount_paid=amount_paid)
        create_order.save()

        order_id = create_order.pk
        for product in cart_products():
            product_id = product.id
            price = product.sale_price
            for key,value in quantities().items():
                if int(key) == product.id:
                    create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price,)
                    create_order_item.save()

        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]
                
        messages.success(request, 'سفارش تایید و ارسال شد')
        return redirect('sabt')
    
