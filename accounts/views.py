from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CompanyForm, JobSeekerProfileForm
from .models import CustomUser, Company, JobSeekerProfile
from .forms import CustomUserCreationForm, CompanyForm, JobSeekerProfileForm, CustomUser


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        role = request.POST.get('role')

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.role = role
            user.save()

            # Handle profile creation based on role
            if role == CustomUser.Role.EMPLOYER:
                company_form = CompanyForm(request.POST, request.FILES)
                if company_form.is_valid():
                    # Use get_or_create to prevent duplicate company creation
                    company, created = Company.objects.get_or_create(
                        user=user,
                        defaults=company_form.cleaned_data
                    )
                    if not created:
                        # Update existing company if needed
                        company_form = CompanyForm(request.POST, request.FILES, instance=company)
                        company_form.save()
                    messages.success(request, 'Company account created successfully!')
                    return redirect('login')
                else:
                    user.delete()  # Rollback user creation
                    messages.error(request, 'Invalid company information')
            
            elif role == CustomUser.Role.JOBSEEKER:
                profile_form = JobSeekerProfileForm(request.POST, request.FILES)
                if profile_form.is_valid():
                    profile, created = JobSeekerProfile.objects.get_or_create(
                        user=user,
                        defaults=profile_form.cleaned_data
                    )
                    if not created:
                        profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
                        profile_form.save()
                    messages.success(request, 'Job seeker account created successfully!')
                    return redirect('login')
                else:
                    user.delete()  # Rollback user creation
                    messages.error(request, 'Invalid profile information')
            
            return render(request, 'accounts/register.html', {
                'user_form': user_form,
                'company_form': company_form if role == CustomUser.Role.EMPLOYER else CompanyForm(),
                'profile_form': profile_form if role == CustomUser.Role.JOBSEEKER else JobSeekerProfileForm()
            })
        
        else:
            messages.error(request, 'Please correct the errors below')
    
    else:
        user_form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'company_form': CompanyForm(),
        'profile_form': JobSeekerProfileForm()
    })

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def profile(request):
    user = request.user
    context = {}
    
    if user.role == CustomUser.Role.EMPLOYER and hasattr(user, 'company'):
        company = user.company
        if request.method == 'POST':
            form = CompanyForm(request.POST, request.FILES, instance=company)
            if form.is_valid():
                form.save()
                messages.success(request, 'Company profile updated!')
                return redirect('profile')
        else:
            form = CompanyForm(instance=company)
        context['form'] = form
        context['is_employer'] = True
    
    elif user.role == CustomUser.Role.JOBSEEKER and hasattr(user, 'jobseeker_profile'):
        profile = user.jobseeker_profile
        if request.method == 'POST':
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('profile')
        else:
            form = JobSeekerProfileForm(instance=profile)
        context['form'] = form
        context['is_jobseeker'] = True
    
    return render(request, 'accounts/profile.html', context)
