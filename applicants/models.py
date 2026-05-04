from django.db import models
from accounts.models import CustomUser
from jobs.models import Job

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        REVIEWED = 'REVIEWED', 'Reviewed'
        INTERVIEW = 'INTERVIEW', 'Interview Scheduled'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'

    job = models.ForeignKey(
        'jobs.Job', 
        on_delete=models.CASCADE,
        related_name='job_applications' 
    )
    applicant = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_applications'
    )
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='applications/resumes/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job.title}"

    class Meta:
        ordering = ['-applied_on']
        unique_together = ('job', 'applicant')