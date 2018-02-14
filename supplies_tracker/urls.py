"""supplies_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from supplies_tracker import views as supplies_tracker_views
from django.contrib.auth import views as auth_views
# from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', include('admin_tools.urls')),
    url(r'^$', views.home, name='home'),

    url(r'items$', views.items_index, name='items_index'),
    url('items/new', views.items_new, name='items_new'),
    url(r'^items/(?P<item_id>[0-9]+)/$', views.items_show, name='items_show'),
    url(r'^items/(?P<pk>[0-9]+)/edit$', views.ItemUpdate.as_view(), name='items_update'),
    url(r'^items/(?P<pk>[0-9]+)/delete/$', views.ItemDelete.as_view(), name='items_delete'),

    url(r'^storages/items/add/(?P<item_id>[0-9]+)/', views.items_add_to_storage, name='items_add_to_storage'),
    url(r'^storages/(?P<storage_id>[0-9]+)/items/(?P<item_id>[0-9]+)/insert', views.items_add_existing_storage,
        name='items_add_existing_storage'),

    url(r'^storages/(?P<storage_id>[0-9]+)/add_item/(?P<item_id>[0-9]+)/$', views.add_item, name='add_item'),
    url(r'^storages/(?P<storage_id>[0-9]+)/remove_item/(?P<item_id>[0-9]+)/$', views.remove_item, name='remove_item'),

    url(r'storages/$', views.storages_index, name='storages_index'),
    url(r'^storages/new/$', views.storages_new, name='storages_new'),
    url(r'^spaces/(?P<space_id>[0-9]+)/storages/new/$', views.storages_new, name='storages_new'),
    url(r'^storages/(?P<storage_id>[0-9]+)/$', views.storages_show, name='storages_show'),
    url(r'^storages/(?P<pk>[0-9]+)/edit$', views.StorageUpdate.as_view(), name='storages_update'),
    url(r'^storages/(?P<pk>[0-9]+)/delete/$', views.StorageDelete.as_view(), name='storages_delete'),

    url(r'spaces$', views.spaces_index, name='spaces_index'),
    url('spaces/new', views.spaces_new, name='spaces_new'),
    url(r'^spaces/(?P<space_id>[0-9]+)/$', views.spaces_show, name='spaces_show'),
    url(r'^spaces/(?P<pk>[0-9]+)/edit$', views.SpaceUpdate.as_view(), name='spaces_update'),
    url(r'^spaces/(?P<pk>[0-9]+)/delete/$', views.SpaceDelete.as_view(), name='spaces_delete'),

    url(r'^login/$', supplies_tracker_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', supplies_tracker_views.signup, name='signup'),
    url(r'^users/(?P<user_id>[0-9]+)/$', views.users_show, name='users_show'),
    url(r'^users/edit$', views.UserUpdate.as_view(), name='user_update'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
