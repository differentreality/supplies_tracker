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
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from supplies_tracker import views as supplies_tracker_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'', include('item.urls')),
    url(r'^$', views.items_index, name='items_index'), # change the index page
    url('items/new', views.items_new, name='items_new'),
    url('items', views.items_index, name='items_index'),
    url('storages/new', views.storages_new, name='storages_new'),
    url('storages', views.storages_index, name='storages_index'),
    url('spaces/new', views.spaces_new, name='spaces_new'),
    url('spaces', views.spaces_index, name='spaces_index'),
    url(r'^$', supplies_tracker_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', supplies_tracker_views.signup, name='signup'),
    url(r'^signup/$', supplies_tracker_views.signup, name='signup'),
]
