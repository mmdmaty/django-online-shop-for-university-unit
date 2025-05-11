from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from . import forms

@admin.register(models.CustomUserModel)
class CustomUserAdmin(UserAdmin):
    pass