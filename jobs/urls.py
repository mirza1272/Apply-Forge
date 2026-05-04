from django.urls import path, include
from .views import (
    home, job_list, job_detail, create_job, update_job, delete_job,
    employer_dashboard, job_applications, update_application_status
)
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:pk>/', job_detail, name='job_detail'),
    path('jobs/create/', create_job, name='create_job'),
    path('jobs/<int:pk>/update/', update_job, name='update_job'),
    path('jobs/<int:pk>/delete/', delete_job, name='delete_job'),
    path('dashboard/', employer_dashboard, name='employer_dashboard'),
    path('jobs/<int:pk>/applications/', job_applications, name='job_applications'),
    path('applications/<int:pk>/<str:status>/', update_application_status, name='update_application_status'),
]