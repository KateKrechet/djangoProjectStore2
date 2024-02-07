from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput

from .models import *

class Signupform(UserCreationForm):
    username = forms.CharField(label='логин', help_text='')
    password1 = forms.CharField(label='пароль', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='подтверждение', help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    email = forms.EmailField(label='почта', widget=forms.TextInput(attrs={'placeholder': 'qwe@mail.ru'}))
    first_name = forms.CharField(label='имя', max_length=20)
    last_name = forms.CharField(label='фамилия', max_length=20, required=False)

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='Количество:',choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email','address', 'delivery', 'phone']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Имя'}),
            'email':TextInput(attrs={'placeholder': 'qwerty@mail.ru'}),
            'address':TextInput(attrs={'placeholder': 'улица Ленина, д.1, кв.1'}),
            'phone':TextInput(attrs={'placeholder': '+7**********'}),
        }

