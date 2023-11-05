from django.contrib import admin
from .models import registered_data

class registration(admin.ModelAdmin):
    search_fields = ('first_name','last_name')
# Register your models here.
admin.site.register(registered_data,registration)