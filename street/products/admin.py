from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'lang', 'city', 'name', 'contact']
    list_filter = ['chat_id', 'lang', 'city']
    search_fields = ['chat_id', 'lang', 'city']
# admin.site.register(Basket)
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item']
    list_filter = ['id', 'user', 'item']
    search_fields = ['id', 'user']
    ordering = ['id']
# admin.site.register(City)
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_uz']
    list_filter = ['id', 'name_uz']
    search_fields = ['id', 'name_uz']
# admin.site.register(Branches)
@admin.register(Branches)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city']
    list_filter = ['id', 'name', 'city']
    search_fields = ['id', 'name', 'city']
    ordering = ['id']
# admin.site.register(Category)
@admin.register(Category)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    search_fields = ['id', 'name']
# admin.site.register(Items)
@admin.register(Items)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    list_filter = ['id', 'name', 'category']
    search_fields = ['id', 'name', 'category']
    ordering = ['id']
