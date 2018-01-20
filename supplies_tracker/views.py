from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Item, Storage, Space, Items_Storage
from .forms import item_form, storage_form, space_form, SignUpForm, LoginForm, space_dropdown_form
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def items_index(request):
  items = Item.objects.all()
  return render(request, 'items/index.html.haml', { 'items': items })

class SpaceUpdate(UpdateView):
    model = Space
    fields = ['name', 'address', 'description','image']
    template_name = 'spaces/edit.html.haml'
    success_url = reverse_lazy('spaces_index')

class SpaceDelete(DeleteView):
    model = Space
    success_url = reverse_lazy('spaces_index')

class StorageUpdate(UpdateView):
    template_name = 'storages/edit.html.haml'
    model = Storage
    fields = ['name','image']
    success_url = reverse_lazy('storages_index')

class StorageDelete(DeleteView):
    model = Storage
    success_url = reverse_lazy('storages_index')

class ItemUpdate(UpdateView):
    model = Item
    fields = ['name', 'description', 'price_bought', 'reimbursement','image']
    template_name = 'items/edit.html.haml'
    success_url = reverse_lazy('items_index')

class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('items_index')

@login_required
def add_item(request, storage_id, item_id):
    storage = Storage.objects.get(id=storage_id)
    storage_items = storage.item.all()
    item = Item.objects.get(id=item_id)
    items_storage = item.items_storage_set.get(storage_id=storage_id)

    items_storage.quantity = int(items_storage.quantity or 0) + 1
    items_storage.save()
    return HttpResponseRedirect(reverse('storages_show', kwargs= {'storage_id': storage_id}))

def remove_item(request, storage_id, item_id):
    storage = Storage.objects.get(id=storage_id)
    storage_items = storage.item.all()
    item = Item.objects.get(id=item_id)
    items_storage = item.items_storage_set.get(storage_id=storage_id)

    if (items_storage.quantity > 0):
      items_storage.quantity = items_storage.quantity - 1
      items_storage.save()
    return HttpResponseRedirect(reverse('storages_show', kwargs= {'storage_id': storage_id}))

@login_required
def items_new(request):
    storage_id = request.GET['storage_id']
    if request.method == 'POST':
        form = item_form(request.POST,request.FILES)
        if form.is_valid():
            obj = Item(**form.cleaned_data)
            obj.user = request.user
            storage = request.GET['storage_id']
            obj.save()
            new_item = Items_Storage(storage=Storage.objects.get(id=storage), items=Item.objects.get(id=obj.id))
            new_item.save()

            return HttpResponseRedirect(reverse('storages_show', kwargs= {'storage_id': storage_id}))
    else:
        form = item_form()

    return render(request, 'items/new.html.haml', { 'form': form })

@login_required
def storages_index(request):
    user_spaces = Space.objects.filter(user_id=request.user.id)
    user_spaces_ids = user_spaces.values_list('id', flat=True)

    # If this is from the filter form (dropdown)
    if request.method == 'POST':
        selected_space_id = request.POST['space_id']
        if selected_space_id == 'all':
            storages = Storage.objects.filter(space_id__in=user_spaces_ids)
        else:
            storages = Storage.objects.filter(space_id=selected_space_id)
        if request.user is not None:
          form = space_dropdown_form(user = request.user)
          form.fields['space_id'].initial = selected_space_id

    # else this is the index
    else:
      storages = Storage.objects.filter(space_id__in=user_spaces_ids)
      if request.user is not None:
        form = space_dropdown_form(user = request.user)
      selected_space_id = None
    return render(request, 'storages/index.html.haml', { 'storages': storages,
                                                         'user_spaces': user_spaces,
                                                         'form': form ,
                                                         'selected_space_id': selected_space_id })

def storages_show(request, storage_id):
    try:
        storage = Storage.objects.get(id=storage_id)
        items = storage.item.all()

    except Storage.DoesNotExist:
        storage = None
        items = None

    if storage is None:
        return render(request, 'error.html.haml' )
    else:
      if request.user.is_authenticated:
        return render(request, 'storages/show.html.haml', { 'storage': storage, 'items': items })
      else:
        return render(request, 'storages/public.html.haml', { 'storage': storage, 'items': items })

@login_required
def storages_new(request, space_id=None):
    if space_id is None:
        space = None
    else:
        space = Space.objects.get(id=space_id)

    if request.method == 'POST':
        form = storage_form(None, request.POST,request.FILES)
        if form.is_valid():
            obj = Storage(**form.cleaned_data)
            if space_id is None:
              space_id = form.data.get('space_id')
              obj.space_id = space_id
            else:
              obj.space_id = space_id

            obj.save()

            return HttpResponseRedirect(reverse('spaces_show', args= space_id))
    else:
        if space_id is None:
          form = storage_form(user = request.user)
        else:
            form = storage_form(None,None)


    return render(request, 'storages/new.html.haml', { 'form': form , 'space': space })

@login_required
def spaces_index(request):
  spaces = Space.objects.filter(user_id=request.user.id)
  enum_spaces = enumerate(spaces)
  return render(request, 'spaces/index.html.haml', { 'enum_spaces': enum_spaces })

#@login_required
#def spaces_show(request, space_id):
 # space = Space.objects.get(id=space_id)
 # storages = Storage.objects.filter(space_id=space_id)
 # return render(request, 'spaces/show.html.haml', { 'space': space, 'storages': storages } )

def spaces_show(request,space_id):
    try:
        space = Space.objects.get(id=space_id)
        storages = Storage.objects.filter(space_id=space_id)

    except Space.DoesNotExist:
        space = None
        storages = None

    if space is None:
      return render(request, 'error.html.haml')
    else:
      return render(request, 'spaces/show.html.haml', {'space': space, 'storages': storages})

@login_required
def spaces_new(request):
    if request.method == 'POST':
        form = space_form(request.POST,request.FILES)
        if form.is_valid():
            obj = Space(**form.cleaned_data)
            obj.user = request.user
            obj.save()

            return HttpResponseRedirect('/spaces')
    else:
        form = space_form()

    return render(request, 'spaces/new.html.haml', { 'form': form })

def home(request):
    search_keyword = request.GET.get('search-keyword')
    search_results = None
    if search_keyword is not None:
        results = Space.objects.filter(Q(name__contains=search_keyword)|
                                       Q(description__contains=search_keyword)|
                                       Q(address__contains=search_keyword))
        results2 = Storage.objects.filter(Q(name__contains=search_keyword))
        search_results = enumerate(chain(results,results2))

    return render(request, 'home.html.haml', { 'search_results': search_results })

def users_show(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.is_active:
            myclass = 'btn-success'
        else:
            myclass = 'btn-danger'

        return render(request, 'users/show.html.haml', { 'user': user, 'myclass': myclass } )
    except User.DoesNotExist:
        return render(request, 'error.html.haml')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('home.html.haml')
    else:
        form = SignUpForm()
    if request.user.is_authenticated():
        return render(request, 'home.html.haml')
    else:
        return render(request, 'signup.html.haml', { 'form': form })

def logout_view(request):
    logout(request)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                # Redirect to a success page.
                return render(request, 'home.html.haml')
            else:
                # Return a 'disabled account' error message
                return render(request, 'home.html.haml')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'home.html.haml')
    else:
        form = LoginForm()

    return render(request, 'login.html.haml', { 'form': form })

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username','first_name', 'last_name', 'email',]
    template_name = 'users/edit.html.haml'
    success_url = reverse_lazy('users_show')

    def get_success_url(self):
        user_id = self.kwargs['pk']
        return reverse_lazy('users_show', kwargs={'user_id': user_id} )


def items_add_to_storage(request,item_id):
    user_spaces = Space.objects.filter(user_id=request.user.id)
    user_spaces_ids = user_spaces.values_list('id', flat=True)

    # If this is from the filter form (dropdown)
    if request.method == 'POST':
        selected_space_id = request.POST['space_id']
        if selected_space_id == 'all':
            storages = Storage.objects.filter(space_id__in=user_spaces_ids)
        else:
            storages = Storage.objects.filter(space_id=selected_space_id)
        if request.user is not None:
            form = space_dropdown_form(user=request.user)
            form.fields['space_id'].initial = selected_space_id

    # else this is the index
    else:
        storages = Storage.objects.filter(space_id__in=user_spaces_ids)
        if request.user is not None:
            form = space_dropdown_form(user=request.user)
        selected_space_id = None
    return render(request, 'storages/index.html.haml', {'storages': storages,
                                                        'user_spaces': user_spaces,
                                                        'form': form,
                                                        'item_id': item_id,
                                                        'selected_space_id': selected_space_id})


def items_add_existing_storage(request, storage_id, item_id):

    if storage_id is None:
        return render(request, 'error.html.haml')
    else:
        if Items_Storage.objects.filter(storage_id=storage_id, items_id=item_id).exists():
            return render(request, 'items_storage_unique_error.html.haml')
        else:
            new_item = Items_Storage(storage_id=storage_id, items_id=item_id)
            new_item.save()
            return HttpResponseRedirect(reverse('storages_show', kwargs={'storage_id': storage_id}))
