from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class item_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', max_length=100)

class storage_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)


class space_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    address=forms.CharField(label='Address', max_length=100)
    description = forms.CharField(label='Description', max_length=100)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



