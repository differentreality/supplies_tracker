# from hamlpy.views.generic import HamlExtensionTemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Item
from .forms import item_form

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
