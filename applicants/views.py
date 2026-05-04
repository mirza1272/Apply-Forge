from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from .models import Application
from .forms import ApplicationForm
from accounts.models import JobSeekerProfile
from accounts.models import CustomUser

@login_required
def apply_job(request, pk):
    if request.user.role != CustomUser.Role.JOBSEEKER:
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('home')
    
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    if not hasattr(request.user, 'jobseeker_profile'):
        messages.error(request, 'Please complete your profile first.')
        return redirect('profile')
    
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.profile = request.user.jobseeker_profile
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('job_detail', pk=pk)
    else:
        form = ApplicationForm()
    
    context = {
        'job': job,
        'form': form,
    }
    return render(request, 'applicants/apply_job.html', context)

@login_required
def my_applications(request):
    if request.user.role != CustomUser.Role.JOBSEEKER:
        messages.error(request, 'Only job seekers can view applications.')
        return redirect('home')
    
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_on')
    
    context = {
        'applications': applications,
    }
    return render(request, 'applicants/my_applications.html', context)

@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    
    context = {
        'application': application,
    }
    return render(request, 'applicants/application_detail.html', context)