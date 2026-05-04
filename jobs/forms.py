from django import forms
from .models import Job, JobCategory

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'description', 'location', 'job_type', 'salary_range', 'category', 'deadline')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = ('name', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }