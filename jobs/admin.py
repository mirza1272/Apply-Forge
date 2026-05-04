from django.contrib import admin
from .models import Job, JobCategory

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'is_active')
    list_filter = ('is_active', 'job_type')

admin.site.register(Job, JobAdmin)
admin.site.register(JobCategory)