from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Company, JobSeekerProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == CustomUser.Role.EMPLOYER:
            Company.objects.get_or_create(
                user=instance,
                defaults={'name': f'{instance.username} Company'}
            )
        elif instance.role == CustomUser.Role.JOBSEEKER:
            JobSeekerProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'bio': '',
                    'skills': '',
                    'experience': '',
                    'education': '',
                    'resume': None
                }
            )