from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class item_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', max_length=100, required=False)
    price_bought = forms.FloatField(label='How much does this cost to buy?')
    reimbursement = forms.FloatField(label='How much do you make? (Fill if you sell the items, or provide them against donation)')

class storage_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)


class space_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    address=forms.CharField(label='Address', max_length=50, required=False)
    description = forms.CharField(label='Description', max_length=100, required=False)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
