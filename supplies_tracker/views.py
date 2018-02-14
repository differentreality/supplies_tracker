from itertools import chain

from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import UpdateView, DeleteView

from .models import Item, Storage, Space, Items_Storage
from .forms import ItemForm, StorageForm, SpaceForm, SignUpForm, LoginForm, SpaceDropdownForm


# @login_required
def items_index(request):
    items = Item.objects.all()
    return render(request, 'items/index.html.haml', {'items': items})


class SpaceUpdate(UpdateView):
    model = Space
    fields = ['name', 'address', 'description', 'image']
    template_name = 'spaces/edit.html.haml'
    success_url = reverse_lazy('spaces_index')


class SpaceDelete(DeleteView):
    model = Space
    success_url = reverse_lazy('spaces_index')


class StorageUpdate(UpdateView):
    template_name = 'storages/edit.html.haml'
    model = Storage
    fields = ['name', 'image']
    success_url = reverse_lazy('storages_index')


class StorageDelete(DeleteView):
    model = Storage
    success_url = reverse_lazy('storages_index')


class ItemUpdate(UpdateView):
    model = Item
    fields = ['name', 'description', 'price_bought', 'reimbursement', 'image']
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
    return HttpResponseRedirect(reverse('storages_show', kwargs={'storage_id': storage_id}))


def remove_item(request, storage_id, item_id):
    storage = Storage.objects.get(id=storage_id)
    storage_items = storage.item.all()
    item = Item.objects.get(id=item_id)
    items_storage = item.items_storage_set.get(storage_id=storage_id)

    if (items_storage.quantity > 0):
        items_storage.quantity = items_storage.quantity - 1
        items_storage.save()
    return HttpResponseRedirect(reverse('storages_show', kwargs={'storage_id': storage_id}))


@login_required
def items_new(request):
    if 'storage_id' in request.GET:
        storage_id = request.GET['storage_id']
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Item(**form.cleaned_data)
            obj.user = request.user
            obj.save()
            if 'storage_id' in request.GET and request.GET['storage_id'] is not None and request.GET[
                'storage_id'] != '':
                storage_id = request.GET['storage_id']
                new_item = Items_Storage(storage_id=storage_id, item=Item.objects.get(id=obj.id))
                new_item.save()
                return HttpResponseRedirect(reverse('storages_show', kwargs={'storage_id': storage_id}))
            else:
                return HttpResponseRedirect(reverse('items_index'))
    else:
        form = ItemForm()
        return render(request, 'items/new.html.haml', {'form': form})


def items_show(request, item_id):
    item = Item.objects.get(id=item_id)
    items_storages = Items_Storage.objects.filter(item_id=item_id)
    return render(request, 'items/show.html.haml', {'item': item, 'items_storages': items_storages})


# @login_required
def storages_index(request):
    if request.user.is_anonymous:
        user_spaces = Space.objects.all()
    else:
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
            form = SpaceDropdownForm(user=request.user)
            form.fields['space_id'].initial = selected_space_id
    # else this is the index
    else:
        storages = Storage.objects.filter(space_id__in=user_spaces_ids)

        form = SpaceDropdownForm(user=request.user)
        selected_space_id = None

    return render(request, 'storages/index.html.haml', {'storages': storages,
                                                        'user_spaces': user_spaces,
                                                        'form': form,
                                                        'selected_space_id': selected_space_id})


def storages_show(request, storage_id):
    try:
        storage = Storage.objects.get(id=storage_id)
        items_storage = Items_Storage.objects.filter(storage_id=storage_id)

        items_cost_sum = 0
        items_reimbursement_sum = 0
        for storage_item in items_storage:
            items_cost_sum += int(storage_item.quantity or 0) * float(storage_item.item.price_bought or 0)
            items_reimbursement_sum += int(storage_item.quantity or 0) * float(storage_item.item.reimbursement or 0)

        # # items_cost_sum = storage.item.aggregate(Sum('price_bought'))
        # items_reimbursement_sum = storage.item.aggregate(Sum('reimbursement'))

    except Storage.DoesNotExist:
        storage = None
        items = None

    if storage is None:
        return render(request, 'error.html.haml')
    else:
        if request.user.is_anonymous:
            return render(request, 'storages/public.html.haml', {'storage': storage, 'items_storage': items_storage})
        else:
            return render(request, 'storages/show.html.haml', {'storage': storage,
                                                               'items_storage': items_storage,
                                                               'items_cost': items_cost_sum,
                                                               'items_reimbursement': items_reimbursement_sum})


@login_required
def storages_new(request, space_id=None):
    if space_id is None:
        space = None
    else:
        space = Space.objects.get(id=space_id)

    if request.method == 'POST':
        form = StorageForm(None, request.POST, request.FILES)
        if form.is_valid():
            obj = Storage(**form.cleaned_data)
            if space_id is None:
                space_id = form.data.get('space_id')
                obj.space_id = space_id
            else:
                obj.space_id = space_id

            obj.save()

            return HttpResponseRedirect(reverse('spaces_show', kwargs={'space_id': space_id}))
    else:
        if space_id is None:
            form = StorageForm(user=request.user)
        else:
            form = StorageForm(None, None)

    return render(request, 'storages/new.html.haml', {'form': form, 'space': space})


# @login_required
def spaces_index(request):
    if request.user.is_anonymous:
        spaces = Space.objects.all()
    else:
        spaces = Space.objects.filter(user_id=request.user.id)

    return render(request, 'spaces/index.html.haml', {'spaces': spaces})


def spaces_show(request, space_id):
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
        form = SpaceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Space(**form.cleaned_data)
            obj.user = request.user
            obj.save()

            return HttpResponseRedirect('/spaces')
    else:
        form = SpaceForm()

    return render(request, 'spaces/new.html.haml', {'form': form})


def home(request):
    search_keyword = request.GET.get('search-keyword')
    search_results = None
    user_spaces = Space.objects.filter(user_id=request.user.id)

    if search_keyword is not None:
        if request.user.is_authenticated:
            spaces = Space.objects.filter(user_id=request.user.id)
        else:
            spaces = Space.objects.all()

        spaces_ids = spaces.values_list('id', flat=True)
        storages = Storage.objects.filter(space_id__in=spaces_ids)

        results_spaces = spaces.filter(Q(name__contains=search_keyword) |
                                       Q(description__contains=search_keyword) |
                                       Q(address__contains=search_keyword))
        results_storages = storages.filter(Q(name__contains=search_keyword))
        search_results = enumerate(chain(results_spaces, results_storages))

    return render(request, 'home.html.haml', {'search_results': search_results, 'user_spaces': user_spaces})


def users_show(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.is_active:
            myclass = 'btn-success'
        else:
            myclass = 'btn-danger'

        return render(request, 'users/show.html.haml', {'user': user, 'myclass': myclass})
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
            return redirect('home')
    else:
        form = SignUpForm()
    if request.user.is_anonymous:
        return render(request, 'signup.html.haml', {'form': form})
    else:
        return render(request, 'home.html.haml')


def logout_view(request):
    logout(request)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to a success page.
            return redirect('home')

    form = LoginForm()
    return render(request, 'login.html.haml', {'form': form})


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', ]
    template_name = 'users/edit.html.haml'
    success_url = reverse_lazy('users_show')

    def get_object(self):
        """
        Only return the User object that belongs to the logged-in User
        """
        return self.request.user

    def get_success_url(self):
        user_id = self.request.user.pk
        return reverse_lazy('users_show', kwargs={'user_id': user_id} )

@login_required
def items_add_to_storage(request, item_id):
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
            form = SpaceDropdownForm(user=request.user)
            form.fields['space_id'].initial = selected_space_id

    # else this is the index
    else:
        storages = Storage.objects.filter(space_id__in=user_spaces_ids)
        if request.user is not None:
            form = SpaceDropdownForm(user=request.user)
        selected_space_id = None
    return render(request, 'storages/index.html.haml', {'storages': storages,
                                                        'user_spaces': user_spaces,
                                                        'form': form,
                                                        'item_id': item_id,
                                                        'selected_space_id': selected_space_id})


@login_required
def items_add_existing_storage(request, storage_id, item_id):
    if storage_id is None:
        return render(request, 'error.html.haml')
    else:
        if Items_Storage.objects.filter(storage_id=storage_id, item_id=item_id).exists():
            return render(request, 'items_storage_unique_error.html.haml')
        else:
            new_item = Items_Storage(storage_id=storage_id, item_id=item_id)
            new_item.save()
            return HttpResponseRedirect(reverse('storages_show', kwargs={'storage_id': storage_id}))
