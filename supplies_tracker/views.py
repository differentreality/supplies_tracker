# from hamlpy.views.generic import HamlExtensionTemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Item,Storage,Space
from .forms import item_form
from .forms import storage_form
from .forms import space_form
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from supplies_tracker.forms import SignUpForm

def items_index(request):
  items = Item.objects.all()
  enum_items = enumerate(items)
  return render(request, 'items/index.html.haml', { 'enum_items': enum_items })

def items_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = item_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            obj = Item(**form.cleaned_data)
            obj.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/items')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = item_form()

    return render(request, 'items/new.html.haml', { 'form': form })

def storages_index(request):
  storages = Storage.objects.all()
  enum_storages = enumerate(storages)
  return render(request, 'storages/index.html.haml', { 'enum_storages': enum_storages })

def storages_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = storage_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            obj = Storage(**form.cleaned_data)
            obj.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/storages')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = storage_form()

    return render(request, 'storages/new.html.haml', { 'form': form })

def spaces_index(request):
  spaces = Space.objects.all()
  enum_spaces = enumerate(spaces)
  return render(request, 'spaces/index.html.haml', { 'enum_spaces': enum_spaces })

def spaces_new(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = space_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            obj = Space(**form.cleaned_data)
            obj.save()

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/spaces')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = space_form()

    return render(request, 'spaces/new.html.haml', { 'form': form })


def home(request):
    return render(request, 'home.html')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})