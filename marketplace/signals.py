from .models import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# post_save signal is the one we will use to create a profile when a User is created
# User will send the info that created = True  , so do something
# post_save_create_profile can be renamed to anything
# sender=User instance=User instance created=Boolean (only True on creation, can be True only once)
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    print(sender)
    print(instance)
    print(created)
    # (only True on creation, can be True only once)
    # when True, create a profile and add the user to the instance
    # if created:
    #     Profile.objects.create(user=instance)   ???Deleted cause it broke app???
        #see apps.py for registration in ready method
