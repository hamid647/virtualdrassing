from django.contrib import admin
from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(products)
class productAdmin(admin.ModelAdmin):
    list_display = ('name','price')