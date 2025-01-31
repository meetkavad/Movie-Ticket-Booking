from django.contrib import admin
from .models import AuthModel

# Register your models here.
class AuthAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')

admin.site.register(AuthModel, AuthAdmin)