from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from .forms import *
from django.views.decorators.http import require_POST
from .cart import Cart
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .tasks import order_created
from django.urls import reverse
import braintree


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


# вариант, при котором работают проверки формы, но нет учета стоимости доставки и персональной скидки
# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             # ищем стоимость доставки
#             delivery = request.POST.get('delivery')
#             delivery_cost = 0 if delivery == '0' else (100 if delivery == '1' else 200)
#             print(delivery, type(delivery))
#             print(delivery_cost)
#             # скидка зарегистрированных пользователей - 5%
#             if request.user.id:
#                 user_discount = 0.95
#             else:
#                 user_discount = 1
#             print(user_discount)
#             # itog1 = cart.get_total_price() * user_discount
#             # itog2 = itog1 + delivery_cost
#             # print(itog1, itog2)
#             for item in cart:
#                 OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
#                                          quantity=item['quantity'])
#             # очистка корзины
#             cart.clear()
#             return render(request, 'order/created.html', {'order': order})
#     else:
#         form = OrderCreateForm()
#     return render(request, 'order/create.html', {'cart': cart, 'form': form})

# через ajax-запрос учтена персональная скидка и стоимость доставки, но не работает проверка формы
@method_decorator(csrf_exempt, name='dispatch')
def order_create(request):
    cart = Cart(request)
    if request.POST:
        form = OrderCreateForm(request.POST)
        if request.POST.get('type') == 'for_cost':
            name = request.POST.get('cn')
            email = request.POST.get('email')
            addr = request.POST.get('addr')
            delivery = request.POST.get('delivery')
            phone = request.POST.get('phone')
            print(name, email, addr, delivery, phone)
            # order = Order.objects.create(name=name, email=email, address=addr, delivery=delivery, phone=phone)
            # стоимость доставки
            delivery_cost = 0 if delivery == '0' else (100 if delivery == '1' else 200)
            print(delivery_cost, type(delivery_cost))
            # скидка для заказчика - 5% для зарегистрированных пользователей
            if request.user.id:
                user_discount = 0.95
            else:
                user_discount = 1
            print(user_discount, type(user_discount))
            itog1 = int(cart.get_total_price() * user_discount)
            itog2 = itog1 + delivery_cost
            print(itog1, itog2)
            order = Order.objects.create(name=name, email=email, address=addr, delivery=delivery, phone=phone,
                                         amount=itog2)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'] * user_discount,
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            print(order.id)
            # асинхронная задача - отправление письма о заказе
            order_created.delay(order.id)
            # устанавливаем в сессии номер текущего заказа
            request.session['order_id'] = order.id

            return JsonResponse({'itog1': itog1, 'itog2': itog2, 'order_id': order.id})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})


# оплата успешна
def payment_done(request):
    return render(request, 'payment/done.html')


# оплата отменена
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


# обработка платежей
def payment_process(request):
    # получаем номер текущего заказа
    order_id = request.session.get('order_id')
    # извлекаем объект order для данного номера
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # одноразовый номер токена, сгенерированный
        # BrainTree за оплату. Он будет сгенерирован в
        # шаблон с использованием Braintree JavaScript SDK
        nonce = request.POST.get('payment_method_nonce', None)
        # создание транзакции
        result = braintree.Transaction.sale({
            # общая сумма на оплату учетом скидки клиента и доставки
            'amount': '{:.2f}'.format(order.amount),
            'payment_method_nonce': nonce,
            # транзакция автоматически передается на урегулирование
            'options': {
                'submit_for_settlement': True
            }
        })
        # Если транзакция успешно обработана
        if result.is_success:
            # помечаем заказ как оплаченный
            order.paid = True
            # сохраняем уникальный номер транзакции
            order.braintree_id = result.transaction.id
            order.save()
            # платеж прошел успещно
            return redirect('done')
        else:
            # оплата отменена
            return redirect('canceled')
    else:
        # генерировать токен, если представление было загружено GET-запросом
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})
