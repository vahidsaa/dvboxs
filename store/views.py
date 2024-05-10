from django.shortcuts import render, redirect
from store.models import Category, Product, ProductChoose, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from store.forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

#search psql
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank



from django.contrib.auth.models import User
from django.db.models import Q
import json
from cart.cart import Cart


def home(request):
    category_shop = Category.objects.filter(shop_page=True)
    category_show = Category.objects.filter(show_page=True)
    category_amade = Category.objects.filter(amade_page=True)
    category_nemone = Category.objects.filter(nemone_page=True)
    off = Product.objects.filter(off=True)

    context = {'category_shop': category_shop, 'category_show' : category_show, 'category_amade' : category_amade, 'category_nemone': category_nemone,'off':off}
	
    return render(request, 'store/home.html', context=context)



def shop(request):
	
	posti = Product.objects.filter(is_posti=True)
	tape =  Product.objects.filter(is_tape=True)
	amade =  Product.objects.filter(is_ready=True)

	return render(request, 'store/shop.html', {'posti': posti, 'tape': tape, 'amade' : amade})


def products_show(request, pk):

	product_show = Category.objects.get(id=pk)
	# posti = Category.objects.get(id=1)
	# chap = Category.objects.get(id=7)
	# ready = Category.objects.get(id=2)

	return render(request, 'store/product_show.html', {'product_show' : product_show})


def product_amade(request):
    return render(request, 'store/product_amade.html', {})

def product_nemone(request):
    products = ProductChoose.objects.all()
    return render(request, 'store/product_nemone.html', {'products':products})


def products_shop(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product_shop.html', {'product' : product})








def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ('خوش آمدید'))
            return redirect('home')
        else:
            messages.success(request, ('اطلاعات وارد شده اشتباه است دوباره امتحان کنید'))
            return redirect('login')
    else:

        return render(request, 'store/login.html', {})



def logout_user(request):
    logout(request)
    messages.success(request, (' از حسابت خارج شدی'))
    return redirect('home')




def register_user(request):

    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('تکمیل اطلاعات (اختیاری)'))
            return redirect('update_info')
        else:
            messages.success(request, ('اطلاعات وارد شده اشتباه است دوباره امتحان کنید'))
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})
    

# def update_user(request):
#     if request.user.is_authenticated:
#         current_user = User.objects.get(id=request.user.id)
#         user_form = UpdateUserForm(request.POST or None, instance=current_user)
#         if user_form.is_valid():
#             user_form.save()
#             login(request, current_user)
#             messages.success(request, ('بروزرسانی انجام شد.'))
#             return redirect('home')
#         return render(request, 'store/update_user.html', {'user_form':user_form})
#     else:
#         messages.success(request, ('ابتدا وارد اکانت بشوید .'))
#         return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ('رمز عبور با موفقیت تغییر کرد'))
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'store/update_password.html', {'form':form})

    else:
        messages.success(request, ('ابتدا وارد اکانت بشوید .'))
        return redirect('home')

    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        current_userr = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_userr)

        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid() or user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, ('اطلاعات جدید ثبت شد.'))
            return redirect('home')
        return render(request, 'store/update_info.html', {'form':form, 'user_form':user_form})
    else:
        messages.success(request, ('ابتدا وارد اکانت بشوید .'))
        return redirect('home')


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        vector = SearchVector('name', 'discrption', 'alt')
        query = SearchQuery(searched)
        searched = Product.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.0001).order_by('-rank')
        # searched = Product.objects.filter(Q(name__icontains=searched) | Q(discrption__icontains=searched))
        return render(request, 'store/search.html', {'searched':searched})
    else:
        return render(request, 'store/search.html', {})



def aboutus(request):
    return render(request, 'store/aboutus.html', {})


def bime(request):
    return render(request, 'store/bime.html', {})



def amozesh(request):
    return render(request, 'store/amozesh.html', {})



def amozesha(request):
    return render(request, 'store/amozesha.html', {})


def amozeshb(request):
    return render(request, 'store/amozeshb.html', {})


def amozeshc(request):
    return render(request, 'store/amozeshc.html', {})


# def amozeshd(request):
#     return render(request, 'store/amozeshd.html', {})


def sabt(request):
    return render(request, 'store/sabt.html', {})


