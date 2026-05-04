from django.urls import path
from .views import apply_job, my_applications, application_detail
from . import views
urlpatterns = [
    path('jobs/<int:pk>/apply/', apply_job, name='apply_job'),
    path('my-applications/', my_applications, name='my_applications'),
    path('my-applications/<int:pk>/', application_detail, name='application_detail'),
]