from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company, JobSeekerProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')

class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)