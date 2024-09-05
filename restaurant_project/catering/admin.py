from django.contrib import admin
from .models import MenuItem, CateringBooking, Category

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')

@admin.register(CateringBooking)
class CateringBookingAdmin(admin.ModelAdmin):
    list_display = ('id',)
    # Other settings if needed

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
