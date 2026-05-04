from .models import JobCategory

def job_categories(request):
    return {
        'job_categories': JobCategory.objects.all()[:10]
    }