from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_on')
    list_filter = ('status', 'job__company')

admin.site.register(Application, ApplicationAdmin)