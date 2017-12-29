from django import forms

class item_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', max_length=100)

class storage_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', max_length=100)

class space_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    description = forms.CharField(label='Description', max_length=100)



