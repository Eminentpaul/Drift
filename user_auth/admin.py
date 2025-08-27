from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'last_name', 'phone', 'email', 'gender', 'is_agent']
    list_display_links = ['user_id', 'first_name', 'last_name', 'phone']
    sortable_by = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    list_filter = ['is_agent']

    list_per_page = 10
    
admin.site.register(User, UserAdmin)