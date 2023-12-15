from django.shortcuts import render, get_object_or_404
from .models import *
from store.forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.
def index(req):
    return render(req, 'index.html')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    data = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'store/product_list.html', data)

def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    data = {'product': product}
    return render(request,'store/product_detail.html',data)

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Вход выполнен!')
#                 else:
#                     return HttpResponse('Аккаунт больше не активен!')
#             else:
#                 return HttpResponse('Пользователя с таким именем или паролем не существует!')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})
