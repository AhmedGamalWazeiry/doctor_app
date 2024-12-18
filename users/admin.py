from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomAdmin(UserAdmin):
    list_display = ['username', 'id']


admin.site.register(User, CustomAdmin)