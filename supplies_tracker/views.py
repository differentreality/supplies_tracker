# from hamlpy.views.generic import HamlExtensionTemplateView
from django.shortcuts import render

def item_list(request):
  return render(request, 'items/index.html.haml', {})
