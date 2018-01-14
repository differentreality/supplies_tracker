from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class item_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    description = forms.CharField(label='Description', max_length=100, required=False)
    price_bought = forms.FloatField(label='How much does this cost to buy?')
    reimbursement = forms.FloatField(label='How much do you make? (Fill if you sell the items, or provide them against donation)')
    image = forms.ImageField(label='Add a photo of Item', required=False)

class storage_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    image = forms.ImageField(label='Add a photo of Storage', required=False)

class space_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    address=forms.CharField(label='Address', max_length=50, required=False)
    description = forms.CharField(label='Description', max_length=100, required=False)
    image = forms.ImageField(label='Add a photo of Space', required=False)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
