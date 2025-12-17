# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User, Group
# from .models import StudentProfile

# @receiver(post_save, sender=User)
# def create_profile_and_group(sender, instance, created, **kwargs):
#     if created:
#         StudentProfile.objects.create(user=instance)
#         instance.groups.add(Group.objects.get(name='Student'))
