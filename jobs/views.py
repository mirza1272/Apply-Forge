from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from .models import Job, JobCategory
from .forms import JobForm, JobCategoryForm
from accounts.models import Company, CustomUser
from applicants.models import Application

@staff_member_required
def admin_stats_view(request):
    context = {
        'job_count': Job.objects.count(),
        'application_count': Application.objects.count(),
    }
    return render(request, 'admin/job_stats.html', context)

def home(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = JobCategory.objects.all()[:6]
    context = {
        'jobs': jobs,
        'categories': categories,
    }
    return render(request, 'jobs/home.html', context)

def job_list(request):
    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    job_type = request.GET.get('type')
    category = request.GET.get('category')

    jobs = Job.objects.filter(is_active=True).order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__name__icontains=query)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if category:
        jobs = jobs.filter(category__id=category)

    context = {
        'jobs': jobs,
        'categories': JobCategory.objects.all(),
        'search_query': query,
        'location_query': location,
        'job_type_query': job_type,
        'category_query': category,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    has_applied = False

    if request.user.is_authenticated and request.user.role == CustomUser.Role.JOBSEEKER:
        has_applied = Application.objects.filter(
            job=job, 
            applicant=request.user
        ).exists()

    context = {
        'job': job,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def create_job(request):
    if request.user.role != CustomUser.Role.EMPLOYER:
        raise PermissionDenied("Only employers can post jobs")

    if not hasattr(request.user, 'company'):
        messages.error(request, 'Please complete your company profile first.')
        return redirect('profile')

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})

@login_required
def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company__user=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/update_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company__user=request.user)

    if request.method == 'POST':
        job.is_active = False
        job.save()
        messages.success(request, 'Job has been deactivated.')
        return redirect('employer_dashboard')

    return render(request, 'jobs/delete_job.html', {'job': job})

@login_required
def employer_dashboard(request):
    if request.user.role != CustomUser.Role.EMPLOYER:
        raise PermissionDenied("Only employers can access this page")

    if not hasattr(request.user, 'company'):
        messages.error(request, 'Please complete your company profile first.')
        return redirect('profile')

    company = request.user.company
    active_jobs = company.jobs.filter(is_active=True)
    
    total_applications = Application.objects.filter(
        job__in=active_jobs
    ).count()

    context = {
        'company': company,
        'jobs': active_jobs.order_by('-created_at'),
        'total_applications': total_applications,
        'active_jobs_count': active_jobs.count(),
    }
    return render(request, 'jobs/employer_dashboard.html', context)

@login_required
def job_applications(request, pk):
    job = get_object_or_404(Job, pk=pk, company__user=request.user)
    
    applications = Application.objects.filter(job=job).select_related('applicant') \
                      .order_by('-applied_on')
    
    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'jobs/job_applications.html', context)

@login_required
def update_application_status(request, pk, status):
    application = get_object_or_404(
        Application,
        pk=pk,
        job__company__user=request.user
    )
    
    # Define valid status transitions
    valid_statuses = {
        'PENDING': ['REVIEWED', 'REJECTED'],
        'REVIEWED': ['INTERVIEW', 'REJECTED'],
        'INTERVIEW': ['ACCEPTED', 'REJECTED'],
        'ACCEPTED': ['ACCEPTED', 'REVIEWED', 'INTERVIEW'],
        'REJECTED': ['ACCEPTED', 'REVIEWED', 'INTERVIEW']
    }
    
    current_status = application.status
    allowed_transitions = valid_statuses.get(current_status, [])
    
    if status in allowed_transitions:
        application.status = status
        application.save()
        messages.success(request, f'Status changed from {current_status} to {status}')
    else:
        messages.error(request, f'Invalid status transition from {current_status} to {status}')
    
    return redirect('job_applications', pk=application.job.pk)