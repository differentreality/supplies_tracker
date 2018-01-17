from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Space

class item_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    description = forms.CharField(label='Description', max_length=100, required=False)
    price_bought = forms.FloatField(label='How much does this cost to buy?')
    reimbursement = forms.FloatField(label='How much do you make? (Fill if you sell the items, or provide them against donation)', required=False)
    image = forms.ImageField(label='Photo', required=False)

class storage_form(forms.Form):
  name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
  image = forms.ImageField(label='Photo', required=False)

  def __init__(self, user, *args, **kwargs):
    super(storage_form, self).__init__(*args, **kwargs)
    if user is not None and user.id is not None:
        self.fields['space_id'] = forms.ModelChoiceField(label='Space',
                                                        queryset=Space.objects.filter(user_id=user.id),
                                                        empty_label= '(Please select)')

class space_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    address=forms.CharField(label='Address', max_length=50, required=False)
    description = forms.CharField(label='Description', max_length=100, required=False)
    image = forms.ImageField(label='Photo', required=False)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
