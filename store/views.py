from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from .forms import *
from django.views.decorators.http import require_POST
from .cart import Cart


# Create your views here.
# def index(req):
#     return render(req, 'index.html')
# страница со всеми продуктами
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    data = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'store/product_list.html', data)


# страница с выбранным продуктом
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    data = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'store/product_detail.html', data)


# регистрация пользователя
def registration(req):
    if req.POST:
        user_form = Signupform(req.POST)
        if user_form.is_valid():
            user_form.save()
            login = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            name = user_form.cleaned_data.get('first_name')
            surname = user_form.cleaned_data.get('last_name')
            mail = user_form.cleaned_data.get('email')
            # сохраняем нового пользователя
            user = authenticate(username=login, password=password)
            # найдем нового пользователя
            man = User.objects.get(username=login)
            # заполним поля в таблице auth_user
            man.email = mail
            man.first_name = name
            man.last_name = surname
            man.save()
            # находим группу зарегистрированных пользователей
            group = Group.objects.get(id=1)
            # добавляем нового человека в группу зарегистрированных пользователей
            group.user_set.add(man)
            return redirect('home')
    else:
        user_form = Signupform()
    data = {'regform': user_form}
    return render(req, 'registration/registration.html', context=data)


# добавление товара в корзину
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')


# удаление товара из корзины
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


# отображение текущей корзины
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

    return render(request, 'cart/cart_detail.html', {'cart': cart})
