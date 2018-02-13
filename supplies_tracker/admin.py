from django.contrib import admin
from .models import Item, Space, Storage


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price_bought', 'reimbursement', 'image', 'created_at')
    list_filter = ('name', 'price_bought', 'reimbursement', 'created_at')
    search_fields = ('name', 'description')


class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'address', 'image', 'user_id')
    list_filter = ('name', 'description', 'address', 'created_at', 'user_id')
    search_fields = ('name', 'address')


class StorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'space_id')
    list_filter = ('name', 'space_id')
    search_fields = ('name', 'space_id')


admin.site.register(Item, ItemAdmin)
admin.site.register(Space, SpaceAdmin)
admin.site.register(Storage, StorageAdmin)
